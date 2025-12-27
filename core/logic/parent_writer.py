"""
Parent Communication Writer
Drafts messages for parent communication.
"""
import os
from utils.helpers import call_openai, save_to_file, setup_logger

logger = setup_logger(__name__)


def generate_parent_message(purpose, child_name, context, teacher_name=""):
    """
    Generate a parent communication message.
    
    Args:
        purpose (str): Purpose of message - "reminder", "feedback", "appreciation", or "concern"
        child_name (str): Name of the student
        context (str): Specific details about the message content
        teacher_name (str): Name of the teacher (optional)
    
    Returns:
        dict: Generated message with metadata
    """
    logger.info(f"Generating parent message ({purpose}) for {child_name}")
    
    try:
        # Load prompt template
        prompt_path = os.path.join("core", "prompts", "parent_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        # Fill in template variables
        prompt = prompt_template.format(
            purpose=purpose,
            child_name=child_name,
            context=context
        )
        
        # Call AI API with lighter settings to avoid rate limits
        response = call_openai(prompt, temperature=0.6, max_tokens=500)
        
        # Add teacher signature if provided
        if teacher_name:
            response += f"\n\nWarm regards,\n{teacher_name}"
        
        # Save output
        output_filename = f"parent_message_{purpose}_{child_name}".replace(" ", "_").lower()
        output_path = save_to_file(response, output_filename, folder="parent_messages")
        
        logger.info(f"Parent message generated successfully: {output_path}")
        
        return {
            "success": True,
            "message": response,
            "metadata": {
                "purpose": purpose,
                "child_name": child_name,
                "output_file": output_path
            }
        }
    
    except Exception as e:
        logger.error(f"Failed to generate parent message: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the generator
    result = generate_parent_message(
        purpose="appreciation",
        child_name="Liam Chen",
        context="Liam showed exceptional kindness by helping a new student feel welcome during lunch break. He shared his crayons and invited them to join his group.",
        teacher_name="Ms. Sarah Thompson"
    )
    
    if result["success"]:
        print("✅ Message Generated Successfully!")
        print("\n" + "="*50)
        print(result["message"])
        print("="*50)
    else:
        print(f"❌ Error: {result['error']}")

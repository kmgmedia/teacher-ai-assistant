"""
Lesson Note Generator
Generates structured lesson plans for teachers.
"""
import os
from utils.helpers import call_openai, save_to_file, setup_logger

logger = setup_logger(__name__)


def generate_lesson(subject, topic, age_group, objectives, duration=60):
    """
    Generate a comprehensive lesson note.
    
    Args:
        subject (str): The subject being taught (e.g., "Mathematics", "Science")
        topic (str): The specific topic (e.g., "Addition", "Plant Life Cycle")
        age_group (str): Target age group (e.g., "5-6 years", "Grade 2")
        objectives (str): Learning objectives for the lesson
        duration (int): Lesson duration in minutes (default: 60)
    
    Returns:
        dict: Generated lesson note with metadata
    """
    logger.info(f"Generating lesson note for {subject} - {topic}")
    
    try:
        # Load prompt template
        prompt_path = os.path.join("core", "prompts", "lesson_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        # Fill in template variables
        prompt = prompt_template.format(
            subject=subject,
            topic=topic,
            age_group=age_group,
            duration=duration,
            objectives=objectives
        )
        
        # Call AI API with lighter settings to avoid rate limits
        response = call_openai(prompt, temperature=0.6, max_tokens=600)
        
        # Save output
        output_filename = f"lesson_{subject}_{topic}".replace(" ", "_").lower()
        output_path = save_to_file(response, output_filename, folder="lessons")
        
        logger.info(f"Lesson note generated successfully: {output_path}")
        
        return {
            "success": True,
            "lesson_note": response,
            "metadata": {
                "subject": subject,
                "topic": topic,
                "age_group": age_group,
                "duration": duration,
                "output_file": output_path
            }
        }
    
    except Exception as e:
        logger.error(f"Failed to generate lesson note: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the generator
    result = generate_lesson(
        subject="Mathematics",
        topic="Introduction to Addition",
        age_group="5-6 years (Kindergarten)",
        objectives="Students will understand the concept of combining groups and represent addition with objects and symbols",
        duration=45
    )
    
    if result["success"]:
        print("✅ Lesson Generated Successfully!")
        print("\n" + "="*50)
        print(result["lesson_note"])
        print("="*50)
    else:
        print(f"❌ Error: {result['error']}")

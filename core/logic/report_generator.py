"""
Student Report Generator
Creates professional progress reports for students.
"""
import os
from utils.helpers import call_openai, save_to_file, setup_logger

logger = setup_logger(__name__)


def generate_report(student_name, period, subject, performance_notes, behavior_notes):
    """
    Generate a student progress report.
    
    Args:
        student_name (str): Name of the student
        period (str): Reporting period (e.g., "Term 1", "September-November 2025")
        subject (str): Subject or area being reported on
        performance_notes (str): Academic performance observations
        behavior_notes (str): Behavioral and social-emotional observations
    
    Returns:
        dict: Generated report with metadata
    """
    logger.info(f"Generating report for student: {student_name}")
    
    try:
        # Load prompt template
        prompt_path = os.path.join("core", "prompts", "report_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        # Fill in template variables
        prompt = prompt_template.format(
            student_name=student_name,
            period=period,
            subject=subject,
            performance_notes=performance_notes,
            behavior_notes=behavior_notes
        )
        
        # Call AI API with lighter settings to avoid rate limits
        response = call_openai(prompt, temperature=0.6, max_tokens=600)
        
        # Save output
        output_filename = f"report_{student_name}_{period}".replace(" ", "_").lower()
        output_path = save_to_file(response, output_filename, folder="reports")
        
        logger.info(f"Report generated successfully: {output_path}")
        
        return {
            "success": True,
            "report": response,
            "metadata": {
                "student_name": student_name,
                "period": period,
                "subject": subject,
                "output_file": output_path
            }
        }
    
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the generator
    result = generate_report(
        student_name="Emma Johnson",
        period="Term 1 (September-December 2025)",
        subject="Overall Progress",
        performance_notes="Shows strong literacy skills, reads independently. Math: solid understanding of number sense 1-20. Needs support with fine motor tasks.",
        behavior_notes="Participates actively in group activities. Works well with peers. Sometimes needs reminders to stay focused during transitions."
    )
    
    if result["success"]:
        print("✅ Report Generated Successfully!")
        print("\n" + "="*50)
        print(result["report"])
        print("="*50)
    else:
        print(f"❌ Error: {result['error']}")

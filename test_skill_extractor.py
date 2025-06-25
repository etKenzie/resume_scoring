import asyncio
import json
import os
from app.resume_scorer import skill_extractor_agent, Runner

async def test_skill_extractor():
    """Test the skill extractor agent with a sample resume."""
    
    # Sample resume path (you can replace this with an actual resume file)
    resume_path = "test/sales/Dindin Moch Waludin.pdf"
    
    # Sample target skills to check for
    target_skills = "Python, JavaScript, React, SQL, Sales, Marketing, Customer Service, Leadership, Communication"
    
    # Prepare input for the skill extractor
    skill_extraction_input = json.dumps({
        "resume_path": resume_path,
        "target_skills": target_skills
    })
    
    print("Testing Skill Extractor Agent...")
    print(f"Resume: {resume_path}")
    print(f"Target Skills: {target_skills}")
    print("-" * 50)
    
    try:
        # Run the skill extractor agent
        result = await Runner.run(
            skill_extractor_agent,
            skill_extraction_input
        )
        
        print("\nSkill Extraction Results:")
        print(f"Skills Found: {result.final_output.skills_found}")
        print(f"Total Skills Checked: {result.final_output.total_skills_checked}")
        print(f"Match Percentage: {result.final_output.match_percentage:.2%}")
        print(f"Skill Context: {result.final_output.skill_context}")
        
        return result.final_output
        
    except Exception as e:
        print(f"Error during skill extraction: {str(e)}")
        raise

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_skill_extractor()) 
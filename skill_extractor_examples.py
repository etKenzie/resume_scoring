import asyncio
import json
from app.resume_scorer import skill_extractor_agent, Runner

async def example_tech_skills():
    """Example: Check for technical skills in a resume."""
    print("=== TECHNICAL SKILLS EXAMPLE ===")
    
    resume_path = "test/sales/Dindin Moch Waludin.pdf"
    tech_skills = "Python, JavaScript, React, Node.js, SQL, MongoDB, AWS, Docker, Git, Agile"
    
    input_data = json.dumps({
        "resume_path": resume_path,
        "target_skills": tech_skills
    })
    
    result = await Runner.run(skill_extractor_agent, input_data)
    
    print(f"Technical Skills Checked: {tech_skills}")
    print(f"Skills Found: {result.final_output.skills_found}")
    print(f"Match Rate: {result.final_output.match_percentage:.1%}")
    print()

async def example_soft_skills():
    """Example: Check for soft skills in a resume."""
    print("=== SOFT SKILLS EXAMPLE ===")
    
    resume_path = "test/sales/Dindin Moch Waludin.pdf"
    soft_skills = "Leadership, Communication, Teamwork, Problem Solving, Time Management, Customer Service"
    
    input_data = json.dumps({
        "resume_path": resume_path,
        "target_skills": soft_skills
    })
    
    result = await Runner.run(skill_extractor_agent, input_data)
    
    print(f"Soft Skills Checked: {soft_skills}")
    print(f"Skills Found: {result.final_output.skills_found}")
    print(f"Match Rate: {result.final_output.match_percentage:.1%}")
    print()

async def example_sales_skills():
    """Example: Check for sales-specific skills in a resume."""
    print("=== SALES SKILLS EXAMPLE ===")
    
    resume_path = "test/sales/Dindin Moch Waludin.pdf"
    sales_skills = "Sales, Marketing, CRM, Lead Generation, Negotiation, Account Management, Cold Calling"
    
    input_data = json.dumps({
        "resume_path": resume_path,
        "target_skills": sales_skills
    })
    
    result = await Runner.run(skill_extractor_agent, input_data)
    
    print(f"Sales Skills Checked: {sales_skills}")
    print(f"Skills Found: {result.final_output.skills_found}")
    print(f"Match Rate: {result.final_output.match_percentage:.1%}")
    print()

async def example_mixed_skills():
    """Example: Check for a mix of technical and business skills."""
    print("=== MIXED SKILLS EXAMPLE ===")
    
    resume_path = "test/sales/Dindin Moch Waludin.pdf"
    mixed_skills = "Excel, PowerPoint, Data Analysis, Project Management, Sales, Customer Relationship"
    
    input_data = json.dumps({
        "resume_path": resume_path,
        "target_skills": mixed_skills
    })
    
    result = await Runner.run(skill_extractor_agent, input_data)
    
    print(f"Mixed Skills Checked: {mixed_skills}")
    print(f"Skills Found: {result.final_output.skills_found}")
    print(f"Match Rate: {result.final_output.match_percentage:.1%}")
    print(f"Skill Context: {result.final_output.skill_context}")
    print()

async def run_all_examples():
    """Run all skill extraction examples."""
    print("SKILL EXTRACTOR AGENT EXAMPLES")
    print("=" * 50)
    
    try:
        await example_tech_skills()
        await example_soft_skills()
        await example_sales_skills()
        await example_mixed_skills()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_all_examples()) 
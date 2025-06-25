#!/usr/bin/env python3
"""
Simple client example for the Resume Scoring API
"""

import requests
import json
import sys
from pathlib import Path

def score_resume(api_url, resume_path, job_description, target_skills=None):
    """
    Score a resume using the API
    
    Args:
        api_url: Base URL of the API (e.g., "https://your-app.railway.app")
        resume_path: Path to the resume file (PDF or text)
        job_description: Job description text
        target_skills: List of skills to check for
    
    Returns:
        API response as dictionary
    """
    
    # Prepare the request
    url = f"{api_url}/events/score-resume"
    
    # Check if file exists
    if not Path(resume_path).exists():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")
    
    # Prepare form data
    files = {"resume": open(resume_path, "rb")}
    data = {"job_description": job_description}
    
    if target_skills:
        if isinstance(target_skills, list):
            target_skills = ",".join(target_skills)
        data["target_skills"] = target_skills
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, files=files, data=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out. Resume scoring can take 30-60 seconds.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    finally:
        files["resume"].close()

def print_results(result):
    """Pretty print the scoring results"""
    if not result or not result.get("success"):
        print("❌ Scoring failed")
        if result and result.get("error"):
            print(f"Error: {result['error']}")
        return
    
    data = result["data"]
    
    print("\n" + "="*60)
    print("📊 RESUME SCORING RESULTS")
    print("="*60)
    
    # Overall score
    scoring = data.get("scoring", {})
    overall_score = scoring.get("overall_score", 0)
    print(f"\n🎯 Overall Score: {overall_score}/10")
    
    # Component scores
    print(f"\n📈 Component Scores:")
    print(f"   • Skills: {scoring.get('skill_score', 0)}/4.0")
    print(f"   • Experience: {scoring.get('experience_score', 0)}/4.5")
    print(f"   • Education: {scoring.get('education_score', 0)}/1.0")
    
    # Skills found
    skills_found = data.get("skills_found", {})
    if skills_found.get("skills_found"):
        print(f"\n✅ Skills Found ({skills_found.get('match_percentage', 0)*100:.1f}% match):")
        for skill in skills_found["skills_found"]:
            print(f"   • {skill}")
    
    # Strengths and weaknesses
    if scoring.get("strengths"):
        print(f"\n💪 Strengths:")
        for strength in scoring["strengths"]:
            print(f"   • {strength}")
    
    if scoring.get("weaknesses"):
        print(f"\n⚠️  Areas for Improvement:")
        for weakness in scoring["weaknesses"]:
            print(f"   • {weakness}")
    
    # Summary
    if scoring.get("summary"):
        print(f"\n📝 Summary:")
        print(f"   {scoring['summary']}")
    
    # Evaluation reasoning
    evaluation = data.get("evaluation", {})
    if evaluation.get("reasoning"):
        print(f"\n🤖 AI Evaluation:")
        print(f"   {evaluation['reasoning']}")

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 4:
        print("Usage: python client_example.py <api_url> <resume_path> <job_description> [skills...]")
        print("\nExample:")
        print("python client_example.py https://your-app.railway.app resume.pdf 'We are looking for a Python developer...' Python JavaScript React")
        sys.exit(1)
    
    api_url = sys.argv[1]
    resume_path = sys.argv[2]
    job_description = sys.argv[3]
    target_skills = sys.argv[4:] if len(sys.argv) > 4 else None
    
    print(f"🎯 Scoring resume: {resume_path}")
    print(f"📋 Job description: {job_description[:100]}...")
    if target_skills:
        print(f"🔧 Target skills: {', '.join(target_skills)}")
    
    result = score_resume(api_url, resume_path, job_description, target_skills)
    print_results(result)

if __name__ == "__main__":
    main() 
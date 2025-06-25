import requests
import os
import json

def test_resume_scoring():
    # API endpoint
    url = "http://localhost:8000/events/score-resume"
    
    # Path to your resume
    resume_path = "test\SalesOfficer\cv406181_ardhi suryani panggabean-1992-02-22.pdf"  # Update this to your actual resume path
    
    # Sample job description
    job_description = """
    SALES OFFICER

    KUALIFIKASI
    1.PRIA/WANITA
    2UMUR MAKS 30
    3.PENDIDIKAN MIN SMA
    4.PENGALAMAN MIN 1 TAHUN
    """
    target_skills=["Communication", "Emotional Intelligence", "Leadership", "Project Management", "Teamwork", "Strategic Planning", "Time Management", "Operations Management", "Creativity", "Sales & Lead Generation"]
    target_skills_2 = ["football", "coaching", "leadership"]
    
    # Prepare the files and data
    files = {
        'resume': ('Firza Hindrawardana.pdf', open(resume_path, 'rb'), 'application/pdf')
    }
    
    data = {
        'job_description': job_description,
        'target_skills': target_skills
    }
    
    # Send the request
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(response.json())
        with open("resume_scoring_result.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close the file
        files['resume'][1].close()

if __name__ == "__main__":
    test_resume_scoring() 
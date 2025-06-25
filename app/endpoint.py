import json
import os
import tempfile
from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from starlette.responses import Response
import asyncio
from resume_scorer import score_resume



router = APIRouter()

security = HTTPBearer()


class EventSchema(BaseModel):
    """Event Schema"""

    event_id: str
    event_type: str
    event_data: dict


class ResumeScoringRequest(BaseModel):
    """Resume Scoring Request Schema"""
    job_description: str
    target_skills: List[str] = []


class ResumeScoringResponse(BaseModel):
    """Resume Scoring Response Schema"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    message: str


"""
Becuase of the router, every endpoint in this file is prefixed with /events/
"""


@router.post("/", dependencies=[])
def handle_event(
    data: EventSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Response:
    print(data, credentials)

    # This is where you implement the AI logic to handle the event
    

    # Return acceptance response
    return Response(
        content=json.dumps({"message": "Data received!"}),
        status_code=HTTPStatus.ACCEPTED,
    )


@router.post("/score-resume", response_model=ResumeScoringResponse)
async def score_resume_endpoint(
    resume: UploadFile = File(..., description="Resume file (PDF or text)"),
    job_description: str = Form(..., description="Job description text"),
    target_skills: List[str] = Form(None, description="Array list of target skills")
) -> ResumeScoringResponse:
    """
    Score a resume against a job description and target skills.
    
    Args:
        resume: PDF or text file containing the resume
        job_description: Text description of the job requirements
        target_skills: Array list of skills to check for
    
    Returns:
        Detailed scoring results including skills match, experience score, education score, and overall assessment
    """
    try:
        # Validate file type
        if not resume.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        allowed_extensions = ['.pdf', '.txt']
        file_extension = os.path.splitext(resume.filename)[1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Validate file size (10MB limit)
        content = await resume.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")
        
    
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Score the resume
            result = await score_resume(temp_path, job_description, target_skills)
            
            return ResumeScoringResponse(
                success=True,
                data=result,
                message="Resume scored successfully"
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except HTTPException:
        raise
    except Exception as e:
        return ResumeScoringResponse(
            success=False,
            error=str(e),
            message="Failed to score resume"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "resume-scoring-api"}


@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Resume Scoring API",
        "version": "1.0.0",
        "endpoints": {
            "score_resume": "/events/score-resume",
            "health": "/events/health",
            "docs": "/docs"
        }
    }

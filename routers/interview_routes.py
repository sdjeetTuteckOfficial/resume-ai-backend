from fastapi import APIRouter, Depends
from schemas.interview_schema import GapAnalysisResponse
from services.gap_analysis_service import GapAnalysisService
from utils.dependencies import DBSession, CurrentUser # Assuming your auth deps exist

router = APIRouter()

@router.post(
    "/analyze-gap",
    response_model=GapAnalysisResponse,
    summary="Generate gap analysis for Job ID JOB26783"
)
async def generate_gap_analysis(
    db: DBSession,
    current_user: CurrentUser 
):
    """
    Analyzes the logged-in user's CV against the hardcoded Job Description (JOB26783).
    """
    
    # Authenticated User ID from Token
    user_id = current_user.id

    return await GapAnalysisService.analyze_gap(
        db=db,
        user_id=user_id
    )
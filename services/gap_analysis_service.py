import io
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Import Config to access the API Key reliably
from config import settings 

# Import models and schemas
from models.user_details import UserDetails 
from models.job_model import TJobDetails 
from schemas.interview_schema import GapAnalysisResponse

class GapAnalysisService:

    @staticmethod
    def _extract_text_from_blob(file_data: bytes) -> str:
        """
        Converts the raw Postgres BYTEA (blob) data into readable string text.
        """
        try:
            stream = io.BytesIO(file_data)
            reader = PdfReader(stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or "" + "\n"
            return text
        except Exception as e:
            # Log this error in a real production app
            print(f"PDF Extraction Error: {e}") 
            return "" 

    @staticmethod
    async def analyze_gap(db: Session, user_id: int) -> GapAnalysisResponse:
        """
        Orchestrates the Gap Analysis.
        Args:
            db: Database session
            user_id: TRUSTED user_id passed from the controller (extracted from Token)
        """
        
        # ---------------------------------------------------------
        # STEP 1: Get User Details (To find the Job ID & CV)
        # ---------------------------------------------------------
        user_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User profile not found."
            )

        if not user_details.job_id:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No Job selected. Please update your profile with a valid Job ID."
            )

        if not user_details.cv_file_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No CV file found in user profile. Please upload a CV first."
            )

        # ---------------------------------------------------------
        # STEP 2: Fetch Job Description using user_details.job_id
        # ---------------------------------------------------------
        # Using TJobDetails.id (Integer Primary Key)
        job_record = db.query(TJobDetails).filter(TJobDetails.id == user_details.job_id).first()
        
        if not job_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration Error: The Job (ID: {user_details.job_id}) associated with this user was not found."
            )
            
        job_description_text = job_record.job_details
        
        # --- DEBUG PRINT ---
        print("\n========== JOB DESCRIPTION ==========")
        print(job_description_text)
        print("=====================================\n")

        # ---------------------------------------------------------
        # STEP 3: Extract Text from the Blob
        # ---------------------------------------------------------
        cv_text = GapAnalysisService._extract_text_from_blob(user_details.cv_file_data)
        
        # --- DEBUG PRINT ---
        print("\n========== CV TEXT ==========")
        print(cv_text)
        print("=============================\n")

        if len(cv_text.strip()) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="The uploaded CV seems empty or unreadable."
            )

        # ---------------------------------------------------------
        # STEP 4: Gemini / LangChain Call
        # ---------------------------------------------------------
        # Use settings.google_api_key instead of os.getenv
        if not settings.google_api_key:
            raise HTTPException(status_code=500, detail="Google API Key configuration missing.")

        # Pass the API key explicitly to the library
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.2,
            google_api_key=settings.google_api_key
        )
        
        # Enforce the Pydantic Schema structure
        structured_llm = llm.with_structured_output(GapAnalysisResponse)

        system_prompt = """
        You are an expert Technical Recruiter.
        Analyze the Candidate's CV against the Job Description.
        
        1. Identify CRITICAL GAPS (missing skills, lack of experience depth).
        2. Generate 20 screening questions. 
           - If they lack a skill (e.g., Docker), ask a conceptual question about it.
           - If they have a skill, ask a scenario-based question to test depth.
        3. Return STRICT JSON matching the schema provided.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "JOB DESCRIPTION:\n{job_desc}\n\nCANDIDATE CV CONTENT:\n{cv_text}")
        ])

        chain = prompt | structured_llm
        
        try:
            result = await chain.ainvoke({
                "job_desc": job_description_text,
                "cv_text": cv_text
            })
            return result
        except Exception as e:
            print(f"AI Generation Error: {e}")
            raise HTTPException(status_code=500, detail="Error generating interview questions.")
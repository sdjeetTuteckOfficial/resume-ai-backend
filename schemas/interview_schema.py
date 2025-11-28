from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# 1. Validation Logic for the Frontend
class ValidationRule(BaseModel):
    required: bool = Field(description="Is this field mandatory?")
    minLength: Optional[int] = Field(None, description="Minimum character count for text answers")

# 2. Structure of a Single Question
class DynamicQuestion(BaseModel):
    id: str = Field(description="Unique key for the form field (e.g., 'q_react_experience')")
    question: str = Field(description="The question text to display to the user")
    type: Literal['text', 'textarea', 'radio', 'select'] = Field(description="Input type")
    options: Optional[List[str]] = Field(None, description="Options if type is radio or select")
    validation: ValidationRule = Field(description="Validation rules for Yup schema")
    placeholder: Optional[str] = Field(None, description="Placeholder text")

# 3. The Full Response Object
class GapAnalysisResponse(BaseModel):
    analysis_summary: str = Field(description="A brief summary of skill gaps found in the CV")
    questions: List[DynamicQuestion] = Field(description="List of dynamic questions to generate")

# 4. Request Body
class GapAnalysisRequest(BaseModel):
    user_id: int
    job_role_description: str
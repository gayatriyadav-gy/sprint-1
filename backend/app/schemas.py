from pydantic import BaseModel, EmailStr

# ==========================================
# DAY 2: AUTHENTICATION SCHEMAS
# ==========================================

# User Sign-up ke waqt jo data bhejega
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User Login ke waqt jo data bhejega
class StudentLogin(BaseModel):
    email: EmailStr
    password: str

# API response mein user ko kya dikhana hai
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ==========================================
# DAY 3: QUIZ SYSTEM SCHEMAS
# ==========================================

# Quiz Question Response Schema
class QuizQuestionResponse(BaseModel):
    id: int
    category: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True

# Student Quiz Submission Schema
class QuizSubmission(BaseModel):
    answers: dict  # Format: {"1": "A", "2": "C"}


# ==========================================
# DAY 4: LEARNING ANALYTICS DASHBOARD SCHEMAS
# ==========================================

class DashboardAnalyticsResponse(BaseModel):
    student_name: str
    career_goal: str | None
    industry_readiness_score: float
    is_verified: int
    recent_quiz_performance: dict

    class Config:
        from_attributes = True
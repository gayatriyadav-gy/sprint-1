from pydantic import BaseModel, EmailStr

# ==========================================
# DAY 2: AUTHENTICATION SCHEMAS
# ==========================================

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ==========================================
# DAY 3: QUIZ SYSTEM SCHEMAS
# ==========================================

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
    gamification_metrics: dict
    industry_insights: dict

    class Config:
        from_attributes = True


# ==========================================
# DAY 5: ACTION PLAN RESPONSE SCHEMA
# ==========================================

class ActionPlanResponse(BaseModel):
    student_name: str
    analysis_summary: str
    identified_gap_domain: str
    personalized_action_plan: dict
    system_status: str

    class Config:
        from_attributes = True
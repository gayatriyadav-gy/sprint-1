from pydantic import BaseModel, EmailStr

<<<<<<< HEAD
# ==========================================
# DAY 2: AUTHENTICATION SCHEMAS
# ==========================================

=======
>>>>>>> 96033feebbe1fb936fbd700b3c1335684e58d1d8
# User Sign-up ke waqt jo data bhejega
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User Login ke waqt jo data bhejega
class StudentLogin(BaseModel):
    email: EmailStr
    password: str

<<<<<<< HEAD
# API response mein user ko kya dikhana hai
=======
# API response mein user ko kya dikhana hai (Password hide karne ke liye)
>>>>>>> 96033feebbe1fb936fbd700b3c1335684e58d1d8
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
<<<<<<< HEAD
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
    answers: dict  # Example format: {"1": "A", "2": "C"}
=======
        from_attributes = True
>>>>>>> 96033feebbe1fb936fbd700b3c1335684e58d1d8

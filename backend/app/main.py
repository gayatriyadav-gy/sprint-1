from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, schemas

# Official Project Title Configuration
app = FastAPI(
    title="SkillSync: Intelligent Career Mentor & Learning Analytics Platform", 
    version="1.0"
)

# Startup event to automatically create MySQL tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ==========================================
# DAY 1: CORE ENGINE & WELCOME ENDPOINTS
# ==========================================

@app.get("/")
def read_root():
    return {"message": "Welcome to SkillSync Engine! Backend Server is Live."}

@app.get("/api/db-check")
def check_db_status(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "success", "database": "Connected Successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# DAY 2: AUTHENTICATION (SIGN-UP & LOGIN)
# ==========================================

@app.post("/api/auth/signup", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def signup_student(student_data: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.Student).filter(models.Student.email == student_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered!"
        )
    
    new_student = models.Student(
        name=student_data.name,
        email=student_data.email,
        password=student_data.password  
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post("/api/auth/login")
def login_student(login_data: schemas.StudentLogin, db: Session = Depends(get_db)):
    user = db.query(models.Student).filter(models.Student.email == login_data.email).first()
    
    if not user or user.password != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password!"
        )
        
    return {
        "status": "success",
        "message": "Login Successful!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

# ==========================================
# DAY 3: QUIZ & CREATIVE CAREER MENTORSHIP
# ==========================================

@app.get("/api/quiz/questions", response_model=list[schemas.QuizQuestionResponse])
def get_quiz_questions(db: Session = Depends(get_db)):
    # Database se saare questions fetch karega
    questions = db.query(models.QuizQuestion).all()
    return questions

@app.post("/api/quiz/submit")
def submit_quiz(submission: schemas.QuizSubmission, db: Session = Depends(get_db)):
    user_answers = submission.answers
    
    # Category wise score counter
    category_scores = {
        "Web Development": 0,
        "Backend & Databases": 0,
        "Data Science & AI": 0,
        "Cloud & DevOps": 0
    }
    
    total_questions = 0
    correct_answers = 0
    
    for q_id, selected_option in user_answers.items():
        question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == int(q_id)).first()
        if question:
            total_questions += 1
            if question.correct_answer.strip().upper() == selected_option.strip().upper():
                correct_answers += 1
                if question.category in category_scores:
                    category_scores[question.category] += 1
                    
    # Creative Highest Domain Recommendation Logic
    best_category = max(category_scores, key=category_scores.get)
    
    career_mapping = {
        "Web Development": "Frontend Engineer / UI-UX Developer",
        "Backend & Databases": "Backend Engineer / Database Administrator",
        "Data Science & AI": "Data Scientist / Machine Learning Engineer",
        "Cloud & DevOps": "DevOps Cloud Engineer / System Architect"
    }
    
    if correct_answers == 0:
        recommended_career = "IT Business Analyst / Tech Consultant"
    else:
        recommended_career = career_mapping.get(best_category, "Full-Stack Software Engineer")
        
    readiness_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
    return {
        "status": "Success",
        "message": "Intelligent Analytics Generated Successfully!",
        "metrics": {
            "total_questions_attempted": total_questions,
            "total_correct": correct_answers,
            "industry_readiness_score": f"{round(readiness_percentage, 2)}%"
        },
        "category_breakdown": category_scores,
        "recommended_career_path": recommended_career,
        "next_learning_step": f"Focus on core concepts of {best_category} to boost your profile."
    }
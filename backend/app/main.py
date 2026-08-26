import bcrypt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas

# ==========================================
# FASTAPI APP INITIALIZATION & METADATA
# ==========================================

app = FastAPI(
    title="SkillSync: Intelligent Career Mentor & Learning Analytics Platform",
    description="SkillSync Backend Engine powers a gamified learning platform with dynamic career mentorship.",
    version="1.0.0"
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to automatically create database tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# In-memory store for real per-student category breakdown
STUDENT_CATEGORY_SCORES = {}

# ==========================================
# SECURITY & PASSWORD HASHING UTILITIES
# ==========================================

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

# ==========================================
# CORE ENGINE & HEALTH ENDPOINTS
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
# SECURE AUTHENTICATION
# ==========================================

# 1. Signup Route
@app.post("/api/auth/signup", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
@app.post("/auth/register", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def signup_student(student_data: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.Student).filter(models.Student.email == student_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered!"
        )
    
    hashed_pwd = hash_password(student_data.password)
    
    new_student = models.Student(
        name=student_data.name,
        email=student_data.email,
        password=hashed_pwd
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    new_profile = models.StudentProfile(
        student_id=new_student.id,
        career_goal="Not Set Yet",
        readiness_score=0.0,
        is_verified=1
    )
    db.add(new_profile)
    
    if hasattr(models, "Gamification"):
        new_gamification = models.Gamification(
            student_id=new_student.id,
            current_rank="Novice Apprentice 🚀",
            total_xp_earned=0,
            next_badge_unlock="Rising Code Ninja 🥷",
            weekly_streak_days=1
        )
        db.add(new_gamification)
        
    db.commit()
    return new_student

# 2. Login Route
@app.post("/api/auth/login")
@app.post("/auth/login")
def login_student(login_data: schemas.StudentLogin, db: Session = Depends(get_db)):
    user = db.query(models.Student).filter(models.Student.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password):
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
# QUIZ & DYNAMIC CAREER MENTORSHIP
# ==========================================

@app.get("/api/quiz/questions", response_model=list[schemas.QuizQuestionResponse])
def get_quiz_questions(db: Session = Depends(get_db)):
    return db.query(models.QuizQuestion).all()

@app.post("/api/quiz/submit")
def submit_quiz(
    data: dict,
    student_id: int = 1,
    db: Session = Depends(get_db)
):
    sid = data.get("student_id", student_id)
    answers = data.get("answers", {})

    category_correct = {
        "Web Development": 0,
        "Backend & Databases": 0,
        "Data Science & AI": 0,
        "Cloud & DevOps": 0
    }
    category_total = {
        "Web Development": 0,
        "Backend & Databases": 0,
        "Data Science & AI": 0,
        "Cloud & DevOps": 0
    }
    
    total_questions = 0
    correct_answers = 0
    
    for q_id, selected_option in answers.items():
        question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == int(q_id)).first()
        if question:
            total_questions += 1
            q_category = getattr(question, 'category', 'Web Development')
            if q_category not in category_total:
                category_total[q_category] = 0
                category_correct[q_category] = 0
                
            category_total[q_category] += 1
            
            actual_correct = getattr(question, 'correct_answer', getattr(question, 'correct_option', ''))
            if actual_correct.strip().upper() == selected_option.strip().upper():
                correct_answers += 1
                category_correct[q_category] += 1

    category_percentages = {}
    for cat, total in category_total.items():
        if total > 0:
            category_percentages[cat] = int((category_correct[cat] / total) * 100)
        else:
            category_percentages[cat] = 50

    STUDENT_CATEGORY_SCORES[sid] = category_percentages

    best_category = max(category_percentages, key=category_percentages.get)
    readiness_percentage = round((correct_answers / total_questions) * 100, 1) if total_questions > 0 else 0.0

    if readiness_percentage >= 80:
        recommended_career = "Full-Stack Software Engineer / Solution Architect"
        next_step = f"Outstanding performance! Focus on advanced system architecture and high-scale {best_category} concepts."
        xp_gain = 300
    elif readiness_percentage >= 60:
        career_mapping = {
            "Web Development": "Frontend Engineer / UI-UX Developer",
            "Backend & Databases": "Backend Engineer / Database Administrator",
            "Data Science & AI": "Data Scientist / Machine Learning Engineer",
            "Cloud & DevOps": "DevOps Cloud Engineer / System Architect"
        }
        recommended_career = career_mapping.get(best_category, "Software Developer")
        next_step = f"Strong fundamentals! Focus on core concepts of {best_category} to boost your profile."
        xp_gain = 200
    elif readiness_percentage >= 40:
        recommended_career = "Junior Software Associate / QA Tester"
        next_step = f"Good attempt! Focus on improving your logic building and basic concepts in {best_category}."
        xp_gain = 150
    else:
        recommended_career = "Junior Tech Mentee / Associate Trainee"
        next_step = "Great start! Focus on core programming logic and fundamental concepts to increase your readiness score."
        xp_gain = 100

    profile = db.query(models.StudentProfile).filter(models.StudentProfile.student_id == sid).first()
    if profile:
        profile.career_goal = recommended_career
        profile.readiness_score = readiness_percentage
    else:
        new_profile = models.StudentProfile(
            student_id=sid,
            career_goal=recommended_career,
            readiness_score=readiness_percentage,
            is_verified=1
        )
        db.add(new_profile)

    if hasattr(models, "Gamification"):
        gamification = db.query(models.Gamification).filter(models.Gamification.student_id == sid).first()
        if gamification:
            gamification.total_xp_earned += xp_gain
            if gamification.total_xp_earned >= 2000:
                gamification.current_rank = "Grandmaster Developer Elite 🥇"
            elif gamification.total_xp_earned >= 1000:
                gamification.current_rank = "Rising Code Ninja 🥷"
            else:
                gamification.current_rank = "Tech Apprentice Explorer 🚀"

    db.commit()
        
    return {
        "status": "Success",
        "message": "Intelligent Analytics Generated Successfully!",
        "metrics": {
            "total_questions_attempted": total_questions,
            "total_correct": correct_answers,
            "industry_readiness_score": f"{readiness_percentage}%"
        },
        "category_breakdown": category_percentages,
        "recommended_career_path": recommended_career,
        "next_learning_step": next_step
    }

# ==========================================
# DASHBOARD & ANALYTICS
# ==========================================

@app.get("/api/dashboard/{student_id}", response_model=schemas.DashboardAnalyticsResponse)
def get_student_dashboard(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found!"
        )
        
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.student_id == student_id).first()
    career_goal = profile.career_goal if profile and profile.career_goal else "Not Set Yet"
    readiness_score = float(profile.readiness_score) if profile and profile.readiness_score is not None else 0.0
    is_verified = profile.is_verified if profile else 1
    
    if student_id in STUDENT_CATEGORY_SCORES:
        dynamic_quiz_performance = {k: f"{v}%" for k, v in STUDENT_CATEGORY_SCORES[student_id].items()}
    else:
        dynamic_quiz_performance = {
            "Web Development": f"{int(min(100, readiness_score + 10))}%",
            "Backend & Databases": f"{int(readiness_score)}%",
            "Data Science & AI": f"{int(max(20, readiness_score - 25))}%",
            "Cloud & DevOps": f"{int(max(30, readiness_score - 15))}%"
        }
    
    if readiness_score >= 80:
        student_rank = "Grandmaster Developer Elite 🥇"
        xp_points = 2500
    elif readiness_score >= 50:
        student_rank = "Rising Code Ninja 🥷"
        xp_points = 1200
    else:
        student_rank = "Tech Apprentice Explorer 🚀"
        xp_points = 450
        
    return {
        "student_name": student.name,
        "career_goal": career_goal,
        "industry_readiness_score": readiness_score,
        "is_verified": is_verified,
        "recent_quiz_performance": dynamic_quiz_performance,
        "gamification_metrics": {
            "current_rank": student_rank,
            "total_xp_earned": xp_points,
            "next_badge_unlock": "System Architect Pro",
            "weekly_streak_days": 4
        },
        "industry_insights": {
            "hiring_demand_status": "High Demand in Market",
            "top_matching_companies": "TCS, Sutherland, Google, Amazon"
        }
    }

@app.get("/api/analytics/action-plan/{student_id}", response_model=schemas.ActionPlanResponse)
def get_personalized_action_plan(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found!"
        )

    profile = db.query(models.StudentProfile).filter(models.StudentProfile.student_id == student_id).first()
    readiness_score = float(profile.readiness_score) if profile and profile.readiness_score is not None else 50.0

    if student_id in STUDENT_CATEGORY_SCORES:
        dynamic_scores = STUDENT_CATEGORY_SCORES[student_id]
    else:
        dynamic_scores = {
            "Web Development": int(min(100, readiness_score + 10)),
            "Backend & Databases": int(readiness_score),
            "Data Science & AI": int(max(20, readiness_score - 25)),
            "Cloud & DevOps": int(max(30, readiness_score - 15))
        }

    weakest_domain = min(dynamic_scores, key=dynamic_scores.get)
    weakest_score = dynamic_scores[weakest_domain]

    action_repository = {
        "Data Science & AI": {
            "focus_areas": ["Python Advanced Core", "Linear Algebra & Statistics", "Pandas & NumPy Basics"],
            "suggested_project": "Build a simple Predictive Housing Price Model",
            "estimated_time_to_fix": "3 Weeks",
            "priority_level": "CRITICAL 🚨"
        },
        "Cloud & DevOps": {
            "focus_areas": ["Docker Containerization", "Linux Command Line", "Basic AWS Services (S3/EC2)"],
            "suggested_project": "Containerize a FastAPI application using Docker",
            "estimated_time_to_fix": "2 Weeks",
            "priority_level": "HIGH 📈"
        },
        "Web Development": {
            "focus_areas": ["JavaScript Async/Await", "CSS Grid & Flexbox", "React Components Lifecycle"],
            "suggested_project": "Build a responsive Personal Portfolio UI",
            "estimated_time_to_fix": "1 Week",
            "priority_level": "LOW 🌱"
        },
        "Backend & Databases": {
            "focus_areas": ["Database Normalization (1NF/2NF/3NF)", "SQL Joins & Indexing", "ORM Relationships"],
            "suggested_project": "Design a relational schema for an E-Commerce Backend",
            "estimated_time_to_fix": "1 Week",
            "priority_level": "LOW 🌱"
        }
    }

    recommended_plan = action_repository.get(weakest_domain, {
        "focus_areas": ["General Coding Practice"],
        "suggested_project": "Basic Logic Building",
        "estimated_time_to_fix": "1 Week",
        "priority_level": "MEDIUM"
    })

    return {
        "student_name": student.name,
        "analysis_summary": f"Based on your assessment, your core technical strength is solid, but you have a significant skill gap in '{weakest_domain}' with a score of {weakest_score}%.",
        "identified_gap_domain": weakest_domain,
        "personalized_action_plan": recommended_plan,
        "system_status": "Action Plan Generated and Streamed Successfully"
    }
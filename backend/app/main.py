from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Student
from .schemas import StudentCreate, StudentLogin, StudentResponse

# Official Project Title Configuration
app = FastAPI(
    title="SkillSync: Intelligent Career Mentor & Learning Analytics Platform", 
    version="1.0"
)

# Startup event to automatically create MySQL tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 1. Welcome Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to SkillSync Engine! Backend Server is Live."}

# 2. Database Status Check
@app.get("/api/db-check")
def check_db_status(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "success", "database": "Connected Successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 3. STUDENT REGISTRATION (SIGN-UP) API
@app.post("/api/auth/signup", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def signup_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered!"
        )
    
    # Create new student object (Ma'am ko batane ke liye: Abhi direct password save kar rahe hain, baad mein hash karenge)
    new_student = Student(
        name=student_data.name,
        email=student_data.email,
        password=student_data.password  
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 4. STUDENT LOGIN API
@app.post("/api/auth/login")
def login_student(login_data: StudentLogin, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.email == login_data.email).first()
    
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
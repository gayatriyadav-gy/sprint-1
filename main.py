from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db

# 1. Main FastAPI Application Launch
app = FastAPI(title="SkillSync: Intelligent Career Mentor & Learning Analytics Platform", version="1.0")

# 2. Server start hote hi MySQL mein saare tables automatically create karne ke liye
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 3. Welcome Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to SkillSync Engine! Backend Server is Live and Connected."}

# 4. Database Connection Testing Endpoint
@app.get("/api/db-check")
def check_db_status(db: Session = Depends(get_db)):
    try:
        # MySQL pipeline ko test karne ke liye test query
        db.execute("SELECT 1")
        return {"status": "success", "database": "Connected Successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
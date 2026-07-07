from sqlalchemy import Column, Integer, String, Decimal, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

# 1. Students Master Table Model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    profile = relationship("StudentProfile", back_populates="student", uselist=False)

# 2. Career Profile & Image Logs Model
class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True)
    career_goal = Column(String(100), nullable=True)
    cgpa = Column(Decimal(4, 2), nullable=True)
    readiness_score = Column(Integer, default=0)
    profile_image_path = Column(String(255), nullable=True)
    image_verification_status = Column(String(50), default="Pending")

    student = relationship("Student", back_populates="profile")

# 3. Dynamic Question Bank Model
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject = Column(String(50), nullable=False, index=True) 
    question_text = Column(String(500), nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    correct_option = Column(String(1), nullable=False)
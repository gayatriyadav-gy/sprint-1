from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True)
    career_goal = Column(String(255), nullable=True)
    cgpa = Column(Numeric(4, 2), nullable=True)
    readiness_score = Column(Numeric(5, 2), default=0.0)
    is_verified = Column(Integer, default=0)

    student = relationship("Student", back_populates="profile")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    question_text = Column(String(500), nullable=False)
    option_a = Column(String(205), nullable=False)
    option_b = Column(String(205), nullable=False)
    option_c = Column(String(205), nullable=False)
    option_d = Column(String(205), nullable=False)
    correct_answer = Column(String(5), nullable=False)

# Relationships update
Student.profile = relationship("StudentProfile", uselist=False, back_populates="student")
from pydantic import BaseModel, EmailStr

# User Sign-up ke waqt jo data bhejega
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User Login ke waqt jo data bhejega
class StudentLogin(BaseModel):
    email: EmailStr
    password: str

# API response mein user ko kya dikhana hai (Password hide karne ke liye)
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
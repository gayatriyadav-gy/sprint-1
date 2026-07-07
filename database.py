from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. MySQL Database Connection URL
# Note: replace 'your_password' with your actual MySQL Workbench password
DATABASE_URL = "mysql+pymysql://root:gayatri@localhost:3306/skillsync_db"

# 2. Database Engine create karna
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 3. Database Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base Class mapping ke liye
Base = declarative_base()

# 5. Dependency injection function connection close karne ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
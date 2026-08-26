from database import engine, SessionLocal, Base
import models

# Recreate tables or use existing
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear old duplicate questions
db.query(models.QuizQuestion).delete()

fresh_questions = [
    # 1. Web Development
    models.QuizQuestion(
        question_text="Which HTML5 tag is standard for playing video files directly in browser?",
        option_a="&lt;video&gt;",
        option_b="&lt;movie&gt;",
        option_c="&lt;media&gt;",
        option_d="&lt;embed-video&gt;",
        correct_answer="A",
        category="Web Development"
    ),
    models.QuizQuestion(
        question_text="Which CSS property is used to create modern flexible responsive layouts?",
        option_a="float",
        option_b="display: flex",
        option_c="align: center",
        option_d="clear: both",
        correct_answer="B",
        category="Web Development"
    ),

    # 2. Backend & Databases
    models.QuizQuestion(
        question_text="Which FastAPI decorator is used to handle a HTTP POST endpoint?",
        option_a="@app.get()",
        option_b="@app.route()",
        option_c="@app.post()",
        option_d="@app.put()",
        correct_answer="C",
        category="Backend & Databases"
    ),
    models.QuizQuestion(
        question_text="Which SQL clause is used to filter aggregated group records?",
        option_a="WHERE",
        option_b="HAVING",
        option_c="ORDER BY",
        option_d="LIMIT",
        correct_answer="B",
        category="Backend & Databases"
    ),

    # 3. Data Science & AI
    models.QuizQuestion(
        question_text="Which Python library is primarily used for tabular data manipulation and DataFrame structures?",
        option_a="Pandas",
        option_b="Flask",
        option_c="Requests",
        option_d="Pygame",
        correct_answer="A",
        category="Data Science & AI"
    ),
    models.QuizQuestion(
        question_text="Which evaluation metric measures the proportion of correctly predicted positive observations?",
        option_a="Precision",
        option_b="Entropy",
        option_c="Standard Deviation",
        option_d="Variance",
        correct_answer="A",
        category="Data Science & AI"
    ),

    # 4. Cloud & DevOps
    models.QuizQuestion(
        question_text="What core technology does Docker utilize to build lightweight isolated application packages?",
        option_a="Virtual Machines",
        option_b="Containers",
        option_c="Hypervisors",
        option_d="Kernel Drivers",
        correct_answer="B",
        category="Cloud & DevOps"
    ),
    models.QuizQuestion(
        question_text="Which tool is standard for container orchestration and automated deployment scaling?",
        option_a="Kubernetes",
        option_b="Nginx",
        option_c="Postman",
        option_d="Git",
        correct_answer="A",
        category="Cloud & DevOps"
    )
]

for q in fresh_questions:
    db.add(q)

db.commit()
db.close()
print("✅ Quiz Questions refreshed successfully with all 4 technical domains!")
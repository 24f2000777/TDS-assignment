from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List, Optional

app = FastAPI(title="Students API")

# Allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the CSV once at startup
STUDENTS = []
with open("students.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        STUDENTS.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })

@app.get("/api")
def get_students(classes: Optional[List[str]] = Query(None, alias="class")):
    """
    - /api               -> all students
    - /api?class=1A      -> only class 1A
    - /api?class=1A&class=1B -> classes 1A and 1B
    """
    if not classes:
        return {"students": STUDENTS}
    wanted = set(classes)
    return {"students": [s for s in STUDENTS if s["class"] in wanted]}

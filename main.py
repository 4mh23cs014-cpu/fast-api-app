from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Simple in-memory database
students_db = {}

class student(BaseModel):
    name: str
    email: str
    roll_number: int 
    department: str

class studentsResponse(BaseModel):
    id: int
    name: str
    email: str
    roll_number: int 
    department: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/students", response_model=studentsResponse)
def create_student(new_student: student):
    # Generate a simple ID
    student_id = len(students_db) + 1
    students_db[student_id] = new_student.dict()
    return studentsResponse(id=student_id, **new_student.dict())

@app.get("/students/{student_id}", response_model=studentsResponse)
def read_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = students_db[student_id]
    return studentsResponse(id=student_id, **student_data)

@app.put("/students/{student_id}", response_model=studentsResponse)
def update_student(student_id: int, updated_student: student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db[student_id] = updated_student.dict()
    return studentsResponse(id=student_id, **updated_student.dict())

@app.delete("/students/{student_id}", response_model=studentsResponse)
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = students_db.pop(student_id)
    return studentsResponse(id=student_id, **student_data)
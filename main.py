from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import students_collection



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["http://localhost:5173"]
)

class Student(BaseModel):
    rollno:int
    name: str
    age: int
    branch:str

students = [
    {
        "rollno": 101,
        "name": "Rahul",
        "age": 21,
        "branch": "CSE"
    },
    {
        "rollno": 102,
        "name": "Priya",
        "age": 20,
        "branch": "ECE"
    }
]


@app.get("/test-db")
async def test_db():
    await students_collection.database.command("ping")
    return {"message": "MongoDB connected successfully"}



@app.get("/")
def home():
    return {
        "message":"hello farm stack"
    }


@app.get("/students")
async def get_students():
    students = await students_collection.find(
        {},
        {"_id":0}
    ).to_list(length=None)
    
    return students


@app.get("/students/rollno/{rollno}")
async def get_students_by_roll_no(rollno:int):
        student = await students_collection.find_one(
             {"rollno":rollno},
             {"_id":0}
        )
        if student is None:
             return {"message":"data not found"}

        return student

@app.get("/students/branch/{branch}")
def get_Students_by_branch(branch:str):
    result = []
    for student in students:
        if student["branch"]==branch:
            result.append(student)

    return result



@app.post("/students")
async def create(student:Student):
    student_data = student.model_dump()
    await students_collection.insert_one(student_data)
    return student


@app.put("/students/{rollno}")
async def update(rollno:int,student:Student):
    student_data = student.model_dump()
    result = await students_collection.update_one(
        {"rollno":rollno},
        {"$set":student_data}
    )
    if result.matched_count ==0:
        return {"message":"no data found"}

    return {"meassage": "data updated successfully"}
        


@app.delete("/students/{rollno}")
async def delete(rollno:int):

    result = await students_collection.delete_one(
        {"rollno":rollno}

    )
    if result.deleted_count==0:
        return {"message":"data not found"}

    return {"message": "data deleted successfully"}

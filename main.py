from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI()

"""
HTTP Method:
1.GET -> to just show the message on the website or the page or on the application 
"""

@app.get('/') #Endpoint -> where on the url the below message must be displayed
def greet():
    return {"Hello and welcome to fastapi"}

@app.get('/hello')
def hello():
    return {"this is hello page"}

#helper function
def load_data():
    with open("students.json",'r') as file:
        return json.load(file)

@app.get('/student')
def student():
    return load_data()

#student_id -> This is the path parameter.
@app.get("/students/{student_id}") #/student/S001
def get_id(student_id:str=Path(...,description="The Id of the student",examples=['S001'])):#student_id = S001
    data = load_data()
    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with Id '{student_id}' not found")
    
    return data[student_id]#data[S001]

'''
http://127.0.0.1:8000/filter?course=Python
? -> after this our query is present
Course=Python -> this is key-value pair
'''

@app.get('/filter')
def filter_student(course : str = Query(None,description="Show only students in this course",examples=["Python"])): 
    data = load_data()

    if course is None:
        return data

    filtered ={}
    for student_id , info in data.items():
        if info["course"].lower == course.lower:
            filtered[student_id] = info
    return filtered

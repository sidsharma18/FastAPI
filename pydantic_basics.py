"""
PYDANTIC FUNDAMENTALS
"""

"""
STEP 1- The Problem
A normal dictionary accept anything . Nobody checks the data.
"""
bad_student = {"name": "", "age": "Twenty", "marks": 160, "email": "not-an-email"}
# print(bad_student)


from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field

"""
Step 2 - BASEMODEL + TYPE HINTS
We describe a student once. python checks every student against it.
"""


# class SimpleStudent(BaseModel):  # Pydantic model
#     name: str
#     age: int
#     marks: int


# s = SimpleStudent(name="Arav", age=20, marks=80)
# print(s.name, s.age, s.marks)


"""
Step 3 - FIELD() RULES
gt = greater than            lt = less than
ge = greater pr equal        le = less or equal
"""


class RuleStudent(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)  # ... = required
    age: int = Field(..., gt=0, lt=100)  # 1 to 99
    marks: int = Field(..., gt=0, lt=100)  # 0 to 100
    course: str = "Python"  # default value -> Python
    phone: str | None = None  # optional field can be empty


s = RuleStudent(name="sid", age=21, marks=77)
# print(s.name, s.age, s.marks, s.course, s.phone)


"""
Step 4 - EMAILSTR
checks the text really look like an email
"""


class EmailStudents(BaseModel):
    name: str
    email: EmailStr


s = EmailStudents(name="kabir", email="kabirsingh@gmail.com")
# print(s.name, s.email)


"""
Step 5 - FINAL STUDENT MODEL
1. field validator -> our own custom rule.
2. Computed_field -> a value Pydantic calculates for us.
"""


class Student(BaseModel):
    id: str = Field(..., examples=["S001"])
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, le=100)
    course: str = Field(..., max_length=50)
    marks: int = Field(..., ge=0, le=100)
    email: EmailStr

    # Custom Rule : name must contain only letters and spaces

    @field_validator("name")
    @classmethod
    def check_name(cls, value):  # value ="name"
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name Must Contain Only letters and spaces")
        return value.title()

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "Fail"


s = Student(
    id="S001",
    name="sid sharma",
    age=21,
    course="Python",
    marks=88,
    email="arav@gmail.com",
)
# print(s.id, s.name, s.age, s.course, s.marks, s.email)
# print(s.grade)


"""
Step 6. MODEL_DUMP()
turn a model back into python dictionay (so that we can save it later)
"""

data = s.model_dump()
# print(data)

import json

"""
Step 7. Chcek our real data (students.json)
Every in our will go through the student model
"""
with open("students.json", "r") as file:
    raw = json.load(file)

for student_id, info in raw.items():
    s = Student(id=student_id, **info)
    print(s.id, s.name, s.grade, s.email)

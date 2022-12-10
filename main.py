# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path



app = FastAPI()


# Models

class Location(BaseModel):
    city : str
    state : str
    country : str 
    
    

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None
    


@app.get('/')
def home():
    return {'Hello': 'World'}


# Request and Response Body

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person


# Validations: Query Parameters

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None,
        min_length = 1,
        max_length = 50,
        title = 'Person Name',
        description = 'This is the person name. It"s between 1 and 50 characters'
        ),
    age: int = Query(
        ...,
        title = 'Person Age',
        description = 'This is the person name. It"s is required'
        )
):
    return {name: age}


# Validations Path Parameter

@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,    
        title = 'Person Id',
        description = 'This is the person Id. It"s between 1 and 50 numbers characters, and it"s required',        
        gt = 0
        )
):
    return {person_id: 'It exists!'}


# Validations: Request Body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title = 'Person ID',
        description = 'This is the person ID',
        gt = 0
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = dict(person)
    result.update(dict(location))

    return result
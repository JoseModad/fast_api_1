# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr
from pydantic import AnyUrl

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path



app = FastAPI()


# Models

class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'
    

class Location(BaseModel):
    city : str = Field(
        ..., 
        min_length = 1, 
        max_length = 30
        )
    state : str = Field(
        ..., 
        min_length = 1, 
        max_length = 30
        )
    country : str = Field(
        ..., 
        min_length = 1, 
        max_length = 30
        )
    
    class Config:
        schema_extra = {
            'example': {                
                'city': 'Capital',
                'state': 'Salta',
                'country': 'Argentina'
            }
        }
        
    

class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length = 1, 
        max_length = 50
        )
    last_name: str = Field(
        ..., 
        min_length = 1, 
        max_length = 50
        )
    age: int = Field(
        ...,
        gt = 0,
        le = 115        
    )
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)
    email: Optional[EmailStr] = Field(default = None)
    url_cliente: Optional[AnyUrl] = Field(default = None)
    
    class Config:
        schema_extra = {
            'example': {                
                'first_name': 'Erika',
                'last_name': 'Alvarez',
                'age': 17,
                'hair_color': 'brown',
                'is_married': False,
                'email': 'turko@gmail.com',
                'url_client': 'https://platzi.com'
            }
        }


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
        description = 'This is the person name. It"s between 1 and 50 characters',
        example = 'Rocio'
        ),
    age: int = Query(
        ...,
        title = 'Person Age',
        description = 'This is the person name. It"s is required',
        example = 25
        
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
        gt = 0,
        example = 23
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
        gt = 0,
        example = 23
        ),
    person: Person = Body(...,),
    location: Location = Body(...)
):
    result = dict(person)
    result.update(dict(location))

    return result    
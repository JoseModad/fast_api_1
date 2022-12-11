# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr
from pydantic import AnyUrl

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File



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

        
    
class PersonBase(BaseModel):
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
    
    hair_color : Optional[HairColor] = Field(default = None)
    is_married : Optional[bool] = Field(default = None)
    email : Optional[EmailStr] = Field(default = None)
    url_cliente : Optional[AnyUrl] = Field(default = None)



class Person(PersonBase):
    
    password: str = Field(
        ..., 
        min_length = 8,
        max_length = 10
    )  
    
    class Config:
        schema_extra = {
            'example': {                
                'first_name': 'Erika',
                'last_name': 'Alvarez',
                'age': 17,
                'password': 'josejose12',                
                'hair_color': 'brown',                
                'is_married': False,
                'email': 'turko@gmail.com',
                'url_client': 'https://platzi.com'
                
            }
        }



class PersonOut(PersonBase):
    pass
    


class LoginOut(BaseModel):
    username: str = Field(..., max_length = 20, example = 'erika123')
    message = str = Field(default = 'Login Succesfully')



@app.get(
    path = '/', 
    status_code = status.HTTP_200_OK
    )
def home():
    return {'Hello': 'World'}



# Request and Response Body


@app.post(
    path='/person/new', 
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED        
    )
def create_person(person: Person = Body(...)):
    return person



# Validations: Query Parameters


@app.get(
    path = '/person/detail',
    status_code = status.HTTP_200_OK
    )
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



# Validations: Path Parameter


@app.get(
    path = '/person/detail/{person_id}',
    status_code = status.HTTP_200_OK
    )
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


@app.put(
    path = '/person/{person_id}', 
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED
    )
def update_person(
    person_id: int = Path(
        ...,
        title = 'Person ID',
        description = 'This is the person ID',
        gt = 0,
        example = 24
        ),
    person: Person = Body(...,),
    location: Location = Body(...)
):
    result = dict(person)
    result.update(dict(location))

    return result 



# Validations: Forms


@app.post(
    path = '/login',
    response_model = LoginOut,
    status_code = status.HTTP_200_OK
)   
def login(
    username: str = Form(...), 
    password: str = Form(...)):
    return LoginOut(username = username)



# Cookies and Headers Parameters

@app.post(
    path = '/contact',
    status_code = status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1
    ),
    last_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        max_length = 200,
        min_length = 20
    ),
    user_agent: Optional[str] = Header(default = None),
    ads: Optional[str] = Cookie(default = None)
):
    return user_agent



# Files

@app.post(path = '/post-image')
def post_image(image: UploadFile = File(...)):
    return{
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': str(round(len(image.file.read())/1024, ndigits = 2)) + ' Kb'
    }
    
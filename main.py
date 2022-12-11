# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import AnyUrl, EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
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



# home


@app.get(
    path = '/', 
    status_code = status.HTTP_200_OK,
    tags = ['Home']
    )
def home():
    """
    Home page of the API

    This path returns the home page of the API.

    No parameters are required.
    """
    return {'Hello': 'World'}



# Request and Response Body


@app.post(
    path='/person/new', 
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED,
    tags = ['Persons'],
    summary = 'Create person in the app'      
    )
def create_person(person: Person = Body(...)):
    '''
    Create Person
    
    This path operation creates a person in the app and save the information in the database
    
    Parameters:
    - Request body parameter:
        -**person: Person** -> A person model with first name, last name, age, hair color, marital status, email, url client and password.
    
    -Returns a person model with first name, last name, age, hair color, marital status, email and url client.
    '''
    return person



# Validations: Query Parameters


@app.get(
    path = '/person/detail',
    status_code = status.HTTP_200_OK,
    tags = ['Persons']
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
    '''
    Show Person

    This path operation shows the person's name and age in the app from the database.

    Parameters:
    - Query parameter:
        - **name: str** -> This is the person name. It's between 1 and 50 characters.
        - **age: int** -> This is the person age. It's required.

    Returns a JSON with the person's name and age.
    '''
    return {name: age}



# Validations: Path Parameter

persons = [1, 2, 3, 4, 5]


@app.get(
    path = '/person/detail/{person_id}',
    status_code = status.HTTP_200_OK,
    tags = ['Persons']
    )
def show_person(
    person_id: int = Path(
        ...,    
        title = 'Person Id',
        description = "This is the person Id. It's between 1 and 50 numbers characters, and it's required",        
        gt = 0,
        example = 3
        )
):
    '''
    Show Person

    This path operation shows the person's ID in the app from the database.

    Parameters:
    - Path parameter:
        - **person_id: int** -> This is the person ID. It's required and must be greater than 0.

    Returns a JSON with the person's ID.
    '''
    if person_id not in persons:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "This person doesn't exist"
        )
    return {person_id: 'It exists!'}



# Validations: Request Body


@app.put(
    path = '/person/{person_id}', 
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED,
    tags = ['Persons']
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
    '''
    Update person
    
    This path operation inherits all its attributes from the person class and allows the client to update its city, state and country information.
    
    Parameters:
    -Request body parameter:
        -**Person id** -> mandatory parameter.
        -**City** -> mandatory parameter.
        -**State** -> mandatory parameter.
        -**Country** -> mandatory parameter.                
        
    -Returns a JSON with person's model with first name, last name, age, hair color, marital status, email, url client, city, state and country.
    '''
    result = dict(person)    
    result.update(dict(location))

    return result



# Validations: Forms


@app.post(
    path = '/login',
    response_model = LoginOut,
    status_code = status.HTTP_200_OK,
    tags = ['Persons']
)   
def login(
    username: str = Form(...), 
    password: str = Form(...)):
    '''
    Login
    
    This path operation allow to client sign in the app. The database will validate if the username and password are correct.
    
    Parameters:
    -Request body parameter:
        -**username** -> mandatory parameter.
        -**password** -> mandatory parameter.
        
    -Returns a JSON with username.
    '''
    return LoginOut(username = username)



# Cookies and Headers Parameters

@app.post(
    path = '/contact',
    status_code = status.HTTP_200_OK,
    tags = ['Contact']
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
    '''
    Contact

    This path operation allows the user to contact the company.

    Parameters:
    - user_agent: The browser that the user is using.
    - ads: The cookies that this website uses.
    - Request body parameter:
        - **first_name** -> mandatory parameter.
        - **last_name:** -> mandatory parameter.
        - **email:** -> mandatory parameter.
        - **message: -> mandatory parameter.
        
    -Returns: user agent's information.
        '''

    return user_agent



# Files

@app.post(path = '/post-image', tags = ['Post Images'] )
def post_image(image: UploadFile = File(...)):
    '''
    Post image

    This path operation allows you to post an image in the app to the database.

    Parameters:
    - Request body parameter:
        - **image** -> This is the file to upload. It's required.

    Returns a JSON with the file's name, format and size in kb.
    '''
    return{
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': str(round(len(image.file.read())/1024, ndigits = 2)) + ' Kb'
    }
    
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'Hello': 'World'}
    
    
    




if __name__ == '__main__':
    home()
    
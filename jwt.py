from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION= 1
SECRET="ARGON2"

app= FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
oauth2=OAuth2PasswordBearer(tokenUrl="login")
crypt= CryptContext(schemes="bcrypt")

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    profile_image:str
    username:str
    full_name: str
    email:str
    phone:str
    matricula:str
    disabled:bool

class UserDB(User):
    password:str

users_db ={
        "V1ct0r":{
         "profile_image": "/static/Victor.jpg",
         "username": "V1ct0r",
         "full_name": "Victor Manuel Rosales Zayas",
         "email": "victor.rosalesz@alumno.buap.mx",
         "phone": "2224415653",
         "matricula": "202081021",
         "disabled": False,
         "password": "$2a$12$ai25p7FXqmtUWkx4aV/e4O/rbl119UzjuEHNgHbEFgLa4WS0d/9gi"#jquery
    },
         "K3v1n":{
         "profile_image": "/static/Kevin.jpg",
         "username": "K3v1n",
         "full_name": "Kevin Armas Hernández",
         "email": "kevin.armas@alumno.buap.mx",
         "phone": "6141998990",
         "matricula": "202094162",
         "disabled": False,
         "password": "$2a$12$.QDDBHePXqDVJlhlU/aMIeXm4Ujv9ma5XCBJFNJxpdary17Hk1vTC"#bearer
    },
        "Arruch4":{
         "profile_image": "/static/Eduardo.jpg",
         "username": "Arruch4",
         "full_name": "José Eduardo Arrucha Álvarez",
         "email": "jose.arruchaal@alumno.buap.mx",
         "phone": "2213317079",
         "matricula": "201965873",
         "disabled": False,
         "password": "$2a$12$DBHyl24F6i.ea9w6c8TbQeISI7XnHxxabSf9G5xhtUGqL6EanFnRa"#ARGON
    },
        "Y0ssel1n":{
        "profile_image": "/static/Yosselin.jpg",
         "username": "Y0ssel1n",
         "full_name": "Yosselin Pablo Ruiz",
         "email": "yosselin.pablo@alumno.buap.mx",
         "phone": "2288358188",
         "matricula": "202061872",
         "disabled": False,
         "password": "$2a$12$WsR854ZpgsAT8Kr27xMLxOGbrFPZWcoDzWmLODm4Cvm/bwiGft2hi"#python
    },
        "Delf1n0":{
        "profile_image": "/static/Delfino.jpg",
         "username": "Delf1n0",
         "full_name": "Luis Delfino Castro Nava",
         "email": "luis.castron@alumno.buap.mx",
         "phone": "8110502639",
         "matricula": "202087173",
         "disabled": False,
         "password": "$2a$12$UxVe8YxJxBtWFMNvuZloE.pgP.96RbsnxN.ImPjkMbF0RVKKvoSjG"#script
    },
        "Estef4n1a":{
        "profile_image": "/static/Estefania.jpg",
         "username": "Estef4n1a",
         "full_name": "Estefania Rodríguez Martínez",
         "email": "estefania.rodriguezma@alumno.buap.mx",
         "phone": "2228669227",
         "matricula": "202072819",
         "disabled": False,
         "password": "$2a$12$t2u86il0lO2wpw4pZbATW.X6NsXpMASdCpAgFLG65cocGUSp/4R7K"#json
    },
         "Abr4ham":{
         "profile_image": "/static/Abraham.jpg",
         "username": "Abr4ham",
         "full_name": "Abraham Coagtle Temis",
         "email": "abraham.coagtle@alumno.buap.mx",
         "phone": "2731327748",
         "matricula": "202182371",
         "disabled": False,
         "password": "$2a$12$NOBUSGIeCQmrECU4ompm.uYKJgfeIfttvE8/dJdc4MdJgYGvCu56G"#ajax
    },
        "P1l4r":{
         "profile_image": "/static/Pilar.jpg",
         "username": "P1l4r",
         "full_name": "Pilar Hernandez Zambrano",
         "email": "pilar.hernandezz@alumno.buap.mx",
         "phone": "2223223454",
         "matricula": "201929897",
         "disabled": False,
         "password": "$2a$12$SDmqec3Cx7k6OVk/OyjoCeNCr.6e/rX4axdnSIXBHZcFAnJ.q0jIi"#bcrypt
    },
        "V1cent3":{
         "profile_image": "/static/Vicente.jpg",
         "username": "V1cent3",
         "full_name": "Vicente Zavaleta Sanchez",
         "email": "vicente.zavaletas@alumno.buap.mx",
         "phone": "2212671849",
         "matricula": "202043826",
         "disabled": False,
         "password": "$2a$12$xZjANzqqEdgAIBUwSCz5l.yDwG199uvkQlla7f1deKp7I.ipgBbUa"#static
    },
         "Ju4n":{
         "profile_image": "/static/Juan.jpg",
         "username": "Ju4n",
         "full_name": "Juan Pablo Mendoza Armas",
         "email": "juan.mendozaar@alumno.buap.mx",
         "phone": "2281776285",
         "matricula": "202084360",
         "disabled": False,
         "password": "$2a$12$6rh/PT.2j7g8tGrQVdwswuosYNumjx/Zzw/4ieX7FfHiZ.zqskBrS"#cors
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:str=Depends(oauth2)):
    try:
        username= jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")

    return search_user(username)

async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user
        
        
@app.post("/login/")
async def login(form:OAuth2PasswordRequestForm= Depends()):

    user_db= users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user= search_user_db(form.username)     
    
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token_expiration=timedelta(minutes=ACCESS_TOKEN_DURATION)

    expire=datetime.utcnow()+access_token_expiration
    
    access_token={"sub": user.username,"exp": expire}
    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type":"bearer"}

@app.get("/users/me/")
async def me(user:User= Depends (current_user)):
    return user
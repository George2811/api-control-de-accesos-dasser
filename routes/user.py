from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from config.db import conn
from model.user import users
from schemas.user import User
from datetime import datetime
from cryptography.fernet import Fernet
from sqlalchemy import text
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users/{id}", tags=["User"])
async def get_user_by_id(id: int):
    query = text(f"SELECT id, name, last_name, login, status, created_at, updated_at from users where users.id = {id}")
    result = conn.execute(query).first()
    if result is None:
        raise HTTPException(HTTP_404_NOT_FOUND, f"No se encontró el usuario con id: {id}")    
    return result

@user.get("/users", tags=["User"])
async def get_users():
    query = text(f"SELECT id, name, last_name, login, status, created_at, updated_at from users")
    result = conn.execute(query).fetchall()
    return result

@user.post("/users", tags=["User"])
async def save_user(user: User):
    if user.password is None or user.password == "":
        raise HTTPException(HTTP_404_NOT_FOUND, f"No se ingresó una contraseña para el nuevo usuario.")
    if user.name == "" or user.last_name == "" or user.login == "" or user.status == "":
        raise HTTPException(HTTP_404_NOT_FOUND, f"Todos los campos son obligatorios.")
    
    now = datetime.now()
    new_user = {'name': user.name,
                'last_name': user.last_name,
                'login': user.login,
                'status': user.status,
                'created_at': now,
                'updated_at': now}
    new_user['password'] = f.encrypt(user.password.encode('utf-8')).decode('utf-8')

    conn.execute(users.insert().values(new_user))
    return JSONResponse(status_code=HTTP_200_OK, content={'response': 'Se creó el usuario correctamente'})

@user.put("/users/{id}", tags=["User"])
async def update_user(id: int, user: User):
    current_user = conn.execute(users.select().where(users.c.id == id)).first()

    if current_user is None:
        raise HTTPException(HTTP_404_NOT_FOUND, f"No se encontró el usuario con id: {id}")
    
    edited_user = {'name': user.name,
                'last_name': user.last_name,
                'login': user.login,
                'status': user.status,
                'created_at': current_user.created_at,
                'updated_at': datetime.now()}
    edited_user['password'] = f.encrypt(user.password.encode('utf-8')).decode('utf-8') if user.password is not None else current_user.password

    result = conn.execute(users.update().values(edited_user).where(users.c.id == id))
    if result:
        return JSONResponse(status_code=HTTP_200_OK, content={'response': f'Se actualizó el usuario con id {id} correctamente'})

    raise HTTPException(HTTP_400_BAD_REQUEST, f"Error al actualizar el usuario con id: {id}")

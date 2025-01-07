from fastapi import APIRouter, Form
from app.auth import crud

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/registration')
async def registration(username: str = Form(...), password: str = Form(...)):
    return crud.register(username, password)

@router.get('/login')
async def login(username: str, password: str):
    return crud.login(username, password)
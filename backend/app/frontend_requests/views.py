from fastapi import APIRouter
# from app.frontend_requests.schemas import FilterKeyElem
from app.frontend_requests import crud

router = APIRouter(prefix='/frontend', tags=['frontend'])


@router.get('/get_cards')
def get_cards(cake_type: int, data:str):
    data = data.split(';')
    filter_key = [cake_type, dict(map(lambda x: (x.split(':')[0], x.split(':')[1].split(',')), data))]

    res = crud.get_sorted_cards([cake_type, filter_key])
    return res

    
@router.get('/get_conditer_info')
def cond_info(conditer_id: int):
    return crud.get_conditer_info(conditer_id)

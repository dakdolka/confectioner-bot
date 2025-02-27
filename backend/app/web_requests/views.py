from fastapi import APIRouter
# from app.frontend_requests.schemas import FilterKeyElem
from app.web_requests import crud

router = APIRouter(prefix='/web_request', tags=['web_request'])


@router.get('/get_all_cake_types')
def get_all_cake_types():
    return crud.get_cake_types()


@router.get('/get_cake_ingrs')
def get_all_cake_types(cake_type_id: int):
    return crud.get_cake_ingrs(cake_type_id)  


@router.get('/get_cards')
def get_cards(cake_type: int, data:str):
    data = data.split(';')
    filter_key = [cake_type, dict(map(lambda x: (x.split(':')[0], x.split(':')[1].split(',')), data))]
    res = crud.get_sorted_cards(filter_key)
    return res 
    # {
    #     "title": "str_value",
    #     "product_id": int_value,
    #     "creator_id": bigint_value
    # }
    
    
@router.get('/get_conditer_info')
def cond_info(conditer_id: int):
    return crud.get_conditer_info(conditer_id)




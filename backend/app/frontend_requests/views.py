from fastapi import APIRouter, Body
# from data.queries.orm import SyncORM
from frontend_requests.schemas import FilterKeyElem
from typing import Dict

router = APIRouter(prefix='/frontend', tags=['frontend'])


@router.get('/get_cards')
def get_cards(cake_type: int, data:str):
    data = data.split(';')
    filter_key = [cake_type, dict(map(lambda x: (x.split(':')[0], x.split(':')[1].split(',')), data))]
    # SyncORM.create_table()
    # SyncORM.insert_data()


    # res = SyncORM.get_result([cake_type, filter_key])
    print([cake_type, filter_key])

    return [cake_type, filter_key]


@router.get('/get_conditer_info')
def cond_info(conditer_id: int):
    return SyncORM.get_conditer_info(conditer_id)

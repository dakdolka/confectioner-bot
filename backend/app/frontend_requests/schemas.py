from pydantic import BaseModel
from typing import Annotated
from annotated_types import MinLen, MaxLen

class FilterKeyElem(BaseModel):
    ingr_id: int
    tastes_id: list[int]
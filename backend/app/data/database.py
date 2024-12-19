from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from config import settings
import asyncio
from typing import Annotated


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False)

session_factory = sessionmaker(sync_engine)
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)

    }

    repr_columns_num = 3
    repr_cols = tuple()

    def __repr__(self): # переделка принта моделей в логах
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_columns_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"{self.__class__.__name__} {', '.join(cols)}"
from typing import Any, Optional
from typing import Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, Numeric, ForeignKey, text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Database.database import Base
from datetime import datetime



metadata_obj = MetaData()
time = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
intpk = Annotated[int, mapped_column(primary_key=True)]


class ConditersORM(Base):
    __tablename__ = 'tconditers'
    
    fuserid: Mapped[int] = mapped_column(BigInteger, primary_key=True) 
    fcreatingtime: Mapped[time]
    fname: Mapped[str]
    fexp: Mapped[str]
    fabout: Mapped[Optional[str]]
    finstagram: Mapped[Optional[str]]
    fvk: Mapped[Optional[str]]
    fyoutube: Mapped[Optional[str]]
    fproducts: Mapped[list["TproductORM"]] = relationship(
        back_populates="fconditer"
    )
    fcanmake: Mapped[list["TCanMakeORM"]] = relationship(
        back_populates="fconditer"
    )


class TproductORM(Base): 
    __tablename__ = 'tproduct'

    fproductid: Mapped[intpk]
    fuserid: Mapped[int] = mapped_column(BigInteger, ForeignKey('tconditers.fuserid', ondelete="CASCADE"))
    fcreatingtime: Mapped[time]
    fiscake: Mapped[bool]
    fproduct_name: Mapped[str]

    fconditer: Mapped['ConditersORM'] = relationship(
        back_populates='fproducts'
    )
    fcakeparts: Mapped[Optional[list['TCakeORM']]] = relationship(
        back_populates='fproduct'
    )


class TCakeTypeORM(Base):
    __tablename__ = 'tcake_type'

    fid: Mapped[intpk]
    fcake_type: Mapped[str]
    fuse: Mapped[Optional[list['TPossibleCakeORM']]] = relationship(
        back_populates = 'fcake_type_more',
        primaryjoin="TPossibleCakeORM.fcake_type == TCakeTypeORM.fid"
    )


class TCakeIngrORM(Base):
    __tablename__ = 'tcake_ingr'

    fid: Mapped[intpk]
    fcake_ingr: Mapped[str]
    fuse: Mapped[Optional[list['TPossibleCakeORM']]] = relationship(
        back_populates = 'fcake_ingr_more',
        primaryjoin="TPossibleCakeORM.fcake_ingr == TCakeIngrORM.fid"
    )


class TIngrTasteORM(Base):
    __tablename__ = 'tingr_taste'

    fid: Mapped[intpk]
    fingr_taste: Mapped[str]
    fuse: Mapped[Optional[list['TPossibleCakeORM']]] = relationship(
        back_populates = 'fingr_taste_more',
        primaryjoin="TPossibleCakeORM.fingr_taste == TIngrTasteORM.fid"
    )


class TPossibleCakeORM(Base):
    __tablename__ = 'tpossible_cake'

    fid: Mapped[intpk]

    fcake_type: Mapped[int] = mapped_column(ForeignKey('tcake_type.fid', ondelete="CASCADE"))
    fcake_type_more: Mapped['TCakeTypeORM'] = relationship(
        back_populates='fuse'
    )
    fcake_ingr: Mapped[int] = mapped_column(ForeignKey('tcake_ingr.fid', ondelete="CASCADE"))
    fcake_ingr_more: Mapped['TCakeIngrORM'] = relationship(
        back_populates='fuse'
    )
    fingr_taste: Mapped[int] = mapped_column(ForeignKey('tingr_taste.fid', ondelete="CASCADE"))
    fingr_taste_more: Mapped['TIngrTasteORM'] = relationship(
        back_populates='fuse'
    )

    fcakes_use: Mapped[Optional[list['TCakeORM']]] = relationship(
        back_populates='fingrcomb'
    )
    fwho_can_make: Mapped[Optional[list['TCanMakeORM']]] = relationship(
        back_populates='fingrcomb'
    )
    detail_orders = relationship('TDetailOrdersORM', back_populates='forder_cake')

    


class TCakeORM(Base):
    __tablename__ = 'tcake'

    fproductid: Mapped[intpk] = mapped_column(ForeignKey(TproductORM.fproductid, ondelete="CASCADE"))
    fingr: Mapped[intpk] = mapped_column(ForeignKey(TPossibleCakeORM.fid, ondelete="CASCADE"))
    fproduct: Mapped['TproductORM'] = relationship(
        back_populates='fcakeparts'
    )
    fingrcomb: Mapped['TPossibleCakeORM'] = relationship(
        back_populates='fcakes_use'
    )


class TCanMakeORM(Base):
    __tablename__ = 'tcan_make'

    fuserid: Mapped[intpk] = mapped_column(ForeignKey(ConditersORM.fuserid, ondelete="CASCADE"))
    fingr: Mapped[intpk] = mapped_column(ForeignKey(TPossibleCakeORM.fid, ondelete="CASCADE"))
    fconditer: Mapped['ConditersORM'] = relationship(
        back_populates='fcanmake'
    )
    fingrcomb: Mapped['TPossibleCakeORM'] = relationship(
        back_populates='fwho_can_make'
    )


class TOrdersORM(Base):
    __tablename__= 'torders'

    forder_id: Mapped[intpk]
    fuser_tg_id: Mapped[str]
    forder_date: Mapped[time]
    fis_cake: Mapped[bool]

class TDetailOrdersORM(Base):
    __tablename__='tdetail_orders'
    fid: Mapped[intpk]
    forder_id: Mapped[intpk] = mapped_column(ForeignKey('torders.forder_id', ondelete='CASCADE'))
    forder_cake: Mapped['TPossibleCakeORM'] = relationship(
        back_populates='detail_orders'
    )
    forder_cake_id = Column(Integer, ForeignKey('tpossible_cake.fid'))

from sqlalchemy import text, insert, select, func, cast, Integer, and_, case 
from Database.database import sync_engine, session_factory
from Database.models import metadata_obj, TCakeTypeORM, TCakeIngrORM, TIngrTasteORM, TPossibleCakeORM, ConditersORM, TproductORM, TCakeORM
from Database.database import Base
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from collections import defaultdict

#функция для получения вкусов ингридиента по типу торта и ингидиенту
def get_ingr_taste(data):
    with session_factory() as session:
        return session.query(TPossibleCakeORM.fingr_taste).filter(TPossibleCakeORM.fcake_type == data['cake_type'], TPossibleCakeORM.fcake_ingr == data['cake_ingr']).all()

class SyncORM:
    @staticmethod
    def create_tables():
            sync_engine.echo = False #можно отключить логи для опреелённых функций
            Base.metadata.drop_all(sync_engine) #удаление существующих таблиц
            Base.metadata.create_all(sync_engine)
            sync_engine.echo = False

    @staticmethod
    def insert_data():
        with session_factory() as session:
            create = []
            create += [TCakeTypeORM(fcake_type='Муссовый')]
            create += [TCakeTypeORM(fcake_type='Бисквитный')]

            create += [TCakeIngrORM(fcake_ingr='Мусс')]
            create += [TCakeIngrORM(fcake_ingr='Начинка')]
            create += [TCakeIngrORM(fcake_ingr='Бисквит')]

            create += [TIngrTasteORM(fingr_taste='Малина')]
            create += [TIngrTasteORM(fingr_taste='Клубника')]
            create += [TIngrTasteORM(fingr_taste='Банан')]



            create += [TPossibleCakeORM(fcake_type=1, fcake_ingr=1, fingr_taste=1)]
            create += [TPossibleCakeORM(fcake_type=1, fcake_ingr=1, fingr_taste=2)]
            create += [TPossibleCakeORM(fcake_type=1, fcake_ingr=1, fingr_taste=3)]
            create += [TPossibleCakeORM(fcake_type=1, fcake_ingr=2, fingr_taste=1)]
            create += [TPossibleCakeORM(fcake_type=1, fcake_ingr=2, fingr_taste=3)]
            create += [TPossibleCakeORM(fcake_type=2, fcake_ingr=2, fingr_taste=1)]
            create += [TPossibleCakeORM(fcake_type=2, fcake_ingr=2, fingr_taste=2)]
            create += [TPossibleCakeORM(fcake_type=2, fcake_ingr=2, fingr_taste=3)]
            create += [TPossibleCakeORM(fcake_type=2, fcake_ingr=3, fingr_taste=3)]

            
            create += [ConditersORM(fuserid=1231231231, fname='Антон', fexp='40 лет на заводе')]
            create += [ConditersORM(fuserid=5962717642, fname='Антон', fexp='40000 лет', finstagram='клшпошкоп', fyoutube='https://youtube.com')]


            create += [TproductORM(fuserid=1231231231, fiscake=True, fproduct_name='Муссовый торт с малиновым муссом и банановой начинкой')]
            create += [TproductORM(fuserid=1231231231, fiscake=True,fproduct_name='Бисквитный торт с банановым бисквитом и клубничной начинкой')]
            create += [TCakeORM(fproductid=1, fingr=1)]
            create += [TCakeORM(fproductid=1, fingr=5)]
            create += [TCakeORM(fproductid=2, fingr=9)]
            create += [TCakeORM(fproductid=2, fingr=7)]
            
            
            session.add_all(create)
            session.commit()

    @staticmethod
    def get_cake_type():
        with session_factory() as session:
            query = select(TCakeTypeORM.fcake_type, TCakeTypeORM.fid)
            res = session.execute(query).all()
            print(res)
            return res
    
    @staticmethod
    def get_cake_ingrs(cake_type):
        with session_factory() as session:
            query = select(TCakeIngrORM.fcake_ingr, TCakeIngrORM.fid).where(and_(TCakeTypeORM.fcake_type == cake_type, TCakeTypeORM.fid == TPossibleCakeORM.fcake_type, TCakeIngrORM.fid == TPossibleCakeORM.fcake_ingr)).distinct()
            res = session.execute(query)
            return res.scalars().all()
    

    @staticmethod
    def getcake_ingr_taste(cake_type, cake_ingr):
        ans = []
        with session_factory() as session:
            query = select(TIngrTasteORM.fingr_taste, TIngrTasteORM.fid).where(and_(TPossibleCakeORM.fcake_ingr == TCakeIngrORM.fid, TPossibleCakeORM.fcake_type == TCakeTypeORM.fid, TCakeIngrORM.fcake_ingr == cake_ingr, TCakeTypeORM.fcake_type == cake_type)).distinct()
            res = session.execute(query).all()
            print(res)
            return res
        
    
    @staticmethod
    def get_tastes_id(data: dict):
        cake_type_back = data['cake_type_back']
        cake_type = data['cake_type']
        cake_ingr = data['cake_ins_back']
        with session_factory() as session:
            query = select(TCakeIngrORM.fid).where(and_(TCakeIngrORM.fcake_ingr.in_(cake_ingr), TCakeTypeORM.fcake_type == cake_type))
            res = session.execute(query).scalars().all()
        ans = f'{cake_type_back};'
        dop = list(cake_ingr.values())
        for i in range(len(res)):
            if len(dop[i]) != 0:
                ans += f'{res[i]}:'
                for elem in dop[i]:
                    ans += f'{elem},'
                ans = ans[:-1] + ';'
        return ans[:-1]
    

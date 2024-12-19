from sqlalchemy import text, insert, select, or_, and_, BigInteger, cast
from data.database import sync_engine, async_engine, session_factory
from models import ConditersORM, TCakeORM, TproductORM, TPossibleCakeORM, TIngrTasteORM, TCakeIngrORM, TCakeTypeORM, TCanMakeORM
from data.database import Base
from sqlalchemy.orm import selectinload
from sorting import sort_prods



class SyncORM:
    @staticmethod
    def create_table():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
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

            create += [TCanMakeORM(fuserid=1231231231, fingr=5)]
            
            
            session.add_all(create)
            session.commit()
    

    @staticmethod
    def select_data():
        with session_factory() as session:
            fuserid = 1
            # fname = session.get(ConditersORM, {"fuserid": fuserid})
            query = select(ConditersORM)
            res = session.execute(query)
            conditers = res.scalars().all() 
            print(f"{conditers = }")


    @staticmethod
    def update_data(conditer_id = 5962717642, new_username = 'Антон (бог)'):
        with session_factory() as session:
            conditer = session.get(ConditersORM, {"fuserid": conditer_id})
            conditer.fname = new_username
            session.commit()
    


    @staticmethod
    def create_profile(userid, name, exp, about=None, instagram=None, vk=None, youtube=None):
        with session_factory() as session:
            profile = ConditersORM(fuserid=userid, fname=name, fexp=exp, fabout=about, finstagram=instagram, fvk=vk, fyoutube=youtube)
            session.add(profile)
            session.commit()
            print('aa')
    

    @staticmethod
    def get_cake_types():
        with session_factory() as session:
            query = select(TCakeTypeORM)
            res = session.execute(query).scalars().all()
            return {elem.__dict__['fid']: elem.__dict__['fcake_type'] for elem in res}
    

    @staticmethod
    def get_cake_ingr(cake_type): # Выводить не номера ингридиентов, а названия
        with session_factory() as session:
            query = select(TPossibleCakeORM).filter(TPossibleCakeORM.fcake_type == cake_type)
            res = session.execute(query).scalars().all()
                
            return [elem.__dict__['fcake_ingr'] for elem in res]
    

    # @staticmethod
    # def get_cake_ingr():
    #     with session_factory() as session:
    #         query = select(TCakeIngrORM)
    #         res = session.execute(query).scalars().all()
    #         return {elem.__dict__['fid']: elem.__dict__['fcake_ingr'] for elem in res}

    @staticmethod
    def get_result(filter_cake):
        sort_prods_with_filter = sort_prods(filter_cake)
        prods = {}
        with session_factory() as session:
            query = (
                select(TproductORM)
                .options(selectinload(TproductORM.fcakeparts))
            )
            res = session.execute(query).scalars().all()

            for elem in res:
                ingr_taste_dict = {}
                for ingr in elem.fcakeparts:
                    stats = ingr.fingrcomb
                    ingr_taste_dict[stats.fcake_ingr] = stats.fingr_taste
                prods[(elem.fproductid, (elem.fproduct_name, elem.fuserid))] = [stats.fcake_type, ingr_taste_dict]
            
            print(prods)
            prods = list(map(lambda x: {'title': x[0][1][0], 'creator_id': x[0][1][1]}, sorted(prods.items(), key=sort_prods_with_filter)))
            return prods
    
    @staticmethod
    def get_conditer_info(conditer_id):
        with session_factory() as session:
            query = (
                select(ConditersORM)
                .where(ConditersORM.fuserid == cast(conditer_id, BigInteger))
                .options(selectinload(ConditersORM.fproducts))
            )
            conditer = session.execute(query).scalars().first()

            if not conditer:
                return None

            conditer_info = {
                'img': 'url',
                'name': conditer.fname,
                'experience': conditer.fexp,
                'creation_time': conditer.fcreatingtime,
                'youtube': conditer.fyoutube,
                'instagram': conditer.finstagram,
                'vk': conditer.fvk,
                'cakes': [
                    {
                        'name': product.fproduct_name,
                        'photo': 'url',
                        'description': 'Description',
                    }
                    for product in conditer.fproducts
                ]
            }
            return conditer_info

class AsyncORM:
    pass
from sqlalchemy import text, insert, select, or_, and_, BigInteger, cast, case, func
from app.data.database.database import sync_engine, session_factory
from app.data.database.models import ConditersORM, TCakeORM, TproductORM, TPossibleCakeORM, TIngrTasteORM, TCakeIngrORM, TCakeTypeORM, TCanMakeORM
from app.data.database.database import Base
from sqlalchemy.orm import selectinload
from app.data.queries.sorting import sort_prods


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


            create += [TproductORM(fuserid=1231231231, fproduct_name='Муссовый торт с малиновым муссом и банановой начинкой')]
            create += [TproductORM(fuserid=1231231231, fproduct_name='Бисквитный торт с банановым бисквитом и клубничной начинкой')]
            create += [TCakeORM(fproductid=1, fingr=1)]
            create += [TCakeORM(fproductid=1, fingr=5)]
            create += [TCakeORM(fproductid=2, fingr=9)]
            create += [TCakeORM(fproductid=2, fingr=7)]

            create += [TCanMakeORM(fuserid=1231231231, fingr=5)]
            
            
            session.add_all(create)
            session.commit()

    @staticmethod
    def create_test_confectioners(user_id):
    # Create test confectioners
        with session_factory() as session:
            confectioner1 = ConditersORM(
                fuserid=user_id,
                fname='John Doe',
                fexp='5 years',
                fabout='Best confectioner in town!',
                finstagram='@john_doe',
                fvk='@john_doe_vk',
                fyoutube='@john_doe_youtube'
            )
            session.add(confectioner1)

            # Create test products
            product1 = TproductORM(
                fuserid=confectioner1.fuserid,
                fproduct_name='Chocolate Cake',
            )
            session.add(product1)

            product2 = TproductORM(
                fuserid=confectioner1.fuserid,
                fproduct_name='Strawberry Pastry',
            )
            session.add(product2)

            session.commit()
    


    @staticmethod
    def create_profile(userid, name, exp, about=None, instagram=None, vk=None, youtube=None):
        with session_factory() as session:
            profile = ConditersORM(fuserid=userid, fname=name, fexp=exp, fabout=about, finstagram=instagram, fvk=vk, fyoutube=youtube)
            session.add(profile)
            session.commit()
            print('Profile created')
    

    @staticmethod
    def get_cake_ingr(cake_type): # Выводить не номера ингридиентов, а названия
        with session_factory() as session:
            query = select(TPossibleCakeORM).filter(TPossibleCakeORM.fcake_type == cake_type)
            res = session.execute(query).scalars().all()
                
            return [elem.__dict__['fcake_ingr'] for elem in res]
    

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

    @staticmethod
    def get_ingr_taste(data):
        with session_factory() as session:
            return session.query(
                TPossibleCakeORM.fingr_taste
                ).filter(
                    TPossibleCakeORM.fcake_type == data['cake_type'],
                    TPossibleCakeORM.fcake_ingr == data['cake_ingr']
                    ).all()

    @staticmethod
    def get_cake_types():
        with session_factory() as session:
            query = select(TCakeTypeORM.fcake_type, TCakeTypeORM.fid)
            res = session.execute(query).all()
            print(res)
            return res
    
    @staticmethod
    def get_cake_ingrs(cake_type):
        with session_factory() as session:
            query = (
                select(TCakeIngrORM.fcake_ingr, TCakeIngrORM.fid)
                .where(and_(
                    TCakeTypeORM.fcake_type == cake_type,
                    TCakeTypeORM.fid == TPossibleCakeORM.fcake_type,
                    TCakeIngrORM.fid == TPossibleCakeORM.fcake_ingr
                    ))
                .distinct()
            )
            res = session.execute(query)
            return res.scalars().all()
    

    @staticmethod
    def getcake_ingr_taste(cake_type, cake_ingr):
        ans = []
        with session_factory() as session:
            query = (
                select(TIngrTasteORM.fingr_taste, TIngrTasteORM.fid)
                .where(and_(
                    TPossibleCakeORM.fcake_ingr == TCakeIngrORM.fid,
                    TPossibleCakeORM.fcake_type == TCakeTypeORM.fid,
                    TCakeIngrORM.fcake_ingr == cake_ingr,
                    TCakeTypeORM.fcake_type == cake_type
                    ))
                .distinct()
            )
            res = session.execute(query).all()
            print(res)
            return res
        
    
    @staticmethod
    def get_tastes_id(data: dict):
        cake_type_back = data['cake_type_back']
        cake_type = data['cake_type']
        cake_ingr = data['cake_ins_back']
        with session_factory() as session:
            query = (select(TCakeIngrORM.fid)
                    .where(and_(
                        TCakeIngrORM.fcake_ingr.in_(cake_ingr),
                        TCakeTypeORM.fcake_type == cake_type
                        ))
                    )
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

    #методы для кондитерского бота
    @staticmethod
    def get_conf_info(id):
        with session_factory() as session:
            query = (
                select(ConditersORM)
                .where(ConditersORM.fuserid == cast(id, BigInteger))
                .options(selectinload(ConditersORM.fproducts))
            )

    @staticmethod
    def get_ingr_id(ingr):
        with session_factory() as session:
            query = (
                select(TCakeIngrORM.fid)
                .where(TCakeIngrORM.fcake_ingr == ingr)
            )
            res = session.execute(query).scalars().first()
            return res

    @staticmethod
    def insert_conf_cake(user_id, data):
        # {'cake_type': 'Муссовый',
        #  'cake_type_back': '1',
        #  'cake_ins': {'Мусс': ['Банан'], 'Начинка': ['Клубника']},
        #  'cake_ins_back': {'Мусс': ['3'], 'Начинка': ['2']}}
        cake_type = data['cake_type_back']
        cake_ins = {SyncORM.get_ingr_id(key): value for key, value in data['cake_ins_back'].items()}
        with session_factory() as session:
            id = session.query(func.max(ConditersORM.fuserid)).scalar() + 1
            for key, value in cake_ins.items():
                for elem in value:
                    dop = session.execute(
                        select(TPossibleCakeORM.fid)
                        .where(and_(
                            TPossibleCakeORM.fcake_ingr == key,
                            TPossibleCakeORM.fingr_taste == elem,
                            TPossibleCakeORM.fcake_type == cake_type
                        ))
                    ).scalars().first()
                    print(dop)
                    session.add(TCakeORM(fproductid=id, fingr=dop))
            session.flush()
            query = (
                insert(TproductORM)
                .values(fuserid=user_id, fproduct_name=data['cake_name'])
            )
            session.execute(query)
            session.commit()
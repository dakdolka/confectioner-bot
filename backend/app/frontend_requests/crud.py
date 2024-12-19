from sqlalchemy import select, cast, BigInteger
from data.database import session_factory
from data.models import TproductORM, ConditersORM
from sqlalchemy.orm import selectinload
from backend.app.frontend_requests.sorting import sort_prods

@staticmethod
def get_sorted_cards(filter_cake):
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

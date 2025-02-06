from sqlalchemy import select, cast, BigInteger, and_
from app.data.database.database import session_factory
from app.data.database import models
from sqlalchemy.orm import selectinload
from app.web_requests.sorting import sort_prods


def get_sorted_cards(filter_cake):
    sort_prods_with_filter = sort_prods(filter_cake)
    prods = {}
    with session_factory() as session:
        query = (
            select(models.TproductORM)
            .options(selectinload(models.TproductORM.fcakeparts))
        )
        res = session.execute(query).scalars().all()

        for elem in res:
            ingr_taste_dict = {}
            for part in elem.fcakeparts:
                stats = part.fingrcomb
                ingr_taste_dict[stats.fcake_ingr] = stats.fingr_taste
            prods[(elem.fproductid, (elem.fproduct_name, elem.fuserid))] = [stats.fcake_type, ingr_taste_dict]
        prods = list(map(lambda x: {'title': x[0][1][0], 'product_id': x[0][0], 'creator_id': x[0][1][1]}, sorted(prods.items(), key=sort_prods_with_filter)))
        return prods


def get_conditer_info(conditer_id):
    with session_factory() as session:
        query = (
            select(models.ConditersORM)
            .where(models.ConditersORM.fuserid == cast(conditer_id, BigInteger))
            .options(selectinload(models.ConditersORM.fproducts))
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

def get_cake_types():
    with session_factory() as session:
        query = select(models.TCakeTypeORM.fid, models.TCakeTypeORM.fcake_type)
        res = session.execute(query).all()
        print(res)
        return dict(res)


def get_cake_ingrs(cake_type):
    with session_factory() as session:
        query = (
            select(models.TCakeIngrORM.fcake_ingr, models.TCakeIngrORM.fid)
            .where(and_(
                int(models.TCakeTypeORM.fcake_type) == cake_type,
                models.TCakeTypeORM.fid == models.TPossibleCakeORM.fcake_type,
                models.TCakeIngrORM.fid == models.TPossibleCakeORM.fcake_ingr
                ))
            .distinct()
        )
        res = session.execute(query).scalars().all()
        return dict(res)
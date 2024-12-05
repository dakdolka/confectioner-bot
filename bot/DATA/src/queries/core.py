from sqlalchemy import text, insert, select, update
from database import sync_engine, async_engine
from models import metadata_obj, conditersTable


class SyncCore:
    @staticmethod
    def create_table():
        sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True


    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            stmt = insert(conditersTable).values(
                [
                    {'fuserid': 12312312312, 'fname': 'Антон', 'fexp': '40 лет на заводе'},
                    {'fuserid': 5962717642, 'fname': 'Антон', 'fexp': '40000 лет', 'finstagram': 'клшпошкоп', 'fyoutube': 'https://youtube.com'}
                ]
            )

            conn.execute(stmt)
            conn.commit()
    
    @staticmethod
    def select_data():
        with sync_engine.connect() as conn:
            query = select(conditersTable)
            res = conn.execute(query)
            print(f"{res.all() = }")
    

    @staticmethod
    def update_data(conditer_id = 5962717642, new_username = 'Антон (бог)'):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE tconditers SET fname=:new_username WHERE fuserid=:id")
            # stmt = stmt.bindparams(new_username=new_username, id=conditer_id)
            stmt = (
                update(conditersTable)
                .values(fname=new_username)
                # .where(conditersTable.c.fuserid==conditer_id)
                .filter_by(fuserid=conditer_id)

            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:
    @staticmethod
    async def create_table():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)

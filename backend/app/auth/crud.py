from app.data.database.models import TestRegORM
from app.data.database.database import session_factory
from sqlalchemy import select, cast, BigInteger
from app.data.database.models import TproductORM
from sqlalchemy import and_


def login(username: str, password: str) -> TestRegORM:
    with session_factory() as session:
        print(username, password)
        query = (
            select(TestRegORM)
            .where(TestRegORM.fname == username)
        )
        result = session.execute(query)
        user = result.scalar()
        if user and user.check_password(password):
            return user
        return 'Access Denied'
    
def register(username: str, password: str) -> TestRegORM:
    with session_factory() as session:
        user = TestRegORM(fname=username, fpassword=password)
        session.add(user)
        session.commit()
        # session.refresh(user)
        return user

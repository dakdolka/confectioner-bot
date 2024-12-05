import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM


SyncORM.create_table()
SyncORM.insert_data()


# SyncCore.select_data()
# SyncCore.update_data()
# SyncCore.select_data()

# SyncORM.select_data()

filter_cake = [
    1,
    {
        1: [1],
        2: [2]
    }
]

# SyncORM.create_profile(1, 'Антон (бог)', '4000000 лет')
# print(SyncORM.get_cake_types())
# print(SyncORM.get_cake_ingr(1))
#get_cake_ingr_taste(cake_type, cake_ingr)
print(*SyncORM.get_result(filter_cake).items(), sep='\n')
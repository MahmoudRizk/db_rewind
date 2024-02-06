from random import random

from vendors.postgres.Columns.column import Column


class Macaddr(Column):
    def get_column_type(self) -> str:
        return 'MACADDR'

    def random_value_generator(self) -> str:
        return '08:00:2b:01:02:03'

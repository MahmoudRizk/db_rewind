import random

from vendors.postgres.Columns.column import Column


class Real(Column):
    def get_column_type(self) -> str:
        return 'REAL'

    def random_value_generator(self) -> str:
        return str(random.uniform(1, 1000))

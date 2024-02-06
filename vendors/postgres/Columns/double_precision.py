import random

from vendors.postgres.Columns.column import Column


class DoublePrecision(Column):
    def get_column_type(self) -> str:
        return 'DOUBLE PRECISION'

    def random_value_generator(self) -> str:
        return str(random.uniform(1, 1000))

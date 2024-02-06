from random import random

from vendors.postgres.Columns.column import Column


class Interval(Column):
    def get_column_type(self) -> str:
        return 'INTERVAL'

    def random_value_generator(self) -> str:
        return '1 day'

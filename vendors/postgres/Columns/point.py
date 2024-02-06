from random import random

from vendors.postgres.Columns.column import Column


class Point(Column):
    def get_column_type(self) -> str:
        return 'POINT'

    def random_value_generator(self) -> str:
        return '(1.5, 2.5)'

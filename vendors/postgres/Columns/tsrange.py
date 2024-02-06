from random import random

from vendors.postgres.Columns.column import Column


class TSRange(Column):
    def get_column_type(self) -> str:
        return 'TSRANGE'

    def random_value_generator(self) -> str:
        return '[2022-01-01 00:00:00, 2022-01-10 00:00:00)'

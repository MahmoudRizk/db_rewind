from random import random

from vendors.postgres.Columns.column import Column


class NumRange(Column):
    def get_column_type(self) -> str:
        return 'NUMRANGE'

    def random_value_generator(self) -> str:
        return '(1.5, 5.5)'


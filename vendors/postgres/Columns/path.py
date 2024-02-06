from random import random

from vendors.postgres.Columns.column import Column


class Path(Column):
    def get_column_type(self) -> str:
        return 'PATH'

    def random_value_generator(self) -> str:
        return '((1,1),(2,2),(3,3))'

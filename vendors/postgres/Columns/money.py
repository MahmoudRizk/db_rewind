from random import random

from vendors.postgres.Columns.column import Column


class Money(Column):
    def get_column_type(self) -> str:
        return 'MONEY'

    def random_value_generator(self) -> str:
        return '123'

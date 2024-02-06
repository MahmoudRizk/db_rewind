from random import random

from vendors.postgres.Columns.column import Column


class Timestamp(Column):
    def get_column_type(self) -> str:
        return 'TIMESTAMP'

    def random_value_generator(self) -> str:
        return '2022-01-01 12:34:56'

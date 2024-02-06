from random import random

from vendors.postgres.Columns.column import Column


class TSQuery(Column):
    def get_column_type(self) -> str:
        return 'TSQUERY'

    def random_value_generator(self) -> str:
        return 'fat & rat | cat & hat'

from random import random

from vendors.postgres.Columns.column import Column


class Inet(Column):
    def get_column_type(self) -> str:
        return 'INET'

    def random_value_generator(self) -> str:
        return '192.168.0.1'

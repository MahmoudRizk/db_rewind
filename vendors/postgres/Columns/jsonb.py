from random import random

from vendors.postgres.Columns.column import Column


class Jsonb(Column):
    def get_column_type(self) -> str:
        return 'JSONB'

    def random_value_generator(self) -> str:
        return '{"key": "value"}'

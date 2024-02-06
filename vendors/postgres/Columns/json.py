from random import random

from vendors.postgres.Columns.column import Column


class Json(Column):
    def get_column_type(self) -> str:
        return 'JSON'

    def random_value_generator(self) -> str:
        return '{"key": "value"}'

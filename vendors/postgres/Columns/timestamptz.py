from random import random

from vendors.postgres.Columns.column import Column


class TimestampTZ(Column):
    def get_column_type(self) -> str:
        return 'TIMESTAMPTZ'

    def random_value_generator(self) -> str:
        return '2022-01-01 12:34:56+00'

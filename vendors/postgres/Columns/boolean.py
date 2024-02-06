import random

from vendors.postgres.Columns.column import Column


class Boolean(Column):
    def get_column_type(self) -> str:
        return 'BOOLEAN'

    def random_value_generator(self) -> str:
        return 'true' if random.choice([True, False]) else 'false'

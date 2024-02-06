from random import randint

from vendors.postgres.Columns.column import Column


class BigInteger(Column):
    def get_column_type(self) -> str:
        return 'BIGINT'

    def random_value_generator(self) -> str:
        return randint(1, 1000)

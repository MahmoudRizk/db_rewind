from random import random

from vendors.postgres.Columns.column import Column


class LineSegment(Column):
    def get_column_type(self) -> str:
        return 'LSEG'

    def random_value_generator(self) -> str:
        return '((1,2), (3,4))'

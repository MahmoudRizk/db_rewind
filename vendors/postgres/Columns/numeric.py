import random

from vendors.postgres.Columns.column import Column


class Numeric(Column):
    def __init__(self, precision: int, scale: int):
        self.precision = precision
        self.scale = scale

    def get_column_type(self) -> str:
        return f"NUMERIC({self.precision}, {self.scale})"

    def random_value_generator(self) -> str:
        return str(random.uniform(1, 1000))

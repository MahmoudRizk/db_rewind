from vendors.postgres.Columns.column import Column
from vendors.postgres.random_string_generator import RandomStringGenerator


class Varchar(Column):
    def __init__(self, length: int = 255):
        self.length = length

    def get_column_type(self) -> str:
        return f"VARCHAR({self.length})"

    def random_value_generator(self) -> str:
        return RandomStringGenerator.generate()

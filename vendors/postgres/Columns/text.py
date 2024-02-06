from vendors.postgres.Columns.column import Column
from vendors.postgres.random_string_generator import RandomStringGenerator


class Text(Column):
    def get_column_type(self) -> str:
        return 'TEXT'

    def random_value_generator(self) -> str:
        return RandomStringGenerator.generate(length=1000)

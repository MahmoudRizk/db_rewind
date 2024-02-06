from vendors.postgres.Columns.column import Column


class Circle(Column):
    def get_column_type(self) -> str:
        return 'CIRCLE'

    def random_value_generator(self) -> str:
        return '((1, 2), 5.0)'

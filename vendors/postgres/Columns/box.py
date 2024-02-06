from vendors.postgres.Columns.column import Column


class Box(Column):
    def get_column_type(self) -> str:
        return 'BOX'

    def random_value_generator(self) -> str:
        return '(1,2),(3,4)'

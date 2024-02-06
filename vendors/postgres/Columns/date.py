from vendors.postgres.Columns.column import Column


class Date(Column):
    def get_column_type(self) -> str:
        return 'DATE'

    def random_value_generator(self) -> str:
        return '2024-02-06 00:00:00'

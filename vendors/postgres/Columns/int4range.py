from vendors.postgres.Columns.column import Column


class Int4Range(Column):
    def get_column_type(self) -> str:
        return 'INT4RANGE'

    def random_value_generator(self) -> str:
        return '(1, 10)'

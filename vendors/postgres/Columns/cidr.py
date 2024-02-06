from vendors.postgres.Columns.column import Column


class Cidr(Column):
    def get_column_type(self) -> str:
        return 'CIDR'

    def random_value_generator(self) -> str:
        return '192.168.0.0/24'

from vendors.postgres.Columns.column import Column


class DateRange(Column):
    def get_column_type(self) -> str:
        return 'DATERANGE'

    def random_value_generator(self) -> str:
        return '[2022-01-01, 2022-01-10]'

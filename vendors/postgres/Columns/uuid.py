import uuid

from vendors.postgres.Columns.column import Column


class UUID(Column):
    def get_column_type(self) -> str:
        return 'UUID'

    def random_value_generator(self) -> str:
        return str(uuid.uuid4())

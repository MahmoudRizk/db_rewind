from vendors.postgres.Columns.date_range import DateRange
from vendors.postgres.Columns.varchar import Varchar
from vendors.postgres.Columns.big_integer import BigInteger
from vendors.postgres.Columns.boolean import Boolean
from vendors.postgres.Columns.box import Box
from vendors.postgres.Columns.char import Char
from vendors.postgres.Columns.cidr import Cidr
from vendors.postgres.Columns.circle import Circle
from vendors.postgres.Columns.date import Date
from vendors.postgres.Columns.double_precision import DoublePrecision
from vendors.postgres.Columns.inet import Inet
from vendors.postgres.Columns.int4range import Int4Range
from vendors.postgres.Columns.integer import Integer
from vendors.postgres.Columns.interval import Interval
from vendors.postgres.Columns.json import Json
from vendors.postgres.Columns.jsonb import Jsonb
from vendors.postgres.Columns.line_segment import LineSegment
from vendors.postgres.Columns.macaddr import Macaddr
from vendors.postgres.Columns.macaddr8 import Macaddr8
from vendors.postgres.Columns.money import Money
from vendors.postgres.Columns.numeric import Numeric
from vendors.postgres.Columns.numrange import NumRange
from vendors.postgres.Columns.path import Path
from vendors.postgres.Columns.point import Point
from vendors.postgres.Columns.polygon import Polygon
from vendors.postgres.Columns.real import Real
from vendors.postgres.Columns.small_integer import SmallInteger
from vendors.postgres.Columns.text import Text
from vendors.postgres.Columns.timestamp import Timestamp
from vendors.postgres.Columns.timestamptz import TimestampTZ
from vendors.postgres.Columns.tsquery import TSQuery
from vendors.postgres.Columns.tsrange import TSRange
from vendors.postgres.Columns.tstzrange import TSTZRange
from vendors.postgres.Columns.uuid import UUID
from vendors.postgres.db_rewinder import DBRewinder
from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.setup import Setup

dbconnection = DBConnection(
    host='127.0.0.1',
    database_name='test',
    username='mahmoudrizk',
    password='123456',
    port=5432
)

cursor = dbconnection.cursor().cursor


class Table:
    def __init__(self):
        self.columns = {
            'varchar_column': Varchar(),
            'char_column': Char(),
            'text_column': Text(),
            'integer_column': Integer(),
            'smallint_column': SmallInteger(),
            'bigint_column': BigInteger(),
            'numeric_column': Numeric(precision=10, scale=2),
            'real_column': Real(),
            'double_precision_column': DoublePrecision(),
            'boolean_column': Boolean(),
            'date_column': Date(),
            'timestamp_column': Timestamp(),
            'timestamptz_column': TimestampTZ(),
            'interval_column': Interval(),
            'uuid_column': UUID(),
            'json_column': Json(),
            'jsonb_column': Jsonb(),
            'point_column': Point(),
            'line_segment_column': LineSegment(),
            'box_column': Box(),
            'circle_column': Circle(),
            'path_column': Path(),
            'polygon_column': Polygon(),
            'inet_column': Inet(),
            'cidr_column': Cidr(),
            'macaddr_column': Macaddr(),
            'macaddr8_column': Macaddr8(),
            'tsquery_column': TSQuery(),
            'tsrange_column': TSRange(),
            'tstzrange_column': TSTZRange(),
            'daterange_column': DateRange(),
            'int4range_column': Int4Range(),
            'numrange_column': NumRange(),
            'money_column': Money(),
        }

    def create(self) -> str:
        res = """
            CREATE TABLE test_table (
                id SERIAL PRIMARY KEY,
                {}
            );
        """.format(', '.join(
            f"{column_name} {column_type.get_column_type()}" for column_name, column_type in self.columns.items()))

        print(res)
        return res

    def drop(self) -> str:
        return """
            DROP TABLE IF EXISTS test_table;
        """

    def insert_random_data(self):
        columns = ', '.join(f"\"{key}\"" for key, values in self.columns.items())
        values = ', '.join(f"'{value.random_value_generator()}'" for key, value in self.columns.items())
        res = """
            INSERT INTO test_table 
                ({}) VALUES ({})
            
        """.format(columns, values)

        print(res)

        return res


table = Table()

cursor.execute(table.drop())

cursor.execute(table.create())

for i in range(0, 100):
    cursor.execute(table.insert_random_data())

dbconnection.commit()

dbsetup = Setup(cursor=cursor)
dbsetup.auto_install()
dbconnection.commit()

cursor.execute("""
    DELETE FROM test_table;
""")
dbconnection.commit()

dbrewinder = DBRewinder(cursor=cursor)
dbrewinder.rewind()
dbconnection.commit()

dbconnection.close()

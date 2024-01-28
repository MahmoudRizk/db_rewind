from vendors.postgres.dbconnection import DBConnection
from console.menu.main import Main as ConsoleMain

import click
from prompt_toolkit import PromptSession


@click.command()
@click.option('--db_name', required=True, help='Database name.')
@click.option('--db_user', required=True, help='Database user.')
@click.option('--db_password', required=True, help='Database password.')
@click.option('--db_host', default='localhost', help='Database host.')
@click.option('--db_port', default='5432', help='Database port.')
def main(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    session = PromptSession()
    dbconnection = DBConnection(
        database_name=db_name,
        password=db_password,
        username=db_user,
        host=db_host,
        port=db_port
    )

    ConsoleMain(session).execute(
        session=session,
        dbconnection=dbconnection
    )
    print('GoodBye!')


if __name__ == "__main__":
    main()

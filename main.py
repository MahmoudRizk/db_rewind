import argparse
import os
import sys

from dotenv import load_dotenv

from db_rewind.console.menu.main import Main as ConsoleMain

from prompt_toolkit import PromptSession

from db_rewind.postgres.db_rewinder import DBRewinder
from db_rewind.postgres.db_setup import DBSetup


def main():
    load_dotenv()

    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Command line tool')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create the parser for the "rewind" command
    parser_rewind = subparsers.add_parser('rewind', help='Rewind the database')
    parser_rewind.add_argument('--db-rewind-date', type=str, help='Optional date to rewind the database to')
    parser_rewind.add_argument('--disable-user-interaction', action='store_true', help='Disable user interaction')

    # Create the parser for the "setup" command
    parser_setup = subparsers.add_parser('setup', help='Setup the database')
    parser_setup.add_argument('--disable-user-interaction', action='store_true', help='Disable user interaction')

    # Start interactive cli
    subparsers.add_parser('interactive', help='Start interactive cli')

    # Parse the arguments
    args = parser.parse_args()

    if args.command == 'rewind':
        handle_rewind(args)
    elif args.command == 'setup':
        handle_setup(args)
    elif args.command == 'interactive':
        handle_interactive(args)


def handle_rewind(args):
    load_dotenv()
    if args.disable_user_interaction:
        print("User interaction is disabled for rewind.")
        os.environ['DB_REWINDER_ALLOW_USER_HANDLE_ERROR_MANUALLY'] = '0'
        os.environ['DB_REWINDER_ALLOW_INPUT_PROMPTS'] = '0'

    if args.db_rewind_date:
        print(f"Rewinding database to {args.db_rewind_date}.")
        os.environ['DB_REWINDER_REWIND_DATE'] = args.db_rewind_date
    else:
        print("Rewinding database to the default date from .env file")

    res = DBRewinder.execute()
    if not res.is_success():
        sys.exit(res.get_exit_code())



def handle_setup(args):
    if args.disable_user_interaction:
        print("User interaction is disabled for setup.")
        os.environ['DB_REWINDER_ALLOW_USER_HANDLE_ERROR_MANUALLY'] = '0'
        os.environ['DB_REWINDER_ALLOW_INPUT_PROMPTS'] = '0'

    print("Setting up the database...")
    res = DBSetup.execute()
    if not res.is_success():
        sys.exit(res.get_exit_code())


def handle_interactive(args):
    os.environ['DB_REWINDER_ALLOW_USER_HANDLE_ERROR_MANUALLY'] = '1'
    os.environ['DB_REWINDER_ALLOW_INPUT_PROMPTS'] = '1'

    session = PromptSession()

    ConsoleMain(session).execute()
    print('GoodBye!')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Something went wrong!!")
        print(e)
        sys.exit(1)

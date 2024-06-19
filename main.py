from dotenv import load_dotenv

from db_rewind.console.menu.main import Main as ConsoleMain

from prompt_toolkit import PromptSession


def main():
    load_dotenv()

    session = PromptSession()

    ConsoleMain(session).execute()
    print('GoodBye!')


if __name__ == "__main__":
    main()

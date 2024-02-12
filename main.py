from dotenv import load_dotenv

from console.menu.main import Main as ConsoleMain

from prompt_toolkit import PromptSession


def main():
    load_dotenv()

    session = PromptSession()

    ConsoleMain(session).execute(
        session=session,
    )
    print('GoodBye!')


if __name__ == "__main__":
    main()

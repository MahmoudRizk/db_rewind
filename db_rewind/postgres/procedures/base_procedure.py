import abc
import os
import pwd
import sys
from multiprocessing import Process, Pipe
from typing import Optional

from prompt_toolkit import PromptSession, print_formatted_text, HTML

from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO

class BaseProcedure(metaclass=abc.ABCMeta):

    def __init__(self):
        self.prompt_session = PromptSession()
        self.next_procedure: Optional[BaseProcedure] = None

    @abc.abstractmethod
    def _execute(self) -> OsResponseDTO:
        pass

    def execute_as_user(self) -> Optional[str]:
        return None

    def execute(self) -> OsResponseDTO:
        res = self._execute_in_new_process()
        if not res.is_success():
            self.print_error(res.get_error_message())

            if self.can_user_handle_error_manually():
                self._user_handle_error_manually()

            return res

        if not self.next_procedure:
            return res

        return self.next_procedure.execute()

    def next(self, next: "BaseProcedure") -> "BaseProcedure":
        self.next_procedure = next
        return self

    def can_user_handle_error_manually(self) -> bool:
        return True

    def _switch_user(self, user_name: Optional[str]) -> None:
        if not user_name:
            return

        self.print_info(f"Switching to user: {user_name}")
        user = pwd.getpwnam(user_name)

        os.setgid(user.pw_uid)
        os.setuid(user.pw_uid)

    def _execute_in_new_process(self) -> OsResponseDTO:
        parent_stdin_fileno = sys.stdin.fileno()

        def _new_process_wrapper():
            # Is used for opening input using parent's process stdin.
            # This is a workaround to be able to open get input from user from another process.
            sys.stdin = os.fdopen(parent_stdin_fileno)

            # setting stdin to parent's process stdin for prompt_session.
            self.prompt_session.input.stdin = sys.stdin

            # TODO: handle exceptions.

            self._switch_user(
                self.execute_as_user()
            )

            child_conn.send(self._execute())

        parent_conn, child_conn = Pipe()
        p = Process(target=_new_process_wrapper)
        p.start()
        p.join()

        return parent_conn.recv()

    def _user_handle_error_manually(self) -> OsResponseDTO:
        self.print_message("Something Went Wrong, Please try to fix it manually.")

        user_input = self.prompt_session.prompt("Is issue fixed manually? Y(es) N(o):")

        # TODO: validate user input using lambda.
        if user_input.lower() in {'y', 'yes'}:
            # retry procedure.
            return self.execute()

        return OsResponseDTO(exit_code=1, message=b'', error_message=b'Failed to handle error manually')

    def print_info(self, message: str):
        print_formatted_text(HTML(f"<ansigreen>INFO: {message}</ansigreen>"))

    def print_error(self, message: str):
        print_formatted_text(HTML(f"<ansired>ERROR: {message}</ansired>"))

    def print_message(self, message: str):
        print_formatted_text(message)

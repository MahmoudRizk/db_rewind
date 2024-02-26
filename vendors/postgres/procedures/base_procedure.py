import abc
import os
import pwd
import sys
from multiprocessing import Process, Pipe
from typing import Optional

from prompt_toolkit import PromptSession

from vendors.postgres.os_handler.os_response_dto import OsResponseDTO


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
        if not (res.is_success() and self.next_procedure):
            return res

        return self.next_procedure.execute()

    def next(self, next: "BaseProcedure") -> "BaseProcedure":
        self.next_procedure = next
        return self

    def _switch_user(self, user_name: Optional[str]) -> None:
        if not user_name:
            return

        print(f"Switching to user: {user_name}")
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

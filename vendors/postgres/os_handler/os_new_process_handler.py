import pwd
import os
import sys
from multiprocessing import Process
from multiprocessing import Pipe
from typing import Optional, Callable

from .os_response_dto import OsResponseDTO


class OsNewProcessHandler:
    @staticmethod
    def switch_user(user_name: str) -> None:
        print(f"Switching to user: {user_name}")
        user = pwd.getpwnam(user_name)

        os.setgid(user.pw_uid)
        os.setuid(user.pw_uid)

    @staticmethod
    def in_new_process(as_user=Optional[str]) -> Callable:
        parent_stdin_fileno = sys.stdin.fileno()

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> OsResponseDTO:
                def new_process_func_wrapper(*args, **kwargs) -> None:
                    # Is used for opening input using parent's process stdin.
                    sys.stdin = os.fdopen(parent_stdin_fileno)

                    # TODO: handle exceptions.
                    if as_user:
                        OsNewProcessHandler.switch_user(as_user)

                    child_conn.send(func(*args, **kwargs))

                parent_conn, child_conn = Pipe()
                p = Process(target=new_process_func_wrapper, args=args, kwargs=kwargs)
                p.start()
                p.join()

                return parent_conn.recv()

            return wrapper

        return decorator

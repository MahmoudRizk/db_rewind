import subprocess

from .os_response_dto import OsResponseDTO


class OsCommandHandler:
    @staticmethod
    def execute(command: str) -> OsResponseDTO:
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        exit_code = proc.wait()
        (out, err) = proc.communicate()

        return OsResponseDTO(exit_code=exit_code, message=out, error_message=err)

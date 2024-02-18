class OsResponseDTO:
    def __init__(self, exit_code: int, message: bytes, error_message: bytes):
        self._exit_code = exit_code
        self._message = message
        self._error_message = error_message

    def get_exit_code(self) -> int:
        return self._exit_code

    def get_message(self) -> str:
        return self._message.decode()

    def get_error_message(self) -> str:
        return self._error_message.decode()

    def is_success(self) -> bool:
        return self._exit_code == 0

    def as_dict(self) -> dict:
        return {
            'exit_code': self.get_exit_code(),
            'message': self.get_message(),
            'error_message': self.get_error_message(),
            'success': self.is_success(),
        }

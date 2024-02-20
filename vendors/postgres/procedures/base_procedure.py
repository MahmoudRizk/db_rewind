import abc
from typing import Optional

from vendors.postgres.os_handler.os_response_dto import OsResponseDTO


class BaseProcedure(metaclass=abc.ABCMeta):
    def __init__(self):
        self.next_procedure: Optional[BaseProcedure] = None

    def execute(self) -> OsResponseDTO:
        res = self._execute()
        if not (res.is_success() and self.next_procedure):
            return res

        return self.next_procedure.execute()

    def next(self, next: "BaseProcedure") -> "BaseProcedure":
        self.next_procedure = next
        return self

    @abc.abstractmethod
    def _execute(self) -> OsResponseDTO:
        pass

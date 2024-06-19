from typing import Callable


class Command:
    def __init__(self, name: str, description: str, callback: Callable):
        self.name: str = name
        self.description: str = description
        self.callback: Callable = callback

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_callback(self) -> Callable:
        return self.callback

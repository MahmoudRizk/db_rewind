import secrets
import string


class RandomStringGenerator:
    @staticmethod
    def generate(length: int = 10) -> str:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(characters) for _ in range(length))
        return random_string

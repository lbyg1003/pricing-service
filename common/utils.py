import re


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_pattern = re.compile(r"^[\w-]+@([\w-]+\.)+[\w]+$")
        return True if email_pattern.match(email) else False
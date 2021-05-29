import uuid
from typing import Dict
from dataclasses import dataclass, field
from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors


@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def to_json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by("email", email)
        except TypeError:
            raise UserErrors.UserNotFoundError("User not found.")

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)
        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorrectPasswordError("Invalid password.")
        return True

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email format is invalid.")

        try:
            cls.find_by_email(email)
            # if succeed, user already exists
            raise UserErrors.UserAlreadyRegisteredError("The email already exists.")
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

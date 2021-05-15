from abc import ABCMeta, abstractmethod
from typing import List, Dict, TypeVar, Type, Union
from common.database import Database

# define a custom data type
T = TypeVar('T', bound="Model")  # bound means T must be a Model or one of its subclasses


class Model(metaclass=ABCMeta):
    """
    The base class for other models.

    @abstractmethod:
    Class inherited from Model class must have a 'to_json' method defined in itself.
    Otherwise when build objects from that child class, it will call the abstract 'to_json' method from here
    and raise the not implemented error.

    Can also put common methods here. So don't need to create the same method under each model.
    EX. The 'all' class method can be used in both Item and Alert class
    """
    collection: str  # collection is going to be defined as a str when creating the class/subclasses, but no value yet
    _id: str

    def __init__(self, *args, **kwargs):  # just to get rid of the warning on 'cls(**ele)'
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.to_json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @abstractmethod
    def to_json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def all(cls: Type[T]) -> List[T]:  # return a list of T
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**ele) for ele in elements_from_db]

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:  # Item.get_by_id() -> Item, Alert.get_by_id() -> Alert
        # return cls(**Database.find_one(cls.collection, {"_id": _id}))
        return cls.find_one_by("_id", _id)  # just a special case of find_one_by

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:  # ex. Item.find_one_by({"url": "xxx"})
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
        return [cls(**ele) for ele in Database.find(cls.collection, {attribute: value})]

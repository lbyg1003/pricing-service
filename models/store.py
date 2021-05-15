import re
import uuid
from typing import Dict
from dataclasses import dataclass, field
from models.model import Model


@dataclass()
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    attrs: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def to_json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "attrs": self.attrs
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}  # url string starts with url_prefix
        return cls.find_one_by("url_prefix", url_regex)  # mongodb supports searching with such regex query

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return a store from an item URL like "https://www.chelseamegastore.com/en/chelsea-track-jacket-blue/"
        :param url: The item's URL
        :return: a Store object
        """
        pattern = re.compile(r"https?://.*?/")
        url_prefix = re.findall(pattern, url)[0]
        return cls.get_by_url_prefix(url_prefix)



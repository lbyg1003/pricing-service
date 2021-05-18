from typing import Dict
import requests
import re
import uuid
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    attrs: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        content = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"}).content
        soup = BeautifulSoup(content, "html.parser")
        txt = soup.find(self.tag_name, self.attrs).text.strip()

        pattern = re.compile(r"\d+,?\d+\.\d*")
        price_list = re.findall(pattern, txt)
        price_list = [float(i.replace(',', '')) for i in price_list]
        self.price = min(price_list)
        return self.price

    def to_json(self) -> Dict:
        return {
            '_id': self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "attrs": self.attrs,
            "price": self.price
        }

    # @classmethod  # we want to use this method in this way: Item.all()
    # def all(cls) -> List:
    #     items_from_db = Database.find("items", {})  # get all from "items" collection (since every item is saved here)
    #
    #     # items_from_db: like a list of Dict
    #     # complex format to create an object for each data point retrieved.
    #     # return [Item(_id=item['_id'],
    #     #              url=item['url'],
    #     #              tag_name=item['tag_name'],
    #     #              attrs=item['attrs'])
    #     #         for item in items_from_db]
    #
    #     # simple format
    #     return [cls(**item) for item in items_from_db]  # list of Item object


import uuid
from typing import Dict
from dataclasses import dataclass, field
from models.item import Item
from models.model import Model


@dataclass(eq=False)  # disallow comparison between Alert objects (alert_1 == alert_2), since it doesn't make any sense
class Alert(Model):
    collection: str = field(init=False, default="alerts")  # make collection as a Class attribute
    name: str
    item_id: str
    price_limit: float
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)  # pass in a function, not a function callable

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)

    def to_json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")

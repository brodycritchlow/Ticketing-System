"""
Contains whatever we need to store about users, this is including balances, tickets owned, etc.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Any

from card import Card
from exceptions import RejectedError

class User(BaseModel):
    creation_date: datetime
    username: str
    tickets: list[Any] # Would love to reomve this Any if possible.
    balance: int
    cards: list[Card]

    def remove_funds(self, amount, **discounts) -> None | False:
        all_stacking_discounts = {k: v for k, v in discounts.items() if v[1] == True}
        non_stacking_discounts = {k: v for k, v in discounts.items() if v[1] == False}

        if len(all_stacking_discounts) >= 1:
            # we know we have atleast one stacking
            for discount in all_stacking_discounts.items():
                amount *= discount[0] # we dont really need stacks
        else:
            maximum_nonstacking = max(non_stacking_discounts.values(), key=lambda item: item[0])
            amount *= maximum_nonstacking[0] # max return type is list[int, bool]

        if self.balance >= amount:
            self.balance -= amount
            return

        try:
            self.cards[0].charge(amount - self.balance)
            self.balance = 0 # Take full amount of balance, charge rest on card.
        except RejectedError:
            return False
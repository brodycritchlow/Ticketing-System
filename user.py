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
        discount_applied = False

        for code, pns in discounts.items(): # pns means Percent and Stacks
            for perc, stacks in pns:
                if stacks and discount_applied == True:
                    amount *= 1 - perc
                elif not stacks and discount_applied == False:
                    # We assume non-stacking discounts are sorted at the back.
                    amount *= 1 - perc
                else:
                    continue

        if self.balance >= amount:
            self.balance -= amount
            return

        try:
            self.cards[0].charge(amount - self.balance)
            self.balance = 0 # Take full amount of balance, charge rest on card.
        except RejectedError:
            return False
"""
Contains whatever we need for our ticketing printout system,
and contains all data about the ticket, this includes (but isn't limited to)
    - Seat
        - Row
        - Number
    - Game 
        - Game ID
        - Game Name
    - Purchase Price
    - Purchase Date (MM/DD/YYYY)
"""

from datetime import datetime
from typing import Self
from pydantic import BaseModel

from database_helpers import get_next_available
from exceptions import AlreadyOwnedError, RejectedError

from user import User

class GenericTicket(BaseModel):
    seat: tuple[str, int] # Seat will look something like (A, 23)
    event: tuple[int, str] # Game will look something like (9381023, "MLB - Orioles vs Dodgers")
    purchase_price: int
    purchase_date: datetime | None
    owner: User | None

    def purchase_ticket(self, purchasing_user, **discounts) -> Self:
        transid = get_next_available()
        
        if self.owner is not None:
            # Someone already owns ticket
            raise AlreadyOwnedError("\
                Someone has already purchased this ticket.\
                Report to customer service if you have a problem, your transaction id is: {transid}.\
            ")
        self.owner = purchasing_user
        
        if not purchasing_user.wallet.remove_funds(self.purchase_price, **discounts):
            self.owner = None
            raise RejectedError(f"Card was rejected while trying to purchase {self.event[1]}")
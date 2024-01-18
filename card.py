from pydantic import BaseModel
from datetime import datetime

class Card(BaseModel):
    pan: int
    cardholder: str
    billing_address: str
    expiration_date: datetime

    def charge(self):
        return NotImplemented
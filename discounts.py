from pydantic import BaseModel, PositiveInt

class StackingDiscount(BaseModel):
    discount_amount: PositiveInt
    stacking: bool | int = True

class NonStackingDiscount(BaseModel):
    discount_amount: PositiveInt
    stacking: bool | int = False

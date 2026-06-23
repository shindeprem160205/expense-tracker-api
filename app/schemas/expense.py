from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryResponse


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, decimal_places=2)
    category_id: int
    description: str | None = Field(default=None, max_length=2000)
    expense_date: date


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    category_id: int | None = None
    description: str | None = Field(default=None, max_length=2000)
    expense_date: date | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: Decimal
    description: str | None
    expense_date: date
    category_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse

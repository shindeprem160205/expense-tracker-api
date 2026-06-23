from decimal import Decimal

from pydantic import BaseModel, Field


class MonthlySummaryItem(BaseModel):
    year: int
    month: int
    total_amount: Decimal
    expense_count: int


class CategorySpendingItem(BaseModel):
    category_id: int
    category_name: str
    total_amount: Decimal
    expense_count: int
    percentage: Decimal = Field(description="Share of total spending as a percentage")


class TotalExpensesResponse(BaseModel):
    total_amount: Decimal
    expense_count: int
    start_date: str | None = None
    end_date: str | None = None

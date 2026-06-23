from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas.analytics import CategorySpendingItem, MonthlySummaryItem, TotalExpensesResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/monthly-summary", response_model=list[MonthlySummaryItem])
def monthly_summary(
    year: int | None = Query(default=None, ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MonthlySummaryItem]:
    return AnalyticsService.monthly_summary(db, current_user, year=year)


@router.get("/category-spending", response_model=list[CategorySpendingItem])
def category_spending(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CategorySpendingItem]:
    return AnalyticsService.category_spending(
        db, current_user, start_date=start_date, end_date=end_date
    )


@router.get("/total", response_model=TotalExpensesResponse)
def total_expenses(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TotalExpensesResponse:
    return AnalyticsService.total_expenses(
        db, current_user, start_date=start_date, end_date=end_date
    )

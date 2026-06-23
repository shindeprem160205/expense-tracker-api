from datetime import date
from decimal import Decimal

from sqlalchemy import and_, extract, func, select
from sqlalchemy.orm import Session

from app.models import Category, Expense, User
from app.schemas.analytics import CategorySpendingItem, MonthlySummaryItem, TotalExpensesResponse


class AnalyticsService:
    @staticmethod
    def _date_filters(query, start_date: date | None, end_date: date | None):
        if start_date is not None:
            query = query.where(Expense.expense_date >= start_date)
        if end_date is not None:
            query = query.where(Expense.expense_date <= end_date)
        return query

    @staticmethod
    def monthly_summary(
        db: Session,
        user: User,
        *,
        year: int | None = None,
    ) -> list[MonthlySummaryItem]:
        query = (
            select(
                extract("year", Expense.expense_date).label("year"),
                extract("month", Expense.expense_date).label("month"),
                func.coalesce(func.sum(Expense.amount), 0).label("total_amount"),
                func.count(Expense.id).label("expense_count"),
            )
            .where(Expense.user_id == user.id)
            .group_by("year", "month")
            .order_by("year", "month")
        )

        if year is not None:
            query = query.where(extract("year", Expense.expense_date) == year)

        rows = db.execute(query).all()
        return [
            MonthlySummaryItem(
                year=int(row.year),
                month=int(row.month),
                total_amount=Decimal(str(row.total_amount)),
                expense_count=int(row.expense_count),
            )
            for row in rows
        ]

    @staticmethod
    def category_spending(
        db: Session,
        user: User,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[CategorySpendingItem]:
        join_conditions = [
            Expense.category_id == Category.id,
            Expense.user_id == user.id,
        ]
        if start_date is not None:
            join_conditions.append(Expense.expense_date >= start_date)
        if end_date is not None:
            join_conditions.append(Expense.expense_date <= end_date)

        query = (
            select(
                Category.id,
                Category.name,
                func.coalesce(func.sum(Expense.amount), 0).label("total_amount"),
                func.count(Expense.id).label("expense_count"),
            )
            .outerjoin(Expense, and_(*join_conditions))
            .where(Category.user_id == user.id)
            .group_by(Category.id, Category.name)
            .order_by(func.coalesce(func.sum(Expense.amount), 0).desc())
        )

        rows = db.execute(query).all()
        grand_total = sum(Decimal(str(row.total_amount)) for row in rows)

        return [
            CategorySpendingItem(
                category_id=row.id,
                category_name=row.name,
                total_amount=Decimal(str(row.total_amount)),
                expense_count=int(row.expense_count),
                percentage=(
                    (Decimal(str(row.total_amount)) / grand_total * 100).quantize(Decimal("0.01"))
                    if grand_total > 0
                    else Decimal("0.00")
                ),
            )
            for row in rows
        ]

    @staticmethod
    def total_expenses(
        db: Session,
        user: User,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> TotalExpensesResponse:
        query = select(
            func.coalesce(func.sum(Expense.amount), 0).label("total_amount"),
            func.count(Expense.id).label("expense_count"),
        ).where(Expense.user_id == user.id)

        query = AnalyticsService._date_filters(query, start_date, end_date)
        row = db.execute(query).one()

        return TotalExpensesResponse(
            total_amount=Decimal(str(row.total_amount)),
            expense_count=int(row.expense_count),
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None,
        )

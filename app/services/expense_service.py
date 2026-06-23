from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Category, Expense, User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


class ExpenseService:
    @staticmethod
    def _get_user_category(db: Session, user_id: int, category_id: int) -> Category | None:
        return db.scalar(
            select(Category).where(Category.id == category_id, Category.user_id == user_id)
        )

    @staticmethod
    def create_expense(db: Session, user: User, expense_data: ExpenseCreate) -> Expense:
        category = ExpenseService._get_user_category(db, user.id, expense_data.category_id)
        if not category:
            raise ValueError("Category not found")

        expense = Expense(
            user_id=user.id,
            category_id=expense_data.category_id,
            title=expense_data.title,
            amount=expense_data.amount,
            description=expense_data.description,
            expense_date=expense_data.expense_date,
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return db.scalar(
            select(Expense)
            .options(joinedload(Expense.category))
            .where(Expense.id == expense.id)
        )

    @staticmethod
    def list_expenses(
        db: Session,
        user: User,
        *,
        category_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Expense]:
        query = (
            select(Expense)
            .options(joinedload(Expense.category))
            .where(Expense.user_id == user.id)
            .order_by(Expense.expense_date.desc(), Expense.id.desc())
        )

        if category_id is not None:
            query = query.where(Expense.category_id == category_id)
        if start_date is not None:
            query = query.where(Expense.expense_date >= start_date)
        if end_date is not None:
            query = query.where(Expense.expense_date <= end_date)

        return list(db.scalars(query.offset(skip).limit(limit)).all())

    @staticmethod
    def get_expense(db: Session, user: User, expense_id: int) -> Expense | None:
        return db.scalar(
            select(Expense)
            .options(joinedload(Expense.category))
            .where(Expense.id == expense_id, Expense.user_id == user.id)
        )

    @staticmethod
    def update_expense(
        db: Session, user: User, expense_id: int, expense_data: ExpenseUpdate
    ) -> Expense | None:
        expense = ExpenseService.get_expense(db, user, expense_id)
        if not expense:
            return None

        update_data = expense_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            category = ExpenseService._get_user_category(db, user.id, update_data["category_id"])
            if not category:
                raise ValueError("Category not found")

        for field, value in update_data.items():
            setattr(expense, field, value)

        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def delete_expense(db: Session, user: User, expense_id: int) -> bool:
        expense = ExpenseService.get_expense(db, user, expense_id)
        if not expense:
            return False
        db.delete(expense)
        db.commit()
        return True

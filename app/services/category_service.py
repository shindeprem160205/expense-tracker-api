from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, User
from app.schemas.category import CategoryCreate


class CategoryService:
    @staticmethod
    def list_categories(db: Session, user: User) -> list[Category]:
        return list(
            db.scalars(
                select(Category).where(Category.user_id == user.id).order_by(Category.name)
            ).all()
        )

    @staticmethod
    def create_category(db: Session, user: User, category_data: CategoryCreate) -> Category:
        existing = db.scalar(
            select(Category).where(
                Category.user_id == user.id,
                Category.name == category_data.name,
            )
        )
        if existing:
            raise ValueError("Category already exists")

        category = Category(name=category_data.name, user_id=user.id)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

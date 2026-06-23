from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserCreate
from app.utils.security import create_access_token, get_password_hash, verify_password

DEFAULT_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Education",
    "Other",
]


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing = db.scalar(select(User).where(User.email == user_data.email))
        if existing:
            raise ValueError("Email already registered")

        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
        )
        db.add(user)
        db.flush()

        from app.models import Category

        for name in DEFAULT_CATEGORIES:
            db.add(Category(name=name, user_id=user.id))

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        user = db.scalar(select(User).where(User.email == email))
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_token_for_user(user: User) -> str:
        return create_access_token(subject=str(user.id))

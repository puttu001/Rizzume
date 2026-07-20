from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Every model in app/models/ inherits from this. Alembic's env.py points
    at Base.metadata for autogenerate — import new model modules there once
    they exist so alembic can see their tables."""

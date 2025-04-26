import pytest
from sqlmodel import Session, SQLModel
from app.core.config import settings
from app.models.dataset import SalesRecord

@pytest.fixture(autouse=True)
def clean_database():
    """Limpia la base de datos antes de cada prueba."""
    with Session(settings.engine) as session:
        session.query(SalesRecord).delete()
        session.commit()

        
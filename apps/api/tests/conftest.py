import pytest
from sqlalchemy import text  # Importa text()
from app.models.dataset import SalesRecord
from app.core.config import settings
from sqlmodel import Session

@pytest.fixture(autouse=True)
def clean_database():
    # tests/conftest.py
# @pytest.fixture(autouse=True)
# def clean_database():
#     ...
    """Limpia la base de datos antes de cada prueba."""
    with Session(settings.engine) as session:
        session.exec(text("DELETE FROM salesrecord"))  # Usa text()
        session.commit()


@pytest.fixture
def sample_csv():
    """CSV válido."""
    return b"fecha,SKU,cantidad,precio_unitario\n2024-01-01,ABC123,10,19.99\n2024-01-02,DEF456,5,9.99"

@pytest.fixture
def invalid_csv():
    """CSV con datos inválidos."""
    return b"fecha,SKU,cantidad,precio_unitario\n2024-01-01,ABC123,-10,abc"

@pytest.fixture
def large_csv():
    """CSV con 100,000 filas."""
    data = "fecha,SKU,cantidad,precio_unitario\n"
    data += "\n".join([f"2024-01-01,ABC{i},{i},19.99" for i in range(100_000)])
    return data.encode()

@pytest.fixture
def malicious_csv():
    """CSV malicioso (ejemplo: intento de SQL Injection)."""
    return b"fecha,SKU,cantidad,precio_unitario\n2024-01-01,ABC123,10,19.99; DROP TABLE salesrecord;--"

@pytest.fixture
def valid_token():
    """Token de prueba."""
    from app.core.security import SECRET_KEY, ALGORITHM
    from datetime import timedelta, datetime
    data = {"sub": "test_user"}
    expires = datetime.utcnow() + timedelta(minutes=10)
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

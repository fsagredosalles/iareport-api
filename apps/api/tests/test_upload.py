import os
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.config import settings
from sqlmodel import Session, select
from app.models.dataset import SalesRecord

# Cliente de prueba para FastAPI
client = TestClient(app)

@pytest.fixture
def sample_csv():
    """Fixture que simula un archivo CSV válido."""
    return b"fecha,SKU,cantidad,precio_unitario\n2024-01-01,ABC123,10,19.99\n2024-01-02,DEF456,5,9.99\n"
def invalid_csv():
    """Fixture que simula un archivo CSV inválido."""
    return b"fecha,SKU,cantidad,precio_unitario\n2024-01-01,ABC123,-10,abc\n"

def test_upload_valid_file(sample_csv):
    """Prueba la carga de un archivo válido."""
    response = client.post(
        "/api/v1/upload-file",
        files={"file": ("data.csv", sample_csv, "text/csv")},
    )
    assert response.status_code == 200
    report_id = response.json()["report_id"]

    # Consultar registros en la base de datos
    with Session(settings.engine) as session:
        statement = select(SalesRecord).where(SalesRecord.report_id == report_id)
        records = session.exec(statement).all()

    # Verificar que se hayan insertado los registros correctamente
    assert len(records) == 2
    assert records[0].sku == "ABC123"
    assert records[1].sku == "DEF456"


def test_upload_invalid_file(invalid_csv):
    """Prueba la carga de un archivo inválido."""
    response = client.post(
        "/api/v1/upload-file",
        files={"file": ("invalid.csv", invalid_csv, "text/csv")},
    )
    assert response.status_code == 400
def large_csv():
    """CSV con 100,000 filas."""
    data = "fecha,SKU,cantidad,precio_unitario\n" + "\n".join(
        [f"2024-01-01,ABC{i},{i},19.99" for i in range(100_000)]
    )
    return data.encode()

def test_upload_large_file(large_csv):
    response = client.post(
        "/api/v1/upload-file",
        files={"file": ("large.csv", large_csv, "text/csv")},
    )
    assert response.status_code == 200
    assert "report_id" in response.json()
def malicious_csv():
    return b"fecha,SKU,cantidad,precio_unitario\n2024-01-01,ABC123,10,19.99\n2024-01-01,ABC123,10,19.99; DROP TABLE salesrecord;--"

def test_upload_malicious_file(malicious_csv):
    response = client.post(
        "/api/v1/upload-file",
        files={"file": ("malicious.csv", malicious_csv)},
    )
    assert response.status_code == 400  # Debe rechazar SQL Injection

print("Ejecutando tests/test_upload.py")


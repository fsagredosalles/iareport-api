# tests/test_manual.py
import sys
from pathlib import Path
# Añadir la raíz del proyecto al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.models.dataset import SalesRecord
from sqlmodel import Session
from datetime import datetime

def test_manual_insert():
    with Session(settings.engine) as session:
        record = SalesRecord(
            report_id="test-123",
            fecha=datetime.now(),
            sku="ABC123",
            cantidad=10,
            precio_unitario=19.99
        )
        session.add(record)
        session.commit()
        print("Registro insertado manualmente.")
# scripts/reset_database.py
from app.models.dataset import create_db_and_tables
from app.core.config import settings

def reset_database():
    """Reinicia la base de datos."""
    from sqlmodel import SQLModel
    print("Eliminando tablas existentes...")
    SQLModel.metadata.drop_all(settings.engine)
    print("Tablas eliminadas.")
    print("Creando tablas nuevas...")
    create_db_and_tables()
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    reset_database()

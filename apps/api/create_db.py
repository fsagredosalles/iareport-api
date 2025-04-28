from sqlalchemy import create_engine
from sqlmodel import SQLModel
from app.models.dataset import SalesRecord  # Importa el modelo
from app.core.config import settings

# Eliminar la base de datos si existe (opcional)
try:
    import os
    os.remove("iareport.db")
    print("Base de datos antigua eliminada.")
except FileNotFoundError:
    print("No se encontró una base de datos antigua.")

# Crear el motor de base de datos
engine = create_engine(settings.database_url)
SQLModel.metadata.create_all(engine)  # Crea todas las tablas

# Crear todas las tablas
def create_tables():
    print("Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    create_tables()
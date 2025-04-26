from pydantic_settings import BaseSettings
from pathlib import Path
from sqlmodel import create_engine

class Settings(BaseSettings):
    app_name: str = "IAReport API"
    debug: bool = True
    database_url: str = "sqlite:///./iareport.db"
    data_dir: str = "./data"  # Directorio para Parquet

    model_config = {
        "env_file": ".env",  # Usar ConfigDict en lugar de class Config
    }

    @property
    def engine(self):
        """Crea y retorna el motor de base de datos."""
        print(f"Creado motor de base de datos con URL: {self.database_url}")
        return create_engine(self.database_url)

# Crear una instancia global de Settings
settings = Settings()

# Crear directorio de datos si no existe
Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
print("Cargando configuración desde app/core/config.py")

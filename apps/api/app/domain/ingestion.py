import pandas as pd
from fastapi import UploadFile
from app.models.dataset import validate_dataframe, SalesRecord
from app.core.config import settings
from uuid import uuid4
import os
from sqlmodel import Session

def process_upload(file: UploadFile) -> str:
    """
    Procesa un archivo subido:
    - Lee el archivo CSV/XLSX.
    - Valida los datos con Pandera.
    - Almacena los datos en SQLite y guarda una versión en Parquet.
    - Retorna un report_id único.
    """
    print(f"Procesando archivo: {file.filename}")
    
    # Leer el archivo
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file.file)
        else:
            raise ValueError("Formato de archivo no soportado. Usa CSV o Excel.")
        
        print("Archivo leído correctamente:")
        print(df.head())
    except Exception as e:
        raise ValueError(f"Error leyendo el archivo: {str(e)}")
    
    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower()
    print("Nombres de columnas normalizados:")
    print(df.columns)
    
    # Validar con Pandera
    try:
        df_validated = validate_dataframe(df)
        print("Datos validados correctamente.")
    except Exception as e:
        raise ValueError(f"Datos inválidos: {str(e)}")
    
    # Generar report_id único
    report_id = str(uuid4())
    print(f"Generado report_id único: {report_id}")
    
    # Convertir DataFrame a registros SQLModel
    records = [
        SalesRecord(
            report_id=report_id,
            fecha=row["fecha"],
            sku=row["sku"],
            cantidad=row["cantidad"],
            precio_unitario=row["precio_unitario"]
        )
        for _, row in df_validated.iterrows()
    ]
        
    # Debugging: Mostrar datos antes de guardar
    print("Datos a insertar:")
    print(df_validated.to_dict(orient="records"))
    
    # Guardar en SQLite
    # Guardar en SQLite
    try:
        with Session(settings.engine) as session:
            session.add_all(records)
            session.commit()
        print("Datos guardados en SQLite correctamente.")
    except Exception as e:
        raise RuntimeError(f"Error al guardar en SQLite: {str(e)}")
    
    # Guardar versión Parquet en disco
    try:
        os.makedirs(settings.data_dir, exist_ok=True)  # Asegurarse de que el directorio exista
        parquet_path = os.path.join(settings.data_dir, f"{report_id}.parquet")
        print(f"Guardando archivo Parquet en: {parquet_path}")
        df_validated.to_parquet(parquet_path)
        print("Archivo Parquet guardado correctamente.")
    except Exception as e:
        raise RuntimeError(f"Error al guardar archivo Parquet: {str(e)}")
    
    return report_id

print("Importando process_upload desde app/domain/ingestion.py")
print("Importando settings desde app/core/config.py")
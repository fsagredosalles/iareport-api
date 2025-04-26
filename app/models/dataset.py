import pandas as pd  # Agrega esta línea
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from pandera import DataFrameSchema, Column, Check, dtypes
from typing import List
from datetime import datetime

# === MODELOS PYDANTIC PARA RESPUESTAS API ===
class FileResponse(BaseModel):
    filename: str
    rows: int
    columns: List[str]

class AnalysisRequest(BaseModel):
    file_id: str
    parameters: dict

# === MODELO SQLMODEL PARA LA BASE DE DATOS ===
class SalesRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    report_id: str = Field(index=True)  # Sin unique=True
    fecha: datetime
    sku: str
    cantidad: int
    precio_unitario: float

# === ESQUEMA PANDERA PARA VALIDACIÓN ===
sales_schema = DataFrameSchema(
    {
        "fecha": Column(dtypes.DateTime, coerce=True, required=True),
        "sku": Column(dtypes.String, checks=Check.str_matches(r"^[A-Z0-9]+$"), required=True),
        "cantidad": Column(dtypes.Int, checks=Check.greater_than_or_equal_to(0), required=True),
        "precio_unitario": Column(dtypes.Float, checks=Check.greater_than(0), required=True),
    },
    strict=True,
    coerce=True,
)

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return sales_schema.validate(df)


    
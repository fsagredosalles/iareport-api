# apps/api/app/domain/validation.py
import pandera as pa
from pandera.typing import Series

class SalesDataSchema(pa.DataFrameModel):
    fecha: Series[pa.DateTime] = pa.Field(coerce=True)
    sku: Series[str] = pa.Field(str_length={"min": 5, "max": 10})
    cantidad: Series[int] = pa.Field(ge=0)
    precio_unitario: Series[float] = pa.Field(ge=0.01)

    class Config:
        strict = True  # No permite columnas extras
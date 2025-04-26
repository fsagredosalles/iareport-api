from fastapi import APIRouter, UploadFile, HTTPException, status
from app.domain.ingestion import process_upload

router = APIRouter()

@router.post("/upload-file", tags=["Upload"])  # Mantén el tag aquí
async def upload_file(file: UploadFile):
    # Validar tamaño máximo (5 MB)
    if file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Archivo demasiado grande (máximo 5 MB).")
    
    # Procesar el archivo
    try:
        report_id = process_upload(file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return {"report_id": report_id}
    
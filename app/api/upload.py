import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido. Use JPG, PNG, GIF ou WEBP.")

    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo 10MB.")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    from app.config import settings
    public_url = f"{settings.API_PUBLIC_URL}/api/upload/{filename}"
    return {"url": f"/api/upload/{filename}", "public_url": public_url, "filename": filename}


@router.get("/{filename}")
async def get_image(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagem não encontrada.")
    return FileResponse(filepath)

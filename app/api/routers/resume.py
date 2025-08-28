import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from docx import Document
from app.core.security import get_current_user
from app.schemas import auth

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), current_user: auth.UserLogin = Depends(get_current_user)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    contents = await file.read()
    document = Document(io.BytesIO(contents))

    text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])

    return {"filename": file.filename, "content": text}

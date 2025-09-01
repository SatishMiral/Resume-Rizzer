import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from docx import Document
from app.core.security import get_current_user
from app.schemas import auth
from app.services.resume.resume import parse_resume_docx  

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: auth.UserLogin = Depends(get_current_user)
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    contents = await file.read()
    document = Document(io.BytesIO(contents))
    text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])

    return {"filename": file.filename, "content": text}


@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    current_user: auth.UserLogin = Depends(get_current_user)
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    # Save uploaded content in memory
    contents = await file.read()
    with io.BytesIO(contents) as tmp:
        # Use parser to generate JSON
        resume_json = parse_resume_docx(tmp)

    return {"filename": file.filename, "parsed_resume": resume_json}

import io
import tempfile
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from docx import Document
from app.core.security import get_current_user
from app.schemas import auth
from app.services.resume.resume import parse_resume_docx
from app.services.resume.tailor import tailor_resume_with_jd  
from app.services.resume.generator import generate_resume_docx, convert_to_pdf
from app.services.resume.replacer import replace_sentences_in_docx, replace_and_style

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

@router.post("/replace_text/")
async def replace_text(
    file: UploadFile = File(...),
    from_sentence: str = Form(...),
    to_sentence: str = Form(...),
    bold_words: str = Form(""),   # comma-separated
    italic_words: str = Form("")  # comma-separated
):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_in:
        tmp_in.write(await file.read())
        tmp_in.flush()
        input_path = tmp_in.name

    # Load document
    doc = Document(input_path)

    # Convert comma-separated lists into Python lists
    bold_list = [w.strip() for w in bold_words.split(",") if w.strip()]
    italic_list = [w.strip() for w in italic_words.split(",") if w.strip()]

    # Replace and style
    replace_and_style(doc, from_sentence, to_sentence, bold_list, italic_list)

    # Save updated file
    output_path = input_path.replace(".docx", "_updated.docx")
    doc.save(output_path)

    return FileResponse(output_path, filename="updated_resume.docx")

@router.post("/tailor")
async def tailor_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: auth.UserLogin = Depends(get_current_user)
):
    if not resume.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    # Save uploaded resume temporarily
    contents = await resume.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_in:
        tmp_in.write(contents)
        input_docx = tmp_in.name

    # Parse resume into JSON
    original_json = parse_resume_docx(io.BytesIO(contents))

    # Tailor resume with GPT
    tailored_json = tailor_resume_with_jd(original_json, job_description, use_demo=True)

    # Replace sentences in original DOCX
    output_docx = input_docx.replace(".docx", "_tailored.docx")
    replace_sentences_in_docx(input_docx, original_json, tailored_json, output_docx)

    return FileResponse(
        output_docx,
        media_type="application/docx",
        filename="tailored_resume.docx"
    )
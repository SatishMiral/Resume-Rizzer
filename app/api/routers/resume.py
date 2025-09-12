import io
import tempfile
import json
from fastapi.responses import FileResponse, JSONResponse
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from docx import Document
from app.core.security import get_current_user
from app.schemas import auth
from app.services.resume.replacer import replace_and_style
from app.services.resume.parser import extract_sentences_regex

router = APIRouter(prefix="/resume", tags=["Resume"])

# Extract sentences from docx
@router.post("/extract_sentences")
async def parse_resume(
    file: UploadFile = File(...),
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """
    Extract sentences from the uploaded `.docx` resume.
    """
    # Step 1: Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_in:
        tmp_in.write(await file.read())
        tmp_in.flush()
        input_path = tmp_in.name

    # Step 2: Extract sentences from the document
    result = extract_sentences_regex(input_path)

    # Step 3: Return the structured JSON response
    return JSONResponse(content=result)


# Replace whole sentences 
@router.post("/replace_sentences")
async def replace_text(
    file: UploadFile = File(...),
    from_sentence: str = Form(...),
    to_sentence: str = Form(...),
    bold_words: str = Form(""),   # comma-separated
    italic_words: str = Form(""),  # comma-separated
    current_user: auth.UserLogin = Depends(get_current_user)
):
    '''
    Replace whole sentences using \n
    `from sentence` the old sentence \n
    `to sentence` the new sentence \n
    `bold words` comma seperated \n
    `italic words` comma seperated
    '''
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


# Tailor Resume
@router.post("/tailor_resume")
async def apply_changes(
    file: UploadFile = File(...),
    changes_json: str = Form(...),
    current_user: auth.UserLogin = Depends(get_current_user)
):
    '''
    Tailor Resume with the response recieved from LLM \n
    Upload `.docx` \n
    Upload `changes_json` - This is a dummy LLM response. \n
    The sentences which needs to be changed in the Resume in JSON format
    '''
    # Save uploaded docx
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_in:
        tmp_in.write(await file.read())
        tmp_in.flush()
        input_path = tmp_in.name

    doc = Document(input_path)

    # Load JSON changes
    changes = json.loads(changes_json)

    # Apply changes
    for change in changes.get("sentences", []):
        replace_and_style(
            doc,
            from_sentence=change["from_sentence"],
            to_sentence=change["to_sentence"],
            bold_words=change.get("bold_words", []),
            italic_words=change.get("italic_words", [])
        )

    # Save updated file
    output_path = input_path.replace(".docx", "_updated.docx")
    doc.save(output_path)

    return FileResponse(output_path, filename="updated_resume.docx")
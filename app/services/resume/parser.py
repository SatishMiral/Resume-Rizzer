from docx import Document
import re

def split_into_sentences(text: str):
    # Very simple sentence splitter (could be improved with nltk/spacy)
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

def parse_resume_docx(file) -> dict:
    """
    Parse a DOCX resume into JSON with sections -> list of sentences.
    """
    doc = Document(file)

    resume_json = {}
    current_section = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Detect headings (basic rule: all caps or ends with colon)
        if text.isupper() or text.endswith(":"):
            current_section = text.strip(":").title()
            resume_json[current_section] = []
            continue

        if current_section:
            sentences = split_into_sentences(text)
            resume_json[current_section].extend(sentences)

    return resume_json

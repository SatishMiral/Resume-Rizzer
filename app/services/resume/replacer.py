from docx import Document
import difflib

def replace_sentences_in_docx(input_docx, original_json, tailored_json, output_docx):
    """
    Replace only modified sentences in the original DOCX.
    """
    doc = Document(input_docx)

    # Build mapping: original -> tailored
    replacements = {}
    for section, sentences in original_json.items():
        if section in tailored_json:
            for old, new in zip(sentences, tailored_json[section]):
                if old.strip() != new.strip():
                    replacements[old.strip()] = new.strip()

    # Replace in document
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        for old, new in replacements.items():
            # Fuzzy match (ignore whitespace differences)
            if difflib.SequenceMatcher(None, text, old).ratio() > 0.8:
                para.text = para.text.replace(old, new)

    doc.save(output_docx)

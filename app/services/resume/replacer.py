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

def replace_and_style(doc, from_sentence, to_sentence, bold_words=None, italic_words=None):
    bold_words = bold_words or []
    italic_words = italic_words or []

    for para in doc.paragraphs:
        if from_sentence in para.text:
            # Clear the paragraph text (remove old runs)
            for run in para.runs:
                run.text = ""

            # Add styled replacement text word by word
            for word in to_sentence.split(" "):
                run = para.add_run(word + " ")
                clean_word = word.strip(",.!?;:")

                if clean_word in bold_words:
                    run.bold = True
                if clean_word in italic_words:
                    run.italic = True

    # Also check inside tables 
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if from_sentence in cell.text:
                    # Clear and rebuild cell
                    cell.text = ""
                    para = cell.add_paragraph()
                    for word in to_sentence.split(" "):
                        run = para.add_run(word + " ")
                        clean_word = word.strip(",.!?;:")
                        if clean_word in bold_words:
                            run.bold = True
                        if clean_word in italic_words:
                            run.italic = True
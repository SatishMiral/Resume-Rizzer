from docx import Document
from docx2pdf import convert

def generate_resume_docx(resume_json: dict, template_docx: str, output_docx: str):
    """
    Fill a DOCX template with tailored resume content.
    Template must have placeholders like {{SUMMARY}}, {{SKILLS}}, etc.
    """
    doc = Document(template_docx)

    for para in doc.paragraphs:
        if "{{SUMMARY}}" in para.text:
            para.text = resume_json.get("Summary", "")

        if "{{SKILLS}}" in para.text:
            para.text = ", ".join(resume_json.get("Skills", []))

        if "{{EXPERIENCE}}" in para.text:
            para.text = "\n".join(resume_json.get("Experience", []))

        if "{{EDUCATION}}" in para.text:
            para.text = "\n".join(resume_json.get("Education", []))

        if "{{PROJECTS}}" in para.text:
            para.text = "\n".join(resume_json.get("Projects", []))

        if "{{CERTIFICATIONS}}" in para.text:
            para.text = "\n".join(resume_json.get("Certifications", []))

    doc.save(output_docx)

def convert_to_pdf(input_docx: str, output_pdf: str):
    """Convert DOCX to PDF (Windows/macOS with Word, Linux needs LibreOffice)."""
    convert(input_docx, output_pdf)

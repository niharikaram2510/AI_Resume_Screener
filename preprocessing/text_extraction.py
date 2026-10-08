from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file):
    """Extract text from a DOCX file."""
    document = Document(file)
    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text


def extract_text(file):
    """Extract text according to the file type."""

    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file)

    elif filename.endswith(".docx"):
        return extract_docx_text(file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF or DOCX."
        )
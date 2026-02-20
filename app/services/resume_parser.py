"""
Resume parsing utility — extracts text from PDF and DOCX files.
"""
import io
from typing import Any, List, Optional


def extract_text_from_pdf(file_storage: Any) -> str:
    """Extract text from an uploaded PDF file."""
    from pypdf import PdfReader
    reader: Any = PdfReader(io.BytesIO(file_storage.read()))
    text_parts: List[str] = []
    for page in reader.pages:
        page_text: Optional[str] = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_storage: Any) -> str:
    """Extract text from an uploaded DOCX file."""
    import docx  # type: ignore[import-untyped]
    doc: Any = docx.Document(io.BytesIO(file_storage.read()))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def parse_resume(file_storage: Any, filename: str) -> str:
    """Auto-detect format and extract text from resume file."""
    ext: str = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "pdf":
        return extract_text_from_pdf(file_storage)
    elif ext in ("docx", "doc"):
        return extract_text_from_docx(file_storage)
    else:
        raise ValueError(f"Unsupported file format: .{ext}. Please upload a PDF or DOCX file.")

import io

from pypdf import PdfReader


class EmptyResumeError(Exception):
    pass


def extract_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    if not text:
        raise EmptyResumeError("No extractable text found in PDF (scanned image? empty file?)")
    return text
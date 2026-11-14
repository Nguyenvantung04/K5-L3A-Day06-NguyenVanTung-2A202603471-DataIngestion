"""Read and normalize source data."""
import re
import unicodedata
from pathlib import Path
from .models import DocumentPage


def normalize_text(text: str) -> str:
    """Normalize Unicode (NFC), non-breaking spaces, and whitespace without losing structure."""
    if not text:
        return ""
    # Normalize unicode to NFC
    normalized = unicodedata.normalize("NFC", text)
    # Replace non-breaking space and soft hyphens
    normalized = normalized.replace("\xa0", " ").replace("\xad", "")
    # Normalize broken hyphen characters
    normalized = re.sub(r"[­‑–—]", "-", normalized)
    # Clean multiple spaces on the same line
    lines = []
    for line in normalized.splitlines():
        line_clean = re.sub(r"[ \t]+", " ", line).strip()
        lines.append(line_clean)
    # Join lines; keep double newlines for paragraph breaks
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def extract_chapter_and_section(text: str) -> tuple[str, str]:
    """Extract chapter and section metadata from normalized text if present."""
    chapter = ""
    section = ""
    chap_match = re.search(r"(CHƯƠNG\s+[IVXLCDM]+:\s*[^\n]+)", text, re.IGNORECASE)
    if chap_match:
        chapter = chap_match.group(1).title()
    else:
        # Fallback to header format
        header_chap = re.search(r"Chương\s+[IVXLCDM]+:\s*[^\n-]+", text)
        if header_chap:
            chapter = header_chap.group(0).strip()
            
    art_match = re.search(r"(Điều\s+\d+[a-z]?\.\s*[^\n]+)", text)
    if art_match:
        section = art_match.group(1).strip()
    return chapter, section


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    """Extract each physical page using pymupdf/pypdf; keep page number, source, and metadata."""
    if not path.exists():
        raise FileNotFoundError(f"PDF not found at {path}")

    pages: list[DocumentPage] = []
    empty_pages: list[int] = []

    try:
        import pymupdf
        doc = pymupdf.open(str(path))
        for idx, page in enumerate(doc):
            page_num = idx + 1
            raw_text = page.get_text() or ""
            cleaned_text = normalize_text(raw_text)

            if not cleaned_text or len(cleaned_text) < 10:
                empty_pages.append(page_num)
                continue

            chapter, section = extract_chapter_and_section(cleaned_text)
            page_meta = {
                "char_count": len(cleaned_text),
                "line_count": len(cleaned_text.splitlines())
            }
            if chapter:
                page_meta["chapter"] = chapter
            if section:
                page_meta["section"] = section

            pages.append(
                DocumentPage(
                    document_id=document_id,
                    source=source,
                    page=page_num,
                    text=cleaned_text,
                    metadata=page_meta
                )
            )
        doc.close()
    except Exception as e:
        print(f"[Ingestion] Fallback to pypdf due to: {e}")
        import pypdf
        reader = pypdf.PdfReader(str(path))
        for idx, raw_page in enumerate(reader.pages):
            page_num = idx + 1
            raw_text = raw_page.extract_text() or ""
            cleaned_text = normalize_text(raw_text)

            if not cleaned_text or len(cleaned_text) < 10:
                empty_pages.append(page_num)
                continue

            chapter, section = extract_chapter_and_section(cleaned_text)
            page_meta = {
                "char_count": len(cleaned_text),
                "line_count": len(cleaned_text.splitlines())
            }
            if chapter:
                page_meta["chapter"] = chapter
            if section:
                page_meta["section"] = section

            pages.append(
                DocumentPage(
                    document_id=document_id,
                    source=source,
                    page=page_num,
                    text=cleaned_text,
                    metadata=page_meta
                )
            )

    if empty_pages:
        print(f"[Ingestion] Warning: {len(empty_pages)} empty/low-text pages detected: {empty_pages}")
    else:
        print(f"[Ingestion] Successfully extracted all {len(pages)} valid content pages from {path}")

    return pages

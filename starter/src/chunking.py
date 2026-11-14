"""Implement fixed-size and structure-aware chunking."""
import re
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping windows and retain page metadata."""
    text = page.text
    if not text:
        return []

    chunks: list[Chunk] = []
    step = max(1, size - overlap)
    idx = 0
    start = 0

    while start < len(text):
        end = min(start + size, len(text))
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunk_meta = dict(page.metadata)
            chunk_meta.update({
                "chunk_strategy": "fixed_size",
                "char_length": len(chunk_text),
                "window_start": start,
                "window_end": end
            })
            chunk_id = f"{page.document_id}_p{page.page:02d}_fixed_{idx:02d}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=chunk_text,
                    metadata=chunk_meta
                )
            )
            idx += 1

        if end >= len(text):
            break
        start += step

    return chunks


def by_paragraph(page: DocumentPage, max_size: int = 800) -> list[Chunk]:
    """Group paragraphs / legal clauses, split oversized blocks and retain metadata."""
    text = page.text
    if not text:
        return []

    # First split by double newlines or numbered legal clauses (e.g., "\n1. ", "\n2. ", "\na) ")
    raw_blocks = re.split(r"\n\s*\n|(?=\n\d+\.\s+)", text)
    blocks = [b.strip() for b in raw_blocks if b.strip()]

    grouped_blocks: list[str] = []
    current_group: list[str] = []
    current_len = 0

    for block in blocks:
        block_len = len(block)
        # If single block is bigger than max_size, split by sentences
        if block_len > max_size:
            if current_group:
                grouped_blocks.append("\n".join(current_group))
                current_group = []
                current_len = 0
            # Split big block by punctuation
            sentences = re.split(r"(?<=[.;?!])\s+", block)
            sub_group: list[str] = []
            sub_len = 0
            for sent in sentences:
                if sub_len + len(sent) > max_size and sub_group:
                    grouped_blocks.append(" ".join(sub_group))
                    sub_group = [sent]
                    sub_len = len(sent)
                else:
                    sub_group.append(sent)
                    sub_len += len(sent)
            if sub_group:
                grouped_blocks.append(" ".join(sub_group))
        elif current_len + block_len + 1 > max_size:
            grouped_blocks.append("\n".join(current_group))
            current_group = [block]
            current_len = block_len
        else:
            current_group.append(block)
            current_len += block_len + 1

    if current_group:
        grouped_blocks.append("\n".join(current_group))

    chunks: list[Chunk] = []
    for idx, c_text in enumerate(grouped_blocks):
        c_text = c_text.strip()
        if not c_text:
            continue
        chunk_meta = dict(page.metadata)
        chunk_meta.update({
            "chunk_strategy": "by_paragraph",
            "char_length": len(c_text),
            "paragraph_idx": idx
        })
        chunk_id = f"{page.document_id}_p{page.page:02d}_para_{idx:02d}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=c_text,
                metadata=chunk_meta
            )
        )

    return chunks

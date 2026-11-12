
from pathlib import Path
import re
import pymupdf


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"


def clean_text(text: str) -> str:
    """Clean extracted PDF text."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_metadata(filename: str, first_page_text: str) -> dict:
    """Extract document number, revision, and title."""

    doc_match = re.search(
        r"\b([A-Z]{2,5}-(?:SOP|MAN)-[A-Z0-9-]+)\b",
        first_page_text,
        re.IGNORECASE
    )

    if not doc_match:
        doc_match = re.search(
            r"\b([A-Z]{2,5}-(?:SOP|MAN)-[A-Z0-9-]+)\b",
            filename,
            re.IGNORECASE
        )

    revision_match = re.search(
        r"\bRevision\s*(?:No\.?)?\s*[:\-]?\s*(\d+)\b",
        first_page_text,
        re.IGNORECASE
    )

    if not revision_match:
        revision_match = re.search(
            r"\bRev(?:ision)?[-_ ]?0*(\d+)\b",
            filename,
            re.IGNORECASE
        )

    doc_no = doc_match.group(1).upper() if doc_match else "UNKNOWN"

    revision = (
        int(revision_match.group(1))
        if revision_match else None
    )

    lines = [line.strip() for line in first_page_text.splitlines() if line.strip()]

    title = next(
        (
            line for line in lines
            if "standard operating procedure" in line.lower()
            or "manual" in line.lower()
        ),
        Path(filename).stem
    )

    return {
        "doc_no": doc_no,
        "revision": revision,
        "title": title
    }


def split_into_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list:
    """Split text into overlapping chunks."""

    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            split_position = text.rfind(" ", start, end)

            if split_position > start + chunk_size // 2:
                end = split_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list:
    """
    Read PDF files and return searchable chunks
    with document and page metadata.
    """

    pdf_files = sorted(documents_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {documents_dir}"
        )

    extracted_documents = []

    for pdf_path in pdf_files:
        print(f"Reading: {pdf_path.name}")

        try:
            with pymupdf.open(pdf_path) as pdf:
                if len(pdf) == 0:
                    print(f"Skipping empty PDF: {pdf_path.name}")
                    continue

                first_page_text = pdf[0].get_text("text")
                metadata = extract_metadata(
                    pdf_path.name,
                    first_page_text
                )

                pages = []

                for page_index, page in enumerate(pdf):
                    page_text = page.get_text("text")

                    if page_text.strip():
                        pages.append({
                            "page": page_index + 1,
                            "text": page_text
                        })

                extracted_documents.append({
                    "filename": pdf_path.name,
                    "metadata": metadata,
                    "pages": pages
                })

        except Exception as error:
            print(f"Could not read {pdf_path.name}: {error}")

    if not extracted_documents:
        raise ValueError("No readable PDF documents were found.")

    # Find the highest revision available for each document.
    latest_revisions = {}

    for document in extracted_documents:
        metadata = document["metadata"]
        doc_no = metadata["doc_no"]
        revision = metadata["revision"]

        if revision is not None:
            latest_revisions[doc_no] = max(
                latest_revisions.get(doc_no, revision),
                revision
            )

    searchable_chunks = []

    for document in extracted_documents:
        metadata = document["metadata"]
        doc_no = metadata["doc_no"]
        revision = metadata["revision"]

        if revision is None:
            revision_status = "revision_not_detected"
        elif revision == latest_revisions.get(doc_no):
            revision_status = "latest_in_supplied_documents"
        else:
            revision_status = "older_revision_in_supplied_documents"

        for page_data in document["pages"]:
            page_chunks = split_into_chunks(page_data["text"])

            for index, chunk in enumerate(page_chunks):
                searchable_chunks.append({
                    "chunk_id": len(searchable_chunks),
                    "text": chunk,
                    "source": document["filename"],
                    "doc_no": doc_no,
                    "revision": revision,
                    "title": metadata["title"],
                    "page": page_data["page"],
                    "revision_status": revision_status
                })

    return searchable_chunks


if __name__ == "__main__":
    chunks = load_documents()

    print("\nPDF processing completed!")
    print(f"Total searchable chunks: {len(chunks)}")

    for item in chunks[:5]:
        print("\n------------------------------")
        print(f"Document: {item['doc_no']}")
        print(f"Revision: {item['revision']}")
        print(f"Page: {item['page']}")
        print(f"Status: {item['revision_status']}")
        print(f"Text: {item['text'][:200]}")

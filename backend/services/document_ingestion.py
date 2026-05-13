import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.models.document import DocumentChunk


SUPPORTED_DOCUMENT_TYPES = {".pdf": "pdf", ".txt": "txt"}
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 150


class UnsupportedDocumentTypeError(ValueError):
    """Raised when an uploaded file is not a supported document type."""


class DocumentIngestionService:
    def __init__(
        self,
        data_dir: str | Path | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> None:
        self.data_dir = Path(
            data_dir or os.getenv("HEALTHCARE_DOCUMENT_DATA_DIR", "data")
        )
        self.uploads_dir = self.data_dir / "uploads"
        self.processed_dir = self.data_dir / "processed"
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def process_upload(
        self, upload_file: UploadFile
    ) -> tuple[Path, Path, list[DocumentChunk], str]:
        original_filename = upload_file.filename or "uploaded_document"
        document_type = self.get_document_type(original_filename)
        upload_timestamp = datetime.now(timezone.utc).isoformat()
        uploaded_file_path = self.save_upload(upload_file, original_filename, upload_timestamp)
        text = self.extract_text(uploaded_file_path, document_type)
        chunks = self.split_text(text)
        chunk_records = self.build_chunk_records(
            chunks=chunks,
            filename=original_filename,
            upload_timestamp=upload_timestamp,
            document_type=document_type,
        )
        processed_file_path = self.save_processed_chunks(
            chunk_records=chunk_records,
            original_filename=original_filename,
            upload_timestamp=upload_timestamp,
        )
        return uploaded_file_path, processed_file_path, chunk_records, upload_timestamp

    def get_document_type(self, filename: str) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix not in SUPPORTED_DOCUMENT_TYPES:
            supported_types = ", ".join(sorted(SUPPORTED_DOCUMENT_TYPES))
            raise UnsupportedDocumentTypeError(
                "Unsupported document type "
                f"'{suffix or 'unknown'}'. Supported types: {supported_types}."
            )
        return SUPPORTED_DOCUMENT_TYPES[suffix]

    def save_upload(
        self, upload_file: UploadFile, original_filename: str, upload_timestamp: str
    ) -> Path:
        safe_name = self.safe_filename(original_filename)
        timestamp_slug = self.timestamp_slug(upload_timestamp)
        destination = self.uploads_dir / f"{timestamp_slug}_{uuid4().hex}_{safe_name}"
        with destination.open("wb") as output_file:
            shutil.copyfileobj(upload_file.file, output_file)
        upload_file.file.seek(0)
        return destination

    def extract_text(self, file_path: Path, document_type: str) -> str:
        if document_type == "pdf":
            return self.extract_pdf_text(file_path)
        if document_type == "txt":
            return self.extract_txt_text(file_path)
        raise UnsupportedDocumentTypeError(f"Unsupported document type '{document_type}'.")

    def extract_pdf_text(self, file_path: Path) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(page_text.strip() for page_text in pages if page_text.strip())

    def extract_txt_text(self, file_path: Path) -> str:
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return file_path.read_text(encoding="latin-1")

    def split_text(self, text: str) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = [chunk.strip() for chunk in splitter.split_text(text) if chunk.strip()]
        return chunks

    def build_chunk_records(
        self,
        chunks: list[str],
        filename: str,
        upload_timestamp: str,
        document_type: str,
    ) -> list[DocumentChunk]:
        return [
            DocumentChunk(
                filename=filename,
                upload_timestamp=upload_timestamp,
                chunk_index=index,
                content=chunk,
                document_type=document_type,
            )
            for index, chunk in enumerate(chunks)
        ]

    def save_processed_chunks(
        self,
        chunk_records: list[DocumentChunk],
        original_filename: str,
        upload_timestamp: str,
    ) -> Path:
        source_stem = self.safe_filename(Path(original_filename).stem)
        timestamp_slug = self.timestamp_slug(upload_timestamp)
        destination = self.processed_dir / f"{timestamp_slug}_{uuid4().hex}_{source_stem}.json"
        payload = [
            chunk.model_dump() if hasattr(chunk, "model_dump") else chunk.dict()
            for chunk in chunk_records
        ]
        destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return destination

    def safe_filename(self, filename: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", filename.strip())
        return cleaned or "document"

    def timestamp_slug(self, upload_timestamp: str) -> str:
        return upload_timestamp.replace(":", "").replace("+", "_")

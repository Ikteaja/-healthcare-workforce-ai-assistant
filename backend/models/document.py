from pydantic import BaseModel


class DocumentChunk(BaseModel):
    filename: str
    upload_timestamp: str
    chunk_index: int
    content: str
    document_type: str


class DocumentUploadResponse(BaseModel):
    filename: str
    document_type: str
    upload_timestamp: str
    uploaded_file_path: str
    processed_file_path: str
    chunk_count: int
    chunks: list[DocumentChunk]

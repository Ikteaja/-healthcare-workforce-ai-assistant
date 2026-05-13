from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from backend.models.document import DocumentUploadResponse
from backend.services.document_ingestion import (
    DocumentIngestionService,
    UnsupportedDocumentTypeError,
)

router = APIRouter(prefix="/documents", tags=["documents"])


def get_document_ingestion_service() -> DocumentIngestionService:
    return DocumentIngestionService()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    ingestion_service: DocumentIngestionService = Depends(get_document_ingestion_service),
) -> DocumentUploadResponse:
    try:
        (
            uploaded_file_path,
            processed_file_path,
            chunks,
            upload_timestamp,
        ) = ingestion_service.process_upload(file)
    except UnsupportedDocumentTypeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    filename = file.filename or "uploaded_document"
    document_type = ingestion_service.get_document_type(filename)
    return DocumentUploadResponse(
        filename=filename,
        document_type=document_type,
        upload_timestamp=upload_timestamp,
        uploaded_file_path=str(uploaded_file_path),
        processed_file_path=str(processed_file_path),
        chunk_count=len(chunks),
        chunks=chunks,
    )

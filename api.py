import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from ocr_service import OCRService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PTSD OCR Service",
    description="OCR service with Hebrew text support and FFmpeg integration",
    version="1.0.0",
)

# Initialize OCR service
ocr_service = OCRService()


# Request and Response models
class ExtractTextRequest(BaseModel):
    file_path: str


class ExtractTextResponse(BaseModel):
    text: Optional[str]
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", message="OCR service is running")


@app.post("/extract-text", response_model=ExtractTextResponse)
async def extract_text(request: ExtractTextRequest):
    """
    Extract text from an image or PDF file.

    Args:
        request: Contains the file_path of the document to process

    Returns:
        Extracted text or error message
    """
    try:
        # Validate file path
        if not request.file_path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File path is required"
            )

        # Check if file exists
        if not os.path.exists(request.file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {request.file_path}",
            )

        # Extract text using OCR service
        logger.info(f"Extracting text from: {request.file_path}")
        extracted_text = ocr_service.extract_text(request.file_path)

        if extracted_text is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to extract text from the file",
            )

        if not extracted_text.strip():
            return ExtractTextResponse(text="", message="No text found in the document")

        return ExtractTextResponse(
            text=extracted_text, message="Text extracted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error extracting text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PTSD OCR Service API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "extract_text": "/extract-text (POST)",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

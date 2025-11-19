import io
import os
import re
import subprocess
import tempfile
from typing import Optional

import fitz  # pymupdf
import magic
import pdfplumber
import pytesseract
from PIL import Image


class OCRService:
    def __init__(self):
        pass

    def detect_file_type(self, file_path: str) -> str:
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type
        except Exception as e:
            print(f"Error detecting file type: {e}")
            return ""

    def convert_image_with_ffmpeg(
        self, input_path: str, output_format: str = "png"
    ) -> Optional[str]:
        try:
            with tempfile.NamedTemporaryFile(
                suffix=f".{output_format}", delete=False
            ) as temp_file:
                output_path = temp_file.name

            cmd = ["ffmpeg", "-i", input_path, "-vf", "scale=iw:ih", "-y", output_path]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return output_path
            else:
                print(f"FFmpeg conversion failed: {result.stderr}")
                os.unlink(output_path)
                return None
        except Exception as e:
            print(f"Error converting image with ffmpeg: {e}")
            if "output_path" in locals() and os.path.exists(output_path):
                os.unlink(output_path)
            return None

    def extract_text_from_image(self, image_path: str) -> Optional[str]:
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return None

    def is_hebrew_text(self, text: str) -> bool:
        if not text or len(text.strip()) < 3:
            return False

        # Check for Hebrew Unicode characters
        hebrew_pattern = re.compile(r"[\u0590-\u05FF]")
        hebrew_chars = hebrew_pattern.findall(text)

        # Consider it Hebrew if at least 10% of characters are Hebrew
        total_chars = len(re.sub(r"\s", "", text))
        if total_chars == 0:
            return False

        hebrew_ratio = len(hebrew_chars) / total_chars
        return hebrew_ratio >= 0.1

    def extract_text_from_pdf_images(self, pdf_path: str) -> Optional[str]:
        try:
            text = ""
            doc = fitz.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc[page_num]

                # Convert page to image with 2x resolution for better OCR
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)

                # Convert to PIL Image
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))

                # Use pytesseract with Hebrew language support
                page_text = pytesseract.image_to_string(image, lang="heb")
                if page_text.strip():
                    text += page_text.strip() + "\n"

            doc.close()
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF images: {e}")
            return None

    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        try:
            # First try direct text extraction
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # Check if extracted text is valid Hebrew
            if self.is_hebrew_text(text):
                return text.strip()
            else:
                print(
                    "PDF text extraction did not yield valid Hebrew text, trying OCR..."
                )
                # Fallback to image-based OCR
                ocr_text = self.extract_text_from_pdf_images(pdf_path)
                return ocr_text

        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def extract_text(self, file_path: str) -> Optional[str]:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None

        # Use magic library to detect file type
        file_type = self.detect_file_type(file_path)

        # Handle PDF files
        if file_type == "application/pdf":
            return self.extract_text_from_pdf(file_path)

        # Handle image files
        elif file_type.startswith("image/"):
            file_extension = os.path.splitext(file_path)[1].lower()

            # Standard image formats that PIL can handle directly
            if file_extension in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]:
                return self.extract_text_from_image(file_path)

            # Non-standard image formats - convert with ffmpeg first
            else:
                print(
                    f"Converting non-standard image format ({file_type}) using ffmpeg..."
                )
                converted_path = self.convert_image_with_ffmpeg(file_path, "png")

                if converted_path:
                    try:
                        text = self.extract_text_from_image(converted_path)
                        return text
                    finally:
                        # Clean up temporary file
                        os.unlink(converted_path)
                else:
                    return None

        else:
            print(f"Unsupported file format: {file_type}")
            return None

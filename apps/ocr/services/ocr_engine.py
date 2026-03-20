"""
OCR engine wrapper around Tesseract.

Handles both image and PDF files, applying preprocessing
and postprocessing to produce clean extracted text.
"""

import logging

import pytesseract
from django.conf import settings
from PIL import Image

from .preprocessing import preprocess_image
from .postprocessing import clean_text

logger = logging.getLogger(__name__)

# Configure Tesseract binary path from Django settings
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from a single PIL Image.
    
    Applies preprocessing, runs Tesseract, and cleans the output.
    
    Args:
        image: PIL Image to process.
    
    Returns:
        Cleaned extracted text.
    """
    processed = preprocess_image(image)
    raw_text = pytesseract.image_to_string(processed)
    return clean_text(raw_text)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF by converting each page to an image.
    
    Uses pdf2image to convert pages, then runs OCR on each.
    
    Args:
        file_path: Absolute path to the PDF file.
    
    Returns:
        Combined cleaned text from all pages.
    """
    try:
        from pdf2image import convert_from_path
    except ImportError:
        logger.error("pdf2image is not installed. Cannot process PDFs.")
        raise RuntimeError("PDF processing requires the pdf2image package.")

    try:
        images = convert_from_path(file_path, dpi=300, poppler_path=settings.POPPLER_PATH)
    except Exception as e:
        logger.error(f"Failed to convert PDF to images: {e}")
        raise RuntimeError(f"Failed to convert PDF: {e}")

    page_texts = []
    for i, page_image in enumerate(images, start=1):
        logger.info(f"Processing PDF page {i}/{len(images)}")
        text = extract_text_from_image(page_image)
        if text:
            page_texts.append(f"--- Page {i} ---\n{text}")

    return '\n\n'.join(page_texts)


def process_document(document) -> str:
    """
    Process a Document model instance and extract text.
    
    Dispatches to the appropriate handler based on file type.
    Updates the document status during processing.
    
    Args:
        document: Document model instance.
    
    Returns:
        Extracted text string.
    
    Raises:
        RuntimeError: If processing fails.
    """
    file_path = document.file.path

    try:
        document.status = 'processing'
        document.save(update_fields=['status'])

        if document.is_pdf:
            text = extract_text_from_pdf(file_path)
        elif document.is_image:
            image = Image.open(file_path)
            text = extract_text_from_image(image)
        else:
            raise ValueError(
                f"Unsupported file type: {document.file_extension}"
            )

        document.status = 'done'
        document.save(update_fields=['status'])
        return text

    except Exception as e:
        document.status = 'failed'
        document.save(update_fields=['status'])
        logger.error(f"OCR failed for {document.original_filename}: {e}")
        raise

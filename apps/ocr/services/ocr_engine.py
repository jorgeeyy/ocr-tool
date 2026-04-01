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
    Extract text from a single PIL Image with basic formatting preservation.
    
    Using Tesseract's HOCR (HTML-based OCR) to preserve relative positions 
    and potentially some font weight information.
    
    Args:
        image: PIL Image to process.
    
    Returns:
        HOCR (HTML) extracted text.
    """
    processed = preprocess_image(image)
    # Get HOCR output for basic layout preservation
    hocr = pytesseract.image_to_pdf_or_hocr(processed, extension='hocr').decode('utf-8')
    # Clean it up to keep it readable
    return clean_text(hocr)


def extract_high_fidelity_pdf(file_path: str) -> str:
    """
    Extract high-fidelity HTML from a PDF using PyMuPDF (fitz).
    
    This preserves fonts, colors, and absolute positioning of text.
    
    Args:
        file_path: Absolute path to the PDF.
    
    Returns:
        HTML content of the PDF.
    """
    try:
        import fitz
        doc = fitz.open(file_path)
        html_out = []
        for page in doc:
            html_out.append(page.get_text("html"))
        doc.close()
        return clean_text("\n".join(html_out))
    except Exception as e:
        logger.error(f"High-fidelity PDF extraction failed: {e}")
        return ""


def extract_scanned_pdf(file_path: str) -> str:
    """
    Legacy fallback: Extract text from a scanned PDF via images and OCR.
    """
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(file_path, dpi=300, poppler_path=settings.POPPLER_PATH)
        page_texts = []
        for i, page_image in enumerate(images, start=1):
            text = extract_text_from_image(page_image)
            if text:
                page_texts.append(text)
        return "\n\n".join(page_texts)
    except Exception as e:
        logger.error(f"Scanned PDF extraction failed: {e}")
        raise RuntimeError(f"Failed to convert PDF: {e}")


def process_document(document) -> str:
    """
    Process a Document model instance and extract text with high fidelity.
    
    Tries digital extraction first for PDFs, falling back to OCR if needed.
    For images, uses HOCR for better layout preservation.
    
    Args:
        document: Document model instance.
    
    Returns:
        High-fidelity HTML/Text string.
    """
    file_path = document.file.path

    try:
        document.status = 'processing'
        document.save(update_fields=['status'])

        if document.is_pdf:
            # 1. Try digital extraction first (fast and high fidelity)
            text = extract_high_fidelity_pdf(file_path)
            
            # 2. If it's a scanned PDF (very small result), fallback to OCR
            if len(text.strip()) < 100:
                logger.info(f"PDF seems scanned, switching to OCR for {document.original_filename}")
                text = extract_scanned_pdf(file_path)
        
        elif document.is_image:
            image = Image.open(file_path)
            text = extract_text_from_image(image)
        
        else:
            raise ValueError(f"Unsupported file type: {document.file_extension}")

        document.status = 'done'
        document.save(update_fields=['status'])
        return text

    except Exception as e:
        document.status = 'failed'
        document.save(update_fields=['status'])
        logger.error(f"OCR failed for {document.original_filename}: {e}")
        raise

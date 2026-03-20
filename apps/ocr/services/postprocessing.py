"""
Text post-processing for OCR output cleanup.

Removes noise characters, normalizes whitespace,
and applies basic formatting fixes.
"""

import re


def clean_text(raw_text: str) -> str:
    """
    Clean and normalize raw OCR output text.
    
    Steps:
        1. Remove non-printable / noise characters
        2. Normalize whitespace
        3. Remove excessive blank lines
        4. Strip leading/trailing whitespace
    
    Args:
        raw_text: Raw text string from OCR engine.
    
    Returns:
        Cleaned text string.
    """
    if not raw_text:
        return ""

    # Remove non-printable characters (keep newlines, tabs, and standard chars)
    text = re.sub(r'[^\x20-\x7E\n\t\r]', '', raw_text)

    # Normalize multiple spaces to single space (preserve newlines)
    text = re.sub(r'[^\S\n]+', ' ', text)

    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip whitespace from each line
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(lines)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text

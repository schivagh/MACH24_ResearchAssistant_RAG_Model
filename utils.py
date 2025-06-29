import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import tempfile

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    if len(text.strip()) < 100:  # Likely a scanned PDF
        text = ocr_pdf(pdf_path)
    return text

def ocr_pdf(pdf_path):
    text = ""
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_path, output_folder=path)
        for img in images:
            text += pytesseract.image_to_string(img)
    return text

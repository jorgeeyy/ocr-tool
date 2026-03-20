# Django OCR Tool – Coding Agent Specification

## 1. Project Overview

A personal OCR (Optical Character Recognition) web application built with Django. The system allows users to upload images or PDFs and extract text using an OCR engine.

---

## 2. High-Level Architecture

### Components

- **Frontend (****Django Templates / Optional**** SPA)**
- **Django Backend (API + Views)**
- **OCR Processing Layer**
- **File Storage (Local / Cloud optional)**
- **Database (PostgreSQL / SQLite for dev)**

### Flow

1. User uploads image/PDF
2. File is stored
3. Preprocessing is applied
4. OCR engine extracts text
5. Text is cleaned (post-processing)
6. Result is saved and returned to user

---

## 3. Tech Stack

- Backend: Django, Django REST Framework (optional)
- OCR Engine: Tesseract OCR
- Image Processing: OpenCV / Pillow
- Queue (optional): Celery + Redis
- Database: PostgreSQL (production), SQLite (dev)

---

## 4. Core Features

### 4.1 File Upload

- Upload image (JPG, PNG)
- Upload PDF
- Validate file type and size

### 4.2 OCR Processing

- Convert PDF to images (if needed)
- Apply preprocessing:
  - Grayscale
  - Thresholding
  - Noise removal
- Run OCR engine

### 4.3 Text Post-Processing

- Remove noise characters
- Normalize spacing
- Basic formatting

### 4.4 Result Management

- Store extracted text
- Link result to uploaded file
- Allow user to view/download text

---

## 5. Suggested Django App Structure

```
ocr_project/
│── ocr_project/
│   ├── settings.py
│   ├── urls.py
│
│── apps/
│   ├── core/              # base configs
│   ├── ocr/               # main OCR logic
│   ├── users/             # optional auth
│
│── media/                 # uploaded files
│── static/
```

### OCR App Structure

```
ocr/
│── models.py
│── views.py
│── services/
│   ├── ocr_engine.py
│   ├── preprocessing.py
│   ├── postprocessing.py
│── utils/
│── serializers.py (if DRF)
│── tasks.py (if Celery)
```

---

## 6. Database Models

### Document

- id
- file (FileField)
- uploaded\_at
- status (pending, processing, done, failed)

### OCRResult

- id
- document (FK)
- extracted\_text (TextField)
- processed\_at

---

## 7. OCR Service Layer

### preprocessing.py

- Load image
- Convert to grayscale
- Apply thresholding
- Remove noise

### ocr\_engine.py

- Call Tesseract
- Handle multiple languages (optional)

### postprocessing.py

- Clean extracted text
- Normalize formatting

---

## 8. API / Views

### Endpoints

- POST /upload/ → upload file
- GET /documents/ → list uploads
- GET /documents/{id}/ → view result

---

## 9. Background Processing (Optional but Recommended)

- Use Celery for async OCR processing
- Redis as message broker
- Avoid blocking request/response cycle

---

## 10. Error Handling

- Invalid file type
- OCR failure
- Corrupted files

---

## 11. Future Enhancements

- Multi-language OCR
- Batch processing
- Export to PDF/DOCX
- Add LLM for text understanding
- Table/form detection

---

## 12. Non-Functional Requirements

- Fast processing for small files
- Scalable architecture
- Clean modular code
- Easy to extend

---

## 13. Development Steps

1. Setup Django project
2. Create OCR app
3. Implement file upload
4. Integrate OCR engine
5. Add preprocessing
6. Save and display results
7. Add background tasks (optional)
8. Improve UI

---

## 14. Deliverables

- Working Django project
- OCR processing pipeline
- API or UI for interaction
- Documentation

---

## 15. Notes for Coding Agent

- Keep logic modular (services layer)
- Avoid putting OCR logic in views
- Ensure error handling at every stage
- Make OCR pipeline reusable
- Write clean, readable, maintainable code


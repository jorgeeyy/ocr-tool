# NexusOCR

NexusOCR is a fast, clean, and locally-hosted Document Parsing and Optical Character Recognition (OCR) web application built beautifully with Django and Tailwind CSS. It empowers users to extract raw text from dense images and converts complex PDF documents into perfectly editable Word files with zero layout loss.

## 🌟 Key Features

- **Dual-Theme Modern UI:** A highly polished Vercel/Stripe-inspired interface featuring seamless Light and **Premium Dark Mode** toggling.
- **Image Text Extraction (OCR):** Upload JPEGs or PNGs and perfectly extract embedded text using the renowned Tesseract OCR engine, pre-processed by OpenCV for maximum accuracy.
- **True PDF-to-Word Conversion:** Bypass destructive OCR and seamlessly convert multi-page PDFs directly into editable Microsoft Word (`.docx`) files while preserving the exact layout, tables, fonts, and graphics securely.
- **Multi-Format Exporting:** Download your extractions as Plain Text (`.txt`), Word Documents (`.docx`), or Data Spreadsheets (`.xlsx`).
- **Secure File Lifecycle Management:** Beautifully integrated Javascript modals to cleanly delete documents and their system traces right from your dashboard.

---

## 🚀 Local Development Setup

Because NexusOCR does heavily lifting with imaging and binaries, you must install a few system dependencies before the Python environment will work.

### 1. Prerequisites (Windows)

Ensure you have the following installed on your system:

- **Python 3.10+**
- **Tesseract-OCR:**
  Download the Windows installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
  _Note: Installed default path is expected to be `C:\Program Files\Tesseract-OCR\tesseract.exe`._
- **Poppler:** (For PDF rendering)
  Download the latest Poppler binary and place it in your project root or add it to your System PATH environment variables or you can use the one provided in the project root.

### 2. Environment Setup

Clone this repository and open your terminal to the root folder:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install the required Python packages
pip install -r requirements.txt
```

### 3. Database & Server

Initialize the local SQLite database and spin up the environment:

```bash
# 1. Run migrations
python manage.py migrate

# 2. Start the Django Development Server
python manage.py runserver
```

Navigate to `http://localhost:8000` in your browser.

---

## 🤝 How to Contribute

We welcome contributions to make NexusOCR even better!

### Contribution Workflow:

1. **Fork the Repository:** Create your own fork and clone it to your local machine.
2. **Create a Branch:** Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit your Changes:** Commit with clear, descriptive messages (`git commit -m 'Add some AmazingFeature'`).
4. **Push to the Branch:** Push your changes up to your fork (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request:** Submit a Pull Request targeting the `main` branch.

### Areas for Future Improvement:

- Moving the synchronous Document Upload parsing into a **Celery Worker Queue** (with Redis) for asynchronous heavy lifting on massive PDFs.
- Adding PostgreSQL support for production environments.
- Enhancing the text cleanup post-processing algorithms.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

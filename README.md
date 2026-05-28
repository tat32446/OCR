Parallel Case File OCR Processor
An advanced, multi-core Python utility designed to batch-process scanned, image-only PDFs across nested directories. It dynamically reads documents from case-specific input folders, applies an invisible searchable text layer using Tesseract OCR, and automatically mirrors the exact directory structure into an output destination.

🏗️ Folder Architecture
The script automatically detects and replicates your multi-level file structures. You only need to supply the inputs; the outputs are generated dynamically on demand.

Plaintext
OCR/
├── run_ocr.py               # The main Python script
├── requirements.txt         # Python dependencies
└── scanned_inputs/          # Put your raw scanned files here
    ├── Case_001/
    │   ├── scan1.pdf
    │   └── scan2.pdf
    └── Case_002/
        └── record.pdf

=========== AUTOMATICALLY GENERATED ON RUN ===========
└── ocr_outputs/             # Mirrored fully searchable results
    ├── Case_001/
    │   ├── scan1.pdf        <-- Searchable / Selectable text
    │   └── scan2.pdf
    └── Case_002/
        └── record.pdf
🚀 Step-by-Step Setup & Execution
1. Install System Dependencies
The Python libraries require the core binary OCR engine to be present on your Linux operating system. Install them via apt:

Bash
sudo apt update
sudo apt install ocrmypdf tesseract-ocr -y
2. Activate Virtual Environment & Install Requirements
Navigate to your project directory, turn on your isolated virtual environment, and install your requirements.txt configurations:

Bash
# Navigate to project root
cd ~/OCR

# Activate environment
source env/bin/activate

# Install/upgrade python libraries
pip install -r requirements.txt --upgrade
3. Run the OCR Pipeline
Place your target case folders containing unsearchable PDFs into scanned_inputs/ and fire up the engine:

Bash
python run_ocr.py
🛠️ Script Processing Pipeline
When you run the script, it executes through three distinct mechanical phases:

[ Phase 1: Directory Discovery ] 
       Uses os.walk to catalog PDFs inside "scanned_inputs/Case_*".
       Checks "ocr_outputs/" to skip files that were completed in past runs.
                      │
                      ▼
[ Phase 2: Concurrent Core Allocation ]
       Distributes files across all available CPU cores via ProcessPoolExecutor.
       Processes up to 4-8 files simultaneously (depending on your machine hardware).
                      │
                      ▼
[ Phase 3: OCR Engine & Write ]
       Extracts raster graphics -> Generates hOCR fonts layer -> 
       Optimizes final file weights -> Writes cleanly into matching output paths.
🔍 Troubleshooting & System Fixes
⚠️ Issue: unrecognized arguments: --fast-logs
Cause: This parameter belongs to modern versions of ocrmypdf and is completely unsupported on older releases compiled for Python 3.8.

Fix: Ensure fast_logs=True has been deleted from your ocrmypdf.ocr() argument dictionary inside run_ocr.py.

⚠️ Issue: ImportError: cannot import name 'PdfMatrix' from 'pikepdf'
Cause: Version mismatch within your environment dependencies (pikepdf updated past the threshold your version of ocrmypdf can read).

Fix: Re-align your environment packages using explicit limits:

Bash
pip install "pikepdf>=6.0.0,<7.0.0" "ocrmypdf==14.4.0" --force-reinstall

### ⚠️ Issue: `CryptographyDeprecationWarning`
* **Warning Context:** `Python 3.8 is no longer supported by the Python core team...`
* **Fix:** This is a non-breaking deprecation logger message from Python's core security

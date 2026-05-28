Parallel Case File OCR Processor
An advanced, multi-core Python utility designed to batch-process scanned, image-only PDFs across nested directories. It dynamically reads documents from case-specific input folders, applies an invisible searchable text layer using Tesseract OCR, and automatically mirrors the exact directory structure into an output destination.


sudo apt update
sudo apt install ocrmypdf tesseract-ocr -y


# Navigate to project root
cd ~/OCR

# Activate environment
source env/bin/activate

# Install/upgrade python libraries
pip install -r requirements.txt --upgrade



python run_ocr.py




🛠️ Script Processing Pipeline
When you run the script, it executes through three distinct phases:

Phase 1: Directory Discovery

Uses os.walk to catalog PDFs inside scanned_inputs/Case_*.

Checks ocr_outputs/ to automatically skip files that were completed in past runs so you don't waste time reprocessing them.

Phase 2: Concurrent Core Allocation

Distributes files across all available CPU cores via ProcessPoolExecutor.

Processes up to 4-8 files simultaneously (depending on your machine hardware instead of one-by-one).

Phase 3: OCR Engine & Write

Extracts raster graphics from the PDF -> Generates an invisible hOCR text fonts layer -> Optimizes final file weights -> Writes cleanly into matching output paths.



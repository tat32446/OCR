Phase 1: Folder Mapping and Scanning (os.walk)
Instead of just looking at one flat folder, the script uses a depth-first search to map your entire directory tree.

Directory Discovery: The script targets ./scanned_inputs. Using os.walk, it dives into every subfolder it finds (e.g., Case_001, Case_999).

Path Calculation: For every PDF it discovers, it calculates its relative path (e.g., Case_001/document.pdf). It uses this relative path to map exactly where the output should go (./ocr_outputs/Case_001/document.pdf).

Auto-Folder Creation: It checks if the destination folder exists inside ocr_outputs. If it doesn't, Python automatically generates it on the fly (os.makedirs).

Deduplication Check: Before doing any heavy lifting, it looks inside the output folder. If ocr_outputs/Case_001/document.pdf already exists, it prints a message skipping it. This saves you massive amounts of time on subsequent runs. If it's missing, it adds the file to a processing master list (the queue).

Phase 2: High-Speed Multi-Core Queueing (ProcessPoolExecutor)
Standard Python scripts process files one by one. If you have 6 files and each takes 20 seconds, you wait 2 minutes. This script bypasses that bottleneck using parallel processing.

                  [ Master Queue: 6 PDF Tasks ]
                                |
         +----------------------+----------------------+
         |                      |                      |
  [ Core 1 Active ]      [ Core 2 Active ]      [ Core 3 Active ]
     Processes:             Processes:             Processes:
     Case_001/doc1.pdf      Case_001/doc2.pdf      Case_002/doc1.pdf
Hardware Detection: The script checks how many CPU cores your machine has.

Task Distribution: It spins up a pool of background processes (ProcessPoolExecutor). If you have a 6-core processor, it handles up to 6 PDFs simultaneously.

Asynchronous Monitoring: As individual CPU cores finish a file, they hand back a "Success" or "Failed" signal and immediately pull the next available PDF from the master queue.

Phase 3: The OCR Engine Pipeline (ocrmypdf)
When a file enters an active CPU core, the ocrmypdf library handles the actual heavy-duty document transformation:

Image Extraction: The script opens the input PDF and extracts the raw scanned images from the pages.

Tesseract Text Layer Generation: It passes those images to the Tesseract OCR engine. Tesseract analyzes the pixels, identifies text characters, maps their precise coordinates, and creates an invisible layer of digital, selectable text.

Layer Integration & Optimization: The script pieces the original scanned image and the new invisible text layer back together. It applies optimization parameters (optimize=1) to compress the image data so your output files don't balloon in size.

Safe Write: The finalized, fully searchable PDF is written safely into its designated ocr_outputs/Case_Number/ destination folder.

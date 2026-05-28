import os
import sys
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import ocrmypdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def ocr_single_pdf(input_path, output_path):
    """
    Worker function to process a single PDF file using ocrmypdf.
    """
    filename = os.path.basename(input_path)
    # Extract the 'Case_Number Folder' name for clearer logging
    case_folder = os.path.basename(os.path.dirname(input_path))
    
    try:
        logging.info(f"[{case_folder}] Starting OCR for: {filename}")
        
        ocrmypdf.ocr(
            input_file=input_path,
            output_file=output_path,
            redo_ocr=True,       # Force OCR over existing layers
            optimize=1           # Optimize file size
        )
        logging.info(f"[{case_folder}] Successfully saved: {os.path.basename(output_path)}")
        return True
    except Exception as e:
        logging.error(f"[{case_folder}] Failed to process {filename}. Error: {str(e)}")
        return False

def batch_process_nested_pdfs(base_input_dir, base_output_dir, max_workers=None):
    """
    Walks through nested directories (Case Folders) and processes PDFs while preserving layout.
    """
    pdf_tasks = []

    # Check if base input directory exists
    if not os.path.exists(base_input_dir):
        logging.error(f"Base input directory '{base_input_dir}' does not exist!")
        return

    # os.walk travels down into all subdirectories (Case_number folders)
    for root, dirs, files in os.walk(base_input_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                # Full path to the input PDF
                in_file_path = os.path.join(root, file)
                
                # Determine the relative path from the base input folder 
                # (e.g., 'Case_12345/document.pdf')
                rel_path = os.path.relpath(in_file_path, base_input_dir)
                
                # Construct the matching output path
                out_file_path = os.path.join(base_output_dir, rel_path)
                
                # Ensure the specific Case output subfolder exists before processing
                os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
                
                # Check if already processed to avoid duplicating work
                if os.path.exists(out_file_path):
                    logging.info(f"Skipping '{rel_path}' — output already exists.")
                    continue
                    
                pdf_tasks.append((in_file_path, out_file_path))
            
    if not pdf_tasks:
        logging.info("No new PDF files found in any Case folders to process.")
        return

    logging.info(f"Found {len(pdf_tasks)} files across Case folders. Starting parallel execution...")

    # Execute tasks across multiple CPU cores
    success_count = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(ocr_single_pdf, inp, outp): os.path.basename(inp) 
            for inp, outp in pdf_tasks
        }
        
        for future in as_completed(futures):
            if future.result():
                success_count += 1
                
    logging.info(f"Batch processing completed. Successfully processed {success_count}/{len(pdf_tasks)} files.")

if __name__ == "__main__":
    # Define your top-level directories
    INPUT_FOLDER = "./scanned_inputs"
    OUTPUT_FOLDER = "./ocr_outputs"
    
    batch_process_nested_pdfs(INPUT_FOLDER, OUTPUT_FOLDER, max_workers=None)
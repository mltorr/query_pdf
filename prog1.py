import os
import fitz
import pytesseract
from PIL import Image
import tempfile
import csv
import streamlit as st

# Function to read and extract text from the PDF
def read_pdf(pdf_path):
    text = ""
    
    with tempfile.NamedTemporaryFile(suffix='.png') as img_temp:
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=170)
            pix.save(img_temp.name, jpg_quality=98)

            img1 = Image.open(img_temp.name)
            page_text = pytesseract.image_to_string(img1, config='--psm 6')

            text += page_text  # Append page text to the overall text

    return text

def main():
    base_dir = r'C:\Users\Advali\Desktop\2020'
    output_file = 'extracted_texts.tsv'

    st.title("PDF Data Extraction")
    
    # Display file uploader
    st.write("Scanning PDF files in subdirectories under:")
    st.text(base_dir)

    # Create and open the output file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Subdirectory', 'Filename', 'Scanned_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()

        # Walk through the base directory
        for root, dirs, files in os.walk(base_dir):
            pdf_files = [file for file in files if file.lower().endswith('.pdf')]

            if pdf_files:
                subdirectory = os.path.relpath(root, base_dir)
                st.write(f"Processing directory: {subdirectory}")

                # Initialize progress bar for the current subdirectory
                progress_bar = st.progress(0)
                total_files = len(pdf_files)

                for idx, file in enumerate(pdf_files):
                    pdf_path = os.path.join(root, file)
                    scanned_text = read_pdf(pdf_path)

                    # Write the extracted text to the output file
                    writer.writerow({
                        'Subdirectory': subdirectory,
                        'Filename': file,
                        'Scanned_text': scanned_text
                    })

                    # Update the progress bar
                    progress_bar.progress((idx + 1) / total_files)

                st.write(f"Finished processing directory: {subdirectory}")

if __name__ == "__main__":
    main()

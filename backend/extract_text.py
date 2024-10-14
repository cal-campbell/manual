# backend/extract_text.py extract text from PDF

import PyPDF2

def extract_text_from_pdf(pdf_path):
    # Open the PDF file at the given path in 'rb' mode (read binary mode).
    with open(pdf_path, 'rb') as file:
        
        # Create a PDF reader object to process the opened PDF file.
        reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string where the extracted text will be stored.
        text = ""
        
        # Loop over each page in the PDF (from page 0 to the last page).
        for page_num in range(len(reader.pages)):
            
            # Extract the text from the current page and append it to the 'text' variable.
            text += reader.pages[page_num].extract_text()

    
    # Return the extracted text once all pages have been processed.
    return text


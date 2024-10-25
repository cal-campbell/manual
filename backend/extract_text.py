import PyPDF2
import requests
from io import BytesIO

def extract_text_from_pdf(pdf_source):
    # Check if the source is a URL (starts with 'http' or 'https')
    if pdf_source.startswith("http://") or pdf_source.startswith("https://"):
        # Download the PDF content from the URL
        response = requests.get(pdf_source)
        response.raise_for_status()  # Ensure we got a valid response
        pdf_content = BytesIO(response.content)  # Create a file-like object from the downloaded content
    else:
        # If it's a local path, open it as a file
        pdf_content = open(pdf_source, 'rb')

    try:
        # Create a PDF reader object to process the opened PDF content
        reader = PyPDF2.PdfReader(pdf_content)
        
        # Initialize an empty string where the extracted text will be stored
        text = ""
        
        # Loop over each page in the PDF and extract the text
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    
    finally:
        # Close the file if it's a local file path
        if not isinstance(pdf_content, BytesIO):
            pdf_content.close()
    
    # Return the extracted text once all pages have been processed
    return text


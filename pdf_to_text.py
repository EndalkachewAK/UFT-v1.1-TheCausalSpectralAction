import PyPDF2
import os

def convert_pdf_to_text(pdf_path):
    """Converts a PDF file to a text file."""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            text_path = os.path.splitext(pdf_path)[0] + ".txt"
            with open(text_path, 'w') as text_file:
                text_file.write(text)
            return f"Successfully converted {pdf_path} to {text_path}"
    except Exception as e:
        return f"Error converting {pdf_path}: {e}"

if __name__ == "__main__":
    for filename in os.listdir('.'):
        if filename.endswith('.pdf'):
            print(convert_pdf_to_text(filename))

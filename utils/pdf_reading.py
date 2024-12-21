import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,
                                            length_function=len, is_separator_regex=False)

def read_pdf(pdf_path: str, start_page: int = 0, final_page: int = None):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        text = ''
        for page in pdf_reader.pages[start_page: final_page]:
            text += page.extract_text()
        chunks = text_splitter.split_text(text)

    return chunks

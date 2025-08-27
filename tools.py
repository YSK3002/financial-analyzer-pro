import os
from dotenv import load_dotenv
from crewai_tools import tool
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

@tool("Financial Document Reader Tool")
def read_data_tool(path: str) -> str:
    """
    Tool to read and extract text from a PDF file from a given path.

    Args:
        path (str): The file path to the PDF document.

    Returns:
        str: The full text content of the financial document.
    """
    loader = PyPDFLoader(file_path=path)
    docs = loader.load()

    full_report = ""
    for page in docs:
        content = page.page_content
        content = ' '.join(content.split())
        full_report += content + "\n"
        
    return full_report
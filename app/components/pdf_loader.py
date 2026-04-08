from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from app.common.logger import logger
from app.common.custom_exception import CustomException
import sys


def load_pdf_files(data_path: str = DATA_PATH):
    try:
        logger.info(f"Loading PDF files from: {data_path}")
        loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages from PDF files")
        return documents
    except Exception as e:
        raise CustomException(e, sys)


def split_documents(documents):
    try:
        logger.info(f"Splitting documents (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        chunks = splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        return chunks
    except Exception as e:
        raise CustomException(e, sys)

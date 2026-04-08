import os
import sys
from app.components.pdf_loader import load_pdf_files, split_documents
from app.components.vector_store import save_vector_store, load_vector_store
from app.config.config import DB_FAISS_PATH

from app.common.logger import logger
from app.common.custom_exception import CustomException

def process_and_store_pdfs():
    try:
        logger.info("Making the vectorstore....")
   
        documents = load_pdf_files()

        text_chunks = split_documents(documents)

        save_vector_store(text_chunks)

        logger.info("Vectorstore created succesfully....")

    except Exception as e:
        raise CustomException(e, sys)


if __name__=="__main__":
    process_and_store_pdfs()

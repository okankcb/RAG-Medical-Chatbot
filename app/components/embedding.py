from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.config.config import DB_FAISS_PATH
from app.common.logger import logger
from app.common.custom_exception import CustomException
import sys


def get_embedding_model():
    try:
        logger.info("Loading HuggingFace embedding model")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        return embeddings
    except Exception as e:
        raise CustomException(e, sys)


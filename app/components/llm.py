import sys
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from app.config.config import HF_TOKEN, HUGGING_REPO_ID
from app.common.logger import logger
from app.common.custom_exception import CustomException


def load_llm(huggingface_repo_id: str = HUGGING_REPO_ID, hf_token: str = HF_TOKEN):
    try:
        logger.info("Loading LLM from HuggingFace")

        endpoint = HuggingFaceEndpoint(
            repo_id=huggingface_repo_id,
            temperature=0.3,
            max_new_tokens=256,
            huggingfacehub_api_token=hf_token,
        )
        llm = ChatHuggingFace(llm=endpoint)

        logger.info("LLM loaded successfully...")
        return llm

    except Exception as e:
        raise CustomException(e, sys)

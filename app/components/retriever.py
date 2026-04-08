from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.config.config import HUGGING_REPO_ID, HF_TOKEN
from app.common.logger import logger
from app.common.custom_exception import CustomException
import sys

CUSTOM_PROMPT_TEMPLATE = """Answer the following medical question in 2-3 lines maximum using only the information provided in the context.

Context:
{context}

Question:
{question}

Answer:"""


def set_custom_prompt():
    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )


def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()

        if db is None:
            raise ValueError("Vector store not present or empty")

        llm = load_llm(huggingface_repo_id=HUGGING_REPO_ID, hf_token=HF_TOKEN)

        if llm is None:
            raise ValueError("LLM not loaded")

        retriever = db.as_retriever(search_kwargs={"k": 3})
        prompt = set_custom_prompt()

        qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        logger.info("Successfully created the QA chain")
        return qa_chain

    except Exception as e:
        raise CustomException(e, sys)
        
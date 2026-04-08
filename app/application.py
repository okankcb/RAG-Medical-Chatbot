from flask import Flask, render_template, request, jsonify
from markupsafe import Markup
from dotenv import load_dotenv
from app.components.retriever import create_qa_chain
from app.common.logger import logger
from app.common.custom_exception import CustomException
import os
import sys

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)


def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

app.jinja_env.filters["nl2br"] = nl2br

qa_chain = None


def get_qa_chain():
    global qa_chain
    if qa_chain is None:
        logger.info("Initializing QA chain...")
        qa_chain = create_qa_chain()
    return qa_chain


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/clear", methods=["POST"])
def clear():
    return jsonify({"status": "cleared"})


@app.route("/get", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a question."}), 400

        logger.info(f"User question: {user_message}")
        chain = get_qa_chain()
        response = chain.invoke(user_message)
        logger.info(f"Bot response: {response}")

        return jsonify({"response": response})

    except Exception as e:
        error = CustomException(e, sys)
        logger.error(str(error))
        return jsonify({"response": "An error occurred. Please try again."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader = False )

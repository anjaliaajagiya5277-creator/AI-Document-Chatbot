import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    jsonify,
    session
)


import traceback

from chatbot import DocumentChatbot
from werkzeug.utils import secure_filename

from config import Config
from document_loader import DocumentLoader
from text_chunker import TextChunker
from vector_store import VectorStore


app = Flask(__name__)
# --------------------------------------
# AI Chatbot
# --------------------------------------

chatbot = DocumentChatbot()

app.config.from_object(Config)

app.secret_key = app.config["SECRET_KEY"]

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# -------------------------------------------------
# Allowed Extensions
# -------------------------------------------------

def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in app.config["ALLOWED_EXTENSIONS"]


# -------------------------------------------------
# Home
# -------------------------------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    uploaded_file = None

    extracted_data = []

    documents = []

    chunk_stats = {}

    total_pages = 0

    total_slides = 0

    vector_created = False
        # --------------------------------------
    # Clear previous uploaded document
    # when opening home page
    # --------------------------------------


        
    if request.method == "POST":

        if "document" not in request.files:

            flash(
                "Please choose a document.",
                "danger"
            )

            return redirect(url_for("home"))

        file = request.files["document"]

        if file.filename == "":

            flash(
                "Please select a file.",
                "warning"
            )

            return redirect(url_for("home"))

        if not allowed_file(file.filename):

            flash(
                "Only PDF, PPT and PPTX are supported.",
                "danger"
            )

            return redirect(url_for("home"))

        try:

            filename = secure_filename(file.filename)

            filepath = os.path.join(

                app.config["UPLOAD_FOLDER"],

                filename

            )

            file.save(filepath)
            session.clear()

            session.modified = True

            uploaded_file = filename

            session["uploaded_file"] = filename

            # --------------------------------------
            # Clear previous conversation
            # --------------------------------------

            chatbot.clear_history()

            # --------------------------------------
            # Extract Document
            # --------------------------------------

            loader = DocumentLoader(filepath)

            extracted_data = loader.load_document()

            # --------------------------------------
            # Chunk Document
            # --------------------------------------

            chunker = TextChunker()

            documents = chunker.create_documents(

                extracted_data,

                filename

            )
            print("\n====================")
            print("TOTAL CHUNKS:", len(documents))
            print("====================")

            for doc in documents[:3]:
                print(doc.metadata)
                print(doc.page_content[:300])
                print("----------------")

            chunk_stats = chunker.statistics(

                documents

            )

            # --------------------------------------
            # Create Vector Store
            # --------------------------------------

            document_name = os.path.splitext(filename)[0]

            vector_db_path = os.path.join(

                "vector_db",

                document_name

            )

            vector_store = VectorStore(

                db_path=vector_db_path

            )

            # Create FAISS vector database

            vector_store.create_vector_store(

                documents

            )

            vector_store.save_vector_store()

            # Save paths in session

            session["uploaded_file"] = filename

            session["vector_db_path"] = vector_db_path

            session["chat_count"] = 0

            vector_created = True
            # --------------------------------------

            extension = filename.rsplit(".",1)[1].lower()

            if extension == "pdf":

                total_pages = len(extracted_data)

            else:

                total_slides = len(extracted_data)

            flash(

                f"{filename} uploaded and processed successfully.",

                "success"

            )
        except Exception as e:

            traceback.print_exc()

            flash(

                f"Processing failed: {str(e)}",

                "danger"

            )

    return render_template(

        "index.html",

        uploaded_file=uploaded_file,

        extracted_data=extracted_data,

        documents=documents,

        chunk_stats=chunk_stats,

        total_pages=total_pages,

        total_slides=total_slides,

        vector_created=vector_created,


    )

# ---------------------------------------------------
# AI Chat Endpoint
# ---------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    try:
        # -----------------------------
        # Read request
        # -----------------------------

        data = request.get_json()

        question = data.get("question", "").strip().lower()


        # -----------------------------
        # Smart Conversation
        # -----------------------------

        greetings = {
            "hi",
            "hello",
            "hey",
            "hii",
            "helo",
            "hello!",
            "good morning",
            "good afternoon",
            "good evening"
        }

        thanks = {
            "thanks",
            "thank you",
            "thankyou"
        }

        bye = {
            "bye",
            "goodbye",
            "see you"
        }

        help_words = {
            "help",
            "what can you do"
        }

        about = {
            "who are you",
            "what are you"
        }


        if question in greetings:

            return jsonify({

                "success": True,

                "answer":
                """
        👋 Hello!

        I'm your AI Document Assistant.

        📄 Upload a PDF or PowerPoint presentation and I'll help you:

        • Summarize documents
        • Answer questions
        • Explain topics
        • Find important points

        How can I help you today?
        """,

                "sources":[]
            })


        if question in thanks:

            return jsonify({

                "success":True,

                "answer":"😊 You're welcome!",

                "sources":[]
            })


        if question in bye:

            return jsonify({

                "success":True,

                "answer":"👋 Goodbye! Have a great day.",

                "sources":[]
            })


        if question in help_words:

            return jsonify({

                "success":True,

                "answer":
                """
        I can help you with:

        • Document Summaries

        • Question Answering

        • Topic Explanation

        • Important Points Extraction

        Simply upload a PDF or PowerPoint presentation to get started.
        """,

                "sources":[]
            })


        if question in about:

            return jsonify({

                "success":True,

                "answer":
                """
        🤖 I'm an AI Document Assistant powered by Gemini AI and Retrieval-Augmented Generation (RAG).

        Upload a PDF or PPT and I'll answer questions based only on your document.
        """,

                "sources":[]
            })


        # -----------------------------
        # Require document for all other questions
        # -----------------------------

        if "uploaded_file" not in session:

            return jsonify({

                "success":False,

                "message":"Please upload a document first."

            }),400
        # -----------------------------
        # Read request
        # -----------------------------

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "Invalid request."

            }), 400

        question = data.get(

            "question",

            ""

        ).strip()

        # -----------------------------
        # Validate question
        # -----------------------------

        if len(question) == 0:

            return jsonify({

                "success": False,

                "message": "Please enter a question."

            }), 400

        if len(question) > 1000:

            return jsonify({

                "success": False,

                "message": "Question is too long."

            }), 400

        # -----------------------------
        # Ask Gemini
        # -----------------------------

        db_path = session.get(

            "vector_db_path",

            "vector_db"

        )

        response = chatbot.ask(

            question,

            db_path=db_path

        )
        # --------------------------------------
        # Update chat count
        # --------------------------------------

        session["chat_count"] = session.get(

            "chat_count",

            0

        ) + 1
        return jsonify({

            "success": True,

            "answer": response["answer"],

            "sources": response["sources"],

            "chat_count": session.get(

                "chat_count",

                0

            ),
            "conversation": chatbot.get_history_stats()

        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500
# ---------------------------------------------------
# Clear Conversation
# ---------------------------------------------------

@app.route("/clear_chat", methods=["POST"])
def clear_chat():

    chatbot.clear_history()

    session["chat_count"] = 0

    return jsonify({

        "success": True,

        "message": "Conversation cleared."

    })

# ===================================================
# END OF NEW CODE
# ===================================================


if __name__ == "__main__":

    app.run(

        debug=True

    )
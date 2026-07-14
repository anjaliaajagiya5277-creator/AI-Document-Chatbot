"""
chatbot.py

Gemini-powered AI Document Chatbot using RAG.
"""

import google.generativeai as genai

from config import Config
from rag import RAGRetriever


class DocumentChatbot:
    def get_history_stats(self):

        return {

            "total_questions": len(self.chat_history),

            "conversation_active": len(self.chat_history) > 0

        }

    def __init__(self):

        if not Config.GOOGLE_API_KEY:

            raise ValueError(
                "GOOGLE_API_KEY not found in .env"
            )

        genai.configure(
            api_key=Config.GOOGLE_API_KEY
        )

        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME
        )

        
        # Conversation memory

        self.chat_history = []

    # --------------------------------------------------------
    # Build Prompt
    # --------------------------------------------------------

    def build_prompt(self, question, documents):

        context = ""

        for doc in documents:

            metadata = doc.metadata

            source = metadata.get("source", "Unknown")

            page = metadata.get("page")

            slide = metadata.get("slide")

            chunk = metadata.get("chunk_id")

            context += f"""

    ========================================

    Source File : {source}

    """

            if page:

                context += f"Page : {page}\n"

            if slide:

                context += f"Slide : {slide}\n"

            context += f"""

    Chunk : {chunk}

    Content:

    {doc.page_content}

    """

        prompt = f"""
    You are an expert AI Document Assistant.

    Your ONLY knowledge source is the DOCUMENT CONTEXT below.

    STRICT RULES

    1. Answer ONLY using the provided document context.

    2. Never use your own knowledge.

    3. Never guess.

    4. Never invent information.

    5. If the answer is not present, reply EXACTLY:

    "I could not find this information in the uploaded document."

    6. Keep answers professional.

    7. Use bullet points whenever appropriate.

    8. If the document contains a definition,
    give the definition first.

    9. If the answer spans multiple pages,
    combine the information.

    10. Mention page numbers or slide numbers whenever available.

    11. Never mention that you are an AI model.

    ==================================================

    DOCUMENT CONTEXT

    {context}

    ==================================================

    QUESTION

    {question}

    ==================================================

    FINAL ANSWER
    """

        return prompt
    
    def build_history(self):

        """
        Convert previous conversation
        into prompt text.
        """

        if not self.chat_history:

            return ""

        history = ""

        for item in self.chat_history[-5:]:

            history += f"""

    User:
    {item["question"]}

    Assistant:
    {item["answer"]}

    """

        return history
    # --------------------------------------------------------
    # Ask Question
    # --------------------------------------------------------

    def ask(
        self,
        question,
        db_path="vector_db"
    ):

        try:

            # Load correct vector database

            retriever = RAGRetriever(
                db_path=db_path
            )

            retrieval = retriever.retrieve(

                question,

                k=5

            )

            documents = retrieval["documents"]

            sources = retrieval["sources"]

            if not documents:

                return {

                    "answer":
                    "I could not find this information in the uploaded document.",

                    "sources": []

                }

            history = self.build_history()

            prompt = self.build_prompt(

                question,

                documents

            )

            prompt = f"""

            Previous Conversation

            {history}

            --------------------------------------

            {prompt}

            """

            response = self.model.generate_content(

                prompt,

                generation_config={

                "temperature": 0.1,

                "top_p": 0.8,

                "top_k": 20,

                "max_output_tokens": 1500

                }
            )

            answer = ""

            if hasattr(response, "text"):

                answer = response.text.strip()

            if not answer:

                answer = "No response generated."

            self.chat_history.append({

                "question": question,

                "answer": answer,

                "sources": sources

            })

            # Keep only the last 10 exchanges
            if len(self.chat_history) > 10:

                self.chat_history.pop(0)

            return {

                "answer": answer,

                "sources": sources

            }
        

        except Exception as e:

            print("\nGemini Exception\n")

            print(e)

            return {

                "answer":
                "Sorry, an internal AI error occurred while processing your question.",

                "sources": []

            }
            # ----------------------------------------------------------
    # Generate AI Summary
    # ----------------------------------------------------------

    def generate_summary(self, db_path="vector_db"):

        """
        Generates an AI summary of the uploaded document.
        """

        try:

            retriever = RAGRetriever(db_path=db_path)

            retrieval = retriever.retrieve(

                "Summarize the entire uploaded document.",

                k=10

            )

            documents = retrieval["documents"]

            if not documents:

                return "No document available for summarization."

            context = ""

            for doc in documents:

                context += doc.page_content

                context += "\n\n"

            prompt = f"""
You are an AI Document Summarizer.

Your task is to summarize the uploaded document.

Rules:

1. Use ONLY the provided document.

2. Do NOT add outside knowledge.

3. Write in simple English.

4. Produce a concise summary.

5. Highlight the most important topics.

6. Keep the summary under 200 words.

-------------------------------------

DOCUMENT

{context}

-------------------------------------

SUMMARY
"""

            response = self.model.generate_content(

                prompt,

                generation_config={

                    "temperature": 0.2,

                    "max_output_tokens": 400

                }

            )

            if hasattr(response, "text"):

                return response.text.strip()

            return "Unable to generate summary."

        except Exception as e:

            print("Summary Error:", e)

            return "Unable to generate document summary."
    def clear_history(self):

        self.chat_history.clear()
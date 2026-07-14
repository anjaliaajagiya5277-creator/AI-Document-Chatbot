"""
rag.py

Retrieval-Augmented Generation (RAG)
Retrieves the most relevant document chunks
from the FAISS vector database.
"""

from vector_store import VectorStore

class RAGRetriever:

    def __init__(self, db_path="vector_db"):

        self.vector_store = VectorStore(
            db_path=db_path
        )
    # -------------------------------------------------

    def retrieve_documents(self, question, k=5):

        """
        Returns the top-k most relevant chunks.
        """

        try:

            results = self.vector_store.similarity_search(
                question,
                k=k
            )

            return results

        except Exception as e:

            print("Retriever Error :", e)

            return []

    # -------------------------------------------------

    def build_context(self, retrieved_documents):

        """
        Converts retrieved LangChain Documents
        into a single context string.
        """

        context = ""

        for document in retrieved_documents:

            metadata = document.metadata

            source = metadata.get("source", "Unknown")

            page = metadata.get("page")

            slide = metadata.get("slide")

            chunk = metadata.get("chunk_id")

            context += "\n---------------------------------\n"

            context += f"Source : {source}\n"

            if page is not None:

                context += f"Page : {page}\n"

            if slide is not None:

                context += f"Slide : {slide}\n"

            context += f"Chunk : {chunk}\n\n"

            context += document.page_content

            context += "\n"

        return context

    # -------------------------------------------------

    def get_sources(self, retrieved_documents):

        """
        Returns detailed source information
        for frontend citation cards.
        """

        sources = []

        for document in retrieved_documents:

            metadata = document.metadata

            info = {

                "source": metadata.get("source", "Unknown"),

                "page": metadata.get("page"),

                "slide": metadata.get("slide"),

                "chunk_id": metadata.get("chunk_id"),

                "chunk_index": metadata.get("chunk_index"),

                "preview": document.page_content[:250] + "..."

                if len(document.page_content) > 250

                else document.page_content

            }

            sources.append(info)

        return sources
    # -------------------------------------------------

    def retrieve(self, question, k=5):

        """
        Complete retrieval pipeline.
        """

        documents = self.retrieve_documents(

            question,

            k

        )
        print("\n====================")
        print("QUESTION:", question)
        print("Retrieved:", len(documents))
        print("====================")

        for doc in documents:
            print(doc.metadata)
            print(doc.page_content[:200])
            print("----------------")

        context = self.build_context(

            documents

        )

        sources = self.get_sources(

            documents

        )

        return {

            "documents": documents,

            "context": context,

            "sources": sources

        }
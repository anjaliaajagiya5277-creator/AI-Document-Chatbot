"""
vector_store.py

Creates, saves, loads and searches
a FAISS Vector Store.
"""

import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStore:

    def __init__(
        self,
        db_path="vector_db"
    ):

        self.db_path = db_path

        os.makedirs(
            self.db_path,
            exist_ok=True
        )

        self.embedding_model = HuggingFaceEmbeddings(

            model_name="BAAI/bge-small-en-v1.5",

            model_kwargs={
                "device": "cpu"
            },

            encode_kwargs={
                "normalize_embeddings": True
            }

        )

        self.vector_db = None

    # --------------------------------------------------

    def create_vector_store(
        self,
        documents
    ):

        self.vector_db = FAISS.from_documents(

            documents,

            self.embedding_model

        )

        return self.vector_db

    # --------------------------------------------------

    def save_vector_store(self):

        if self.vector_db is None:

            raise Exception(
                "Vector database has not been created."
            )

        self.vector_db.save_local(

            self.db_path

        )

    # --------------------------------------------------

    def load_vector_store(self):

        if self.vector_db is not None:

            return self.vector_db

        faiss_file = os.path.join(

            self.db_path,

            "index.faiss"

        )

        if not os.path.exists(faiss_file):

            raise FileNotFoundError(

                f"FAISS index not found in {self.db_path}"

            )

        self.vector_db = FAISS.load_local(

            self.db_path,

            self.embedding_model,

            allow_dangerous_deserialization=True

        )

        return self.vector_db

    # --------------------------------------------------

    def similarity_search(
        self,
        query,
        k=4
    ):

        vector_db = self.load_vector_store()

        return vector_db.similarity_search(

            query,

            k=k

        )

    # --------------------------------------------------

    def similarity_search_with_score(
        self,
        query,
        k=4
    ):

        vector_db = self.load_vector_store()

        return vector_db.similarity_search_with_score(

            query,

            k=k

        )

    # --------------------------------------------------

    def delete_vector_store(self):

        for filename in [

            "index.faiss",

            "index.pkl"

        ]:

            filepath = os.path.join(

                self.db_path,

                filename

            )

            if os.path.exists(filepath):

                os.remove(filepath)

    # --------------------------------------------------

    def vector_store_exists(self):

        return os.path.exists(

            os.path.join(

                self.db_path,

                "index.faiss"

            )

        )
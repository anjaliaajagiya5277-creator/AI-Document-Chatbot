"""
embeddings.py

Centralized HuggingFace embedding model used
throughout the RAG application.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingModel:

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):

        self.model = HuggingFaceEmbeddings(

            model_name=model_name,

            model_kwargs={

                "device": "cpu"

            },

            encode_kwargs={

                "normalize_embeddings": True

            }

        )

    # ------------------------------------------------

    def get_embedding_model(self):

        """
        Returns LangChain-compatible embedding model.
        """

        return self.model
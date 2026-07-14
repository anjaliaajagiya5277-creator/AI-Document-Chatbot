"""
text_chunker.py

Splits extracted document text into semantic chunks
and converts them into LangChain Document objects.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextChunker:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                "; ",
                ", ",
                " ",
                ""
            ]
        )

    # --------------------------------------------------------

    def create_documents(
        self,
        extracted_data,
        source_name
    ):

        documents = []

        chunk_id = 1

        for item in extracted_data:

            text = str(item.get("text", "")).strip()

            if not text:
                continue

            chunks = self.splitter.split_text(text)

            total_chunks = len(chunks)

            for index, chunk in enumerate(chunks):

                chunk = chunk.strip()

                if not chunk:
                    continue

                metadata = {

                    "chunk_id": chunk_id,

                    "chunk_index": index + 1,

                    "total_chunks": total_chunks,

                    "source": source_name,

                    "chunk_length": len(chunk)

                }

                # PDF

                if "page" in item:

                    metadata["page"] = item["page"]

                    metadata["document_type"] = "pdf"

                # PPT

                if "slide" in item:

                    metadata["slide"] = item["slide"]

                    metadata["document_type"] = "ppt"

                document = Document(

                    page_content=chunk,

                    metadata=metadata

                )

                documents.append(document)

                chunk_id += 1

        return documents

    # --------------------------------------------------------

    def statistics(
        self,
        documents
    ):

        if not documents:

            return {

                "total_chunks": 0,

                "total_characters": 0,

                "average_chunk_size": 0,

                "largest_chunk": 0,

                "smallest_chunk": 0

            }

        lengths = [

            len(doc.page_content)

            for doc in documents

        ]

        total_characters = sum(lengths)

        return {

            "total_chunks": len(documents),

            "total_characters": total_characters,

            "average_chunk_size": round(

                total_characters / len(documents),

                2

            ),

            "largest_chunk": max(lengths),

            "smallest_chunk": min(lengths)

        }

    # --------------------------------------------------------

    def preview_chunks(
        self,
        documents,
        limit=5
    ):

        preview = []

        for document in documents[:limit]:

            preview.append({

                "metadata": document.metadata,

                "text": document.page_content[:250]

            })

        return preview
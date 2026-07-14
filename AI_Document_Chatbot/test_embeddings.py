from document_loader import DocumentLoader
from text_chunker import TextChunker
from embeddings import EmbeddingModel

loader = DocumentLoader("uploads/sample.pdf")

data = loader.load_document()

chunker = TextChunker()

documents = chunker.create_documents(
    data,
    "sample.pdf"
)

embedding_model = EmbeddingModel()

vectors = embedding_model.embed_documents(
    documents
)

print("Number of chunks:", len(documents))
print("Embedding shape:", vectors.shape)
print("Dimension:", embedding_model.get_dimension())
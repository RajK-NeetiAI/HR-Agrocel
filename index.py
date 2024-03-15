from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain.vectorstores.qdrant import Qdrant

import config


def create_index(document_dir: str) -> str:
    try:
        loader = DirectoryLoader(
            document_dir,
            glob='**/*.docx',
            loader_cls=Docx2txtLoader,
            show_progress=True
        )
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=32
        )
        texts = text_splitter.split_documents(documents)
        Qdrant.from_documents(
            texts,
            config.embedding_function,
            collection_name=config.COLLECTION_NAME,
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY
        )
        return 'Documents uploaded and index created successfully. You can chat now.'
    except Exception as e:
        return e

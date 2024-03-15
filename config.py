import os

from dotenv import load_dotenv, find_dotenv
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from openai import OpenAI

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')

ERROR_MESSAGE = 'We are facing a technical issue at this moment.'
DIALOGFLOW_LANGUAGE = 'en-US'

COLLECTION_NAME = 'hr_knowledge'
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

K = 10

qdrant_client = QdrantClient(
    url=QDRANT_URL, https=True, api_key=QDRANT_API_KEY)

embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY
)

chat_model = ChatOpenAI(
    temperature=0,
    openai_api_key=OPENAI_API_KEY,
    model_name=OPENAI_MODEL_NAME
)

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

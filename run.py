import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel

from gradio_ui import demo
from conversation import create_llm_conversation_backend

app = FastAPI()


class ValuesChatRequest(BaseModel):
    query: str
    chat_history: list[list]


@app.get('/')
def home():
    return {
        'status': 1,
        'response': 'API is working, Gradio UI is running at /gradio'
    }


@app.post('/values/chat')
def values_chat(values_chat_request: ValuesChatRequest):
    query = values_chat_request.query
    chat_history = values_chat_request.chat_history
    response = create_llm_conversation_backend(chat_history, query)
    return {
        'status': 1,
        'response': response
    }


app = gr.mount_gradio_app(app, demo, '/gradio')

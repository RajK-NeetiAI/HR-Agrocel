import gradio as gr
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from gradio_ui import demo
from utils import format_dialogflow_response
from conversation import create_llm_conversation_backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ValuesChatRequest(BaseModel):
    query: str
    chat_history: list[list]


@app.get('/')
def home():
    return {
        'status': 1,
        'response': 'API is working, Gradio UI is running at /gradio'
    }


@app.post('/hr/chat')
def values_chat(values_chat_request: ValuesChatRequest):
    query = values_chat_request.query
    chat_history = values_chat_request.chat_history
    response = create_llm_conversation_backend(chat_history, query)
    return {
        'status': 1,
        'response': response
    }


@app.post('/dialogflow/webhook')
async def dialogflow_webhook(request: Request):
    body = await request.json()
    action = body['queryResult']['action']
    response_data = {}

    response_data = format_dialogflow_response([
        f'No handler is set for the action - {action}.'
    ])

    return response_data

app = gr.mount_gradio_app(app, demo, '/gradio')

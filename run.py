import time

import gradio as gr
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from gradio_ui import demo
from utils import format_dialogflow_response, detect_intent
import config

app = FastAPI()


class ValuesChatRequest(BaseModel):
    query: str
    session_id: str


@app.middleware("http")
async def authenticate_headers(request: Request, call_next):
    start_time = time.time()
    headers = request.headers
    for k, v in headers.items():
        if k == 'authentication':
            print(v)
    response = await call_next(request)
    process_time = time.time() - start_time
    print(process_time)
    return response


@app.get('/')
def home():
    return {
        'status': 1,
        'response': 'API is working, Gradio UI is running at /gradio'
    }


@app.post('/hr/chat')
def values_chat(values_chat_request: ValuesChatRequest):
    query = values_chat_request.query
    session_id = values_chat_request.session_id
    response = detect_intent(session_id, query, config.DIALOGFLOW_LANGUAGE)
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

    return JSONResponse(response_data)

app = gr.mount_gradio_app(app, demo, '/gradio')

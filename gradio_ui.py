import gradio as gr

from conversation import *

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label='HR Knowledge', bubble_full_width=False)
    with gr.Row():
        level = gr.Dropdown(
            choices=['M-0', 'M-1', 'M-2', 'M-3', 'M-4', 'M-5',
                     'M-6', 'M-7', 'M-8', 'M-9', 'M-10', 'M-11', 'M-12'],
            label='Select Employee Level'
        )
        msg = gr.Textbox(
            label='Query', placeholder='Enter text and press enter')
    text_chat_clear = gr.ClearButton([msg, chatbot], variant='stop')

    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        create_llm_conversation,
        [level, chatbot],
        [chatbot]
    )

demo.queue()

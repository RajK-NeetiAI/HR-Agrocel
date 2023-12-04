import gradio as gr

from conversation import *

with gr.Blocks() as text_chat:
    chatbot = gr.Chatbot(label='Talk to the Douments', bubble_full_width=False)
    msg = gr.Textbox(label='Query', placeholder='Enter text and press enter')
    text_chat_clear = gr.ClearButton([msg, chatbot], variant='stop')

    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        create_llm_conversation,
        [chatbot],
        [chatbot]
    )

with gr.Blocks() as voice_chat:
    chatbot = gr.Chatbot(label='Talk to the Douments', bubble_full_width=False)
    audio_msg = gr.Textbox(visible=False)

    with gr.Row():
        voice_chat_audio_file_path = gr.Audio(
            sources=["microphone"], label='Record your query', type='filepath')
        output_audio = gr.Audio(label='Chatbot response', type='filepath')

    voice_chat_clear = gr.ClearButton(
        [voice_chat_audio_file_path, chatbot, output_audio], variant='stop')

    voice_chat_audio_file_path.stop_recording(
        handle_user_voice_query,
        [voice_chat_audio_file_path, chatbot],
        [voice_chat_audio_file_path, chatbot]
    ).then(
        create_llm_conversation_audio,
        [chatbot],
        [chatbot, audio_msg]
    ).then(
        set_audio_output,
        [audio_msg],
        [output_audio]
    )


demo = gr.TabbedInterface([text_chat, voice_chat],
                          ['Text Chat', 'Voice Chat'], css='footer {visibility: hidden}')

demo.queue()

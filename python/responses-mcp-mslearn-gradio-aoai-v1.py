import os
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv

# Load configuration settings from a .env file
load_dotenv()

# Set the demo title for the top of the app, otherwise leave blank to allow to maximize space
demo_title = ""

# Set up the Azure OpenAI client and deployment
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
client = OpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    base_url=os.environ["AZURE_OPENAI_API_ENDPOINT"].rstrip("/") + "/openai/v1/",
)

# Global variable to store the response identifier from the last API call
previous_response_id = None

def chat_stream(user_prompt, history):
    """
    Handles a chat interaction by:
    1. Adding the user's message to the conversation history.
    2. Creating a placeholder for the assistant's reply.
    3. Beginning a streamed API call to get the response.
    4. Appending streamed chunks to the assistant's message and yielding updates.
    """
    # Ensure the history list is initialized
    if history is None:
        history = []
    
    # Add the user prompt to the conversation history with appropriate role
    history.append({"role": "user", "content": user_prompt})
    
    # Create and add a placeholder for the assistant's reply
    assistant_message = {"role": "assistant", "content": ""}
    history.append(assistant_message)
    
    # Yield initial state to update the UI
    yield history, history

    # Set up API call parameters, specifying the deployment, user input, streaming, and tool configuration
    global previous_response_id
    params = {
        "model": deployment,
        "input": [{"role": "user", "content": user_prompt}],
        "stream": True,
        "tools": [
            {
                "type": "mcp",
                "server_label": "MicrosoftDocs",
                "server_url": "https://learn.microsoft.com/api/mcp",
                "require_approval": "never",
            },
        ]
    }

    # Attach the previous response ID for context if available
    if previous_response_id:
        params["previous_response_id"] = previous_response_id

    # Initiate the streaming conversation using the client
    stream = client.responses.create(**params)

    # Buffer for streamed output text
    output_text_buffer = ""
    output_text_started = False

    for event in stream:
        # Record the response id from the first event
        if event.type == 'response.created':
            previous_response_id = event.response.id

        # Stream in output text (grey section)
        if event.type == 'response.output_text.delta':
            if event.delta:
                output_text_buffer += event.delta
                output_text_started = True  # Set flag when output_text starts

        # On any output update, re-render the assistant message
        if event.type in ('response.output_text.delta', 'response.output_text.done'):
            # show raw text only, no outer container
            content = output_text_buffer if output_text_started else ""
            assistant_message["content"] = content
            yield history, history

    # Final update after stream ends
    # raw final text
    content = output_text_buffer if output_text_started else ""
    assistant_message["content"] = content
    yield history, history

def clear_chat():
    """
    Resets the conversation state by clearing the chat history and previous response identifier.
    """
    global previous_response_id
    previous_response_id = None
    return [], []

# Clears the textbox input
def clear_textbox():
    return ""

CUSTOM_CSS = """
/* Make the overall app use the full viewport height and let inner flex items shrink/expand. */
.gradio-container { height: 100vh; }

/* Force the main layout to be a vertical flex stack. */
#layout { height: 100%; display: flex; flex-direction: column; min-height: 0; }

/* Let the chatbot area take remaining space and scroll internally. */
#chatbot { flex: 1 1 auto; min-height: 0; }
#chatbot [aria-label="chatbot conversation"] { height: 100%; overflow: auto; }

/* Make the input box multi-line and allow the user to resize it vertically. */
#msg textarea { resize: vertical !important; overflow: auto !important; min-height: 3.5rem; }
"""

# Build the Gradio Blocks interface for the chat demo
with gr.Blocks(fill_height=True, fill_width=True, css=CUSTOM_CSS) as demo:
    with gr.Column(elem_id="layout"):
        # Header Markdown text for the demo UI, centered
        if demo_title != "":
            gr.Markdown(f"<h2 style='text-align: center;'>{demo_title}</h2>")

        # Chatbot component to display messages stored in a list of role-content dictionaries
        chatbot = gr.Chatbot(type="messages", render_markdown=True, sanitize_html=False, elem_id="chatbot")

        # State to maintain the conversation history between messages
        state = gr.State([])

        # Textbox for user input with a placeholder message
        msg = gr.Textbox(
            show_label=False,
            placeholder="Type your message here and press Enter",
            lines=2,
            max_lines=12,
            elem_id="msg",
        )

        # Row containing the Submit and Clear buttons
        with gr.Row():
            submit_btn = gr.Button("Submit")
            clear_btn = gr.Button("Clear")

        # Bind the Textbox submit action to the stream processing function and clear the textbox after submission
        msg.submit(fn=chat_stream, inputs=[msg, state], outputs=[chatbot, state]).then(
            clear_textbox, None, msg
        )

        # Also bind the submit button to the same functionality as the Textbox submit
        submit_btn.click(fn=chat_stream, inputs=[msg, state], outputs=[chatbot, state]).then(
            clear_textbox, None, msg
        )

        # Bind the clear button to reset the chat and clear the file upload
        clear_btn.click(fn=clear_chat, inputs=[], outputs=[chatbot, state])

# Launch the Gradio demo application
demo.launch()

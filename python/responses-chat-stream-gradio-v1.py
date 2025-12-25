import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
import base64

# Load configuration settings from a .env file
load_dotenv()

# Set the demo title for the top of the app, otherwise leave blank to allow to maximize space
demo_title = ""

# Set the AI host to Azure, OpenAI, or GitHub Models (coming soon)
AIhost = "AzureOpenAI" # set to "AzureOpenAI", "OpenAI", or "GitHub" based on your requirement

def get_client(host: str):
    """
    Returns the deployment and client based on the specified host.
    Exits the application if an unsupported host is provided.
    """
    if host == "AzureOpenAI":
        deployment = os.getenv("AZURE_OPENAI_API_MODEL")
        client = OpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),
        )
    elif host == "OpenAI":
        deployment = "gpt-5"
        client = OpenAI()
    elif host == "GitHub":
        deployment = "gpt-5"
        print("GitHub Models are not yet supported in this demo. Please check back later.")
        exit(0)
    else:
        print("Invalid AI host specified. Please set AIhost to 'AzureOpenAI', 'OpenAI', or 'GitHub', and provide the configuration in the .env file")
        exit(0)
    return deployment, client

# Set the AI host to Azure, OpenAI, or GitHub Models (coming soon)
deployment, client = get_client(AIhost)

# Global variable to store the response identifier from the last API call
previous_response_id = None

def encode_image(image_path):
    """
    Opens the specified image file, encodes it in base64, and returns the encoded string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chat_stream(user_prompt, history, file_path):
    """
    Handles a chat interaction by:
    1. Adding the user's message to the conversation history.
    2. Creating a placeholder for the assistant's reply.
    3. Beginning a streamed API call to get the response.
    4. Appending streamed chunks to the assistant's message and yielding updates.
    
    If an image file is provided via file_path, it will be encoded and sent along with the user's input.
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

    # Prepare parameters for the API call, including model name and streaming flag
    global previous_response_id
    params = {
        "model": deployment,
        "input": [{"role": "user", "content": user_prompt}],
        "stream": True,
        "text": {"verbosity": "medium"}
    }
    
    # Add reasoning parameters if the model supports it
    if deployment in ["o4-mini", "o3", "gpt-5"]:
        params["reasoning"] = {
            "effort": "high",
            "summary": "auto"
        }

    # Attach the previous response ID for context if available
    if previous_response_id:
        params["previous_response_id"] = previous_response_id

    # If an image file was uploaded, encode it to base64 and add it to the input payload
    if file_path is not None:
        base64_image = encode_image(file_path)
        params["input"].append({
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image}"
                }
            ]
        })

    # Initiate the streaming conversation using the client
    stream = client.responses.create(**params)

    # Buffers for streamed content
    reasoning_summary_buffer = []
    output_text_buffer = ""
    reasoning_summary_present = False
    output_text_started = False  # Track if output_text has started

    for event in stream:
        # Record the response id from the first event
        if event.type == 'response.created':
            previous_response_id = event.response.id

        # Collect reasoning summary text (may be multi-part)
        if event.type == 'response.reasoning_summary_text.delta':
            reasoning_summary_present = True
            if event.delta:
                if not reasoning_summary_buffer or getattr(event, "new_part", False):
                    reasoning_summary_buffer.append("")
                reasoning_summary_buffer[-1] += event.delta

        # Start a new reasoning summary part
        if event.type == 'response.reasoning_summary_part.added':
            reasoning_summary_present = True
            reasoning_summary_buffer.append("")

        # Stream in output text (grey section)
        if event.type == 'response.output_text.delta':
            if event.delta:
                output_text_buffer += event.delta
                output_text_started = True  # Set flag when output_text starts

        # On any update, re-render the assistant message
        if event.type in (
            'response.reasoning_summary_text.delta',
            'response.reasoning_summary_text.done',
            'response.reasoning_summary_part.added',
            'response.reasoning_summary_part.done',
            'response.output_text.delta',
            'response.output_text.done'
        ):
            content = ""
            # Render reasoning summary section if present and has content
            if reasoning_summary_present and any(reasoning_summary_buffer):
                def render_reasoning_part(part):
                    # Split into lines, convert first line markdown bold to HTML bold
                    lines = part.splitlines()
                    if lines and lines[0].startswith("**") and lines[0].endswith("**"):
                        # Remove the leading/trailing '**' and wrap in <strong>
                        title = lines[0][2:-2]
                        lines[0] = f"<strong>{title}</strong>"
                    return "\n".join(lines)
                summary_text = "\n\n".join(render_reasoning_part(part) for part in reasoning_summary_buffer if part)
                content += (
                    "<div style='background-color:#e0f0ff;padding:10px;border-radius:5px;margin-bottom:10px;'>"
                    "<details open><summary><strong>Reasoning Summary</strong></summary>\n"
                    f"{summary_text}\n"
                    "</details></div>"
                )
            # Only render output text bubble if output_text has started
            if output_text_started:
                content += (
                    "<div style='background-color:#f0f0f0;padding:10px;border-radius:5px;'>"
                    f"{output_text_buffer}"
                    "</div>"
                )
            assistant_message["content"] = content
            yield history, history

    # Final update after stream ends (in case of any missed updates)
    content = ""
    if reasoning_summary_present and any(reasoning_summary_buffer):
        def render_reasoning_part(part):
            lines = part.splitlines()
            if lines and lines[0].startswith("**") and lines[0].endswith("**"):
                title = lines[0][2:-2]
                lines[0] = f"<strong>{title}</strong>"
            return "\n".join(lines)
        summary_text = "\n\n".join(render_reasoning_part(part) for part in reasoning_summary_buffer if part)
        content += (
            "<div style='background-color:#e0f0ff;padding:10px;border-radius:5px;margin-bottom:10px;'>"
            "<details open><summary><strong>Reasoning Summary</strong></summary>\n"
            f"{summary_text}\n"
            "</details></div>"
        )
    # Only render output text bubble if output_text has started
    if output_text_started:
        content += (
            "<div style='background-color:#f0f0f0;padding:10px;border-radius:5px;'>"
            f"{output_text_buffer}"
            "</div>"
        )
    assistant_message["content"] = content
    yield history, history

def clear_chat():
    """
    Resets the conversation state by clearing the chat history, previous response identifier,
    and the file upload.
    """
    global previous_response_id
    previous_response_id = None
    return [], [], None

# Clears the textbox input
def clear_textbox():
    return ""

# Build the Gradio Blocks interface for the chat demo
with gr.Blocks(fill_height=True, fill_width=True) as demo:
    # Header Markdown text for the demo UI, centered
    if demo_title != "":
        gr.Markdown(f"<h2 style='text-align: center;'>{demo_title}</h2>")
    
    # Chatbot component to display messages stored in a list of role-content dictionaries
    chatbot = gr.Chatbot(type="messages", scale=1, render_markdown=True, sanitize_html=False)
    
    # State to maintain the conversation history between messages
    state = gr.State([])

    # Textbox for user input with a placeholder message
    msg = gr.Textbox(show_label=False, placeholder="Type your message here and press Enter")

    # Row containing the Submit and Clear buttons
    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn = gr.Button("Clear")
    
    # Move the file upload control into an accordion at the bottom
    with gr.Accordion("Click to upload an image (optional)", open=False):
        file_picker = gr.File(
            label="Choose an image file",
            file_count="single",
            type="filepath",
            file_types=[".jpg", ".jpeg", ".png"],
            height=140
        )
    
    # Bind the Textbox submit action to the stream processing function and clear the textbox after submission
    msg.submit(fn=chat_stream, inputs=[msg, state, file_picker], outputs=[chatbot, state]).then(
        clear_textbox, None, msg
    )
    
    # Also bind the submit button to the same functionality as the Textbox submit
    submit_btn.click(fn=chat_stream, inputs=[msg, state, file_picker], outputs=[chatbot, state]).then(
        clear_textbox, None, msg
    )
    
    # Bind the clear button to reset the chat and clear the file upload
    clear_btn.click(fn=clear_chat, inputs=[], outputs=[chatbot, state, file_picker])

# Launch the Gradio demo application
demo.launch()
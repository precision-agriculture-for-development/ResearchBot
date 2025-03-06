# from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st


# load_dotenv()



# Moderation check
def moderation_endpoint(client: OpenAI, text: str) -> bool:
    """
    Checks if the text is triggers the moderation endpoint

    Args:
    - text (str): The text to check

    Returns:
    - bool: True if the text is flagged
    """
    response = client.moderations.create(input=text)
    return response.results[0].flagged

def assistant():

    if "openai" not in st.session_state:
        st.session_state.openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    client = st.session_state.openai

    # Retrieve the assistant you want to use
    if "assistant" not in st.session_state:
        st.session_state.assistant = client.beta.assistants.retrieve(
            st.secrets["ASSISTANT_ID"]
        )

    assistant = st.session_state.assistant

    # Create the title and subheader for the Streamlit page
    st.set_page_config(page_title="Researchy", page_icon="🕵️", layout='wide')
    st.title("Researchy")

    # Apply custom CSS
    st.html("""
            <style>
                #MainMenu {visibility: hidden}
                #header {visibility: hidden}
                #footer {visibility: hidden}
                .block-container {
                    padding-top: 3rem;
                    padding-bottom: 2rem;
                    padding-left: 3rem;
                    padding-right: 3rem;
                    }
            </style>
            """)
    
    # UI
    st.subheader("🔮 Experiment Registry Engine")
    
    # # Create a status indicator to show the user the assistant is working
    # with st.status("Starting work...", expanded=False) as status_box:
    # Create a new thread
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Local history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    container = st.container(height=400)
        # UI
    for message in st.session_state.messages:
        with container.chat_message(message["role"]):
            for item in message["items"]:
                item_type = item["type"]
                if item_type == "text":
                    st.write(item["content"])
                elif item_type == "image":
                    for image in item["content"]:
                        st.html(image)
                elif item_type == "code_input":
                    with st.status("Code", state="complete"):
                        st.code(item["content"])
                elif item_type == "code_output":
                    with st.status("Results", state="complete"):
                        st.code(item["content"])

    if prompt := st.chat_input("Ask me a question about your experiments"):
        if moderation_endpoint(client, prompt):
            st.toast("Your message was flagged. Please try again.", icon="⚠️")
            st.stop

        st.session_state.messages.append({"role": "user",
                                        "items": [
                                            {"type": "text", 
                                            "content": prompt
                                            }]})
        
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # user = container.chat_message("user")
        
        chat = container.chat_message("user")
        chat.write(prompt)

        assistant_output = []

        with container.chat_message("assistant"):
            with client.beta.threads.runs.stream(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant.id) as stream:
            
                for sse in stream:
                    print(sse.event)
                    # Print the text from text delta events
                    if sse.event == "thread.message.created":
                        assistant_output.append({"type": "text",
                                        "content": ""})
                        assistant_text_box = st.empty()
                    if sse.event == "thread.message.delta" and sse.data.delta.content:
                        # assistant_text_box.empty()
                        assistant_output[-1]["content"] += sse.data.delta.content[0].text.value
                        assistant_text_box.markdown(assistant_output[-1]["content"])
                        print(sse.data.delta.content[0].text)
                        
            st.session_state.messages.append({"role": "assistant", "items": assistant_output})

if __name__ == "__main__":
    assistant()

import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid

def generate_thread_id():
    """Generates a unique ID for each chat thread."""
    return str(uuid.uuid4())

def reset_chat():
    """Initializes a new chat session."""
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []

def add_thread_with_title(thread_id, title):
    """Adds a new chat thread with a title based on the first user message."""
    # Truncate the title to keep it short and readable
    if len(title) > 30:
        title = title[:27] + '...'
    st.session_state['chat_threads'][thread_id] = title

def load_conversation(thread_id):
    """Loads messages from a specific chat thread."""
    try:
        state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
        return state.values.get('messages', [])
    except Exception as e:
        st.error(f"Failed to load conversation: {e}")
        return []

# Initialize session state variables
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# Use a dictionary to store threads: {thread_id: title}
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = {}

# --- Sidebar for Navigation ---
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# Display conversations using their titles
for thread_id, title in st.session_state['chat_threads'].items():
    if st.sidebar.button(title):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        # Format LangChain messages for Streamlit display
        temp_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})
        
        st.session_state['message_history'] = temp_messages

# --- Main Chat Interface ---
st.title('Resume Chatbot')

# Display the chat history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    # Append the user's message to the history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # If this is the first message in a new chat, create a title
    if st.session_state['thread_id'] not in st.session_state['chat_threads']:
        add_thread_with_title(st.session_state['thread_id'], user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    # Append the AI's response to the history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
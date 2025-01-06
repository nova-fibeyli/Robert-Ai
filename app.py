import streamlit as st
from llama_index.core.llms import ChatMessage
from pymongo import MongoClient
import logging
import time
import ollama

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://AdvancedProgramming:AdvancedProgramming@cluster0.uemob.mongodb.net/test?retryWrites=true&w=majority")
db = client.support_bot
dialogue_collection = db.dialogues

# Function to find response from MongoDB
def find_response(user_input):
    result = dialogue_collection.find_one({"prompt": {"$regex": user_input, "$options": "i"}})
    return result["utterance"] if result else None

# Function to store query and response in MongoDB
def store_query_response(user_input, assistant_response):
    dialogue_collection.insert_one({
        "prompt": user_input,
        "utterance": assistant_response,
        "timestamp": time.time()
    })
    logging.info(f"Stored query and response in MongoDB: {user_input} - {assistant_response}")

# Function to handle chat streaming
def stream_chat(model, messages):
    try:
        user_input = messages[-1].content if messages else ""
        if not user_input:
            return "I didn’t catch that. Could you say it again?"

        mongo_response = find_response(user_input) or "I am here to listen and help you. Please tell me more."
        logging.info(f"MongoDB Response: {mongo_response}")

        formatted_messages = [
            {"role": "system", "content": "You are an empathetic assistant."},
            {"role": "assistant", "content": mongo_response},
            {"role": "user", "content": user_input},
        ]

        response = ollama.chat(model=model, messages=formatted_messages)
        logging.info(f"Ollama Response: {response}")

        if response and hasattr(response, 'message') and hasattr(response.message, 'content'):
            return response.message.content
        else:
            logging.error("Ollama response structure is invalid.")
            return "I'm sorry, I couldn't process your request. Could you please rephrase?"

    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        return "An error occurred. Please try again later."

# Main app function
def main():
    st.title("Chat with Robert ['-']")
    logging.info("App started")

    # Session state to store messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    logging.info(f"Model selected: {model}")

    # Display messages (newest first)
    for message in reversed(st.session_state.messages):
        with st.chat_message(message.role):
            st.write(message.content)

    # Add input section at the bottom of the page
    st.markdown(
        """
        <style>
        .fixed-bottom {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f9f9f9;
            padding: 10px 15px;
            box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .message-area {
            padding-bottom: 70px;  /* To make space for the fixed input area */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display message area with padding to avoid overlap with input section
    st.markdown('<div class="message-area">', unsafe_allow_html=True)

    # Validate and display input components
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        prompt = st.text_input("Enter your question:", key="user_prompt")

    with col2:
        send_button = st.button("Send")

    with col3:
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

    st.markdown('</div>', unsafe_allow_html=True)

    # Validate input and file upload
    if send_button:
        if not prompt:
            st.error("Please enter text to send a message.")
        elif uploaded_file:
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size,
            }
            st.session_state.messages.append(ChatMessage(role="user", content=f"{prompt} (Uploaded file: {file_details})"))
            logging.info(f"User uploaded file with message: {prompt} | {file_details}")
        else:
            st.session_state.messages.append(ChatMessage(role="user", content=prompt))
            logging.info(f"User input: {prompt}")

        # Generate assistant response after input is sent
        if st.session_state.messages and st.session_state.messages[-1].role == "user":
            with st.chat_message("assistant"):
                response_container = st.empty()
                response_text = ""

                start_time = time.time()
                logging.info("Generating response")

                with st.spinner("Generating response..."):
                    try:
                        response_message = stream_chat(model, st.session_state.messages)

                        for chunk in response_message.split():
                            response_text += chunk + " "
                            response_container.write(response_text)
                            time.sleep(0.1)

                        duration = time.time() - start_time
                        response_text += f"\n\nResponse generated in {duration:.2f} seconds."

                        st.session_state.messages.append(ChatMessage(role="assistant", content=response_text))
                        logging.info(f"Response: {response_text}, Duration: {duration:.2f} sec.")

                        if prompt:
                            store_query_response(prompt, response_text)

                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append(ChatMessage(role="assistant", content=error_message))
                        st.error(error_message)
                        logging.error(error_message)

if __name__ == "__main__":
    main()


import streamlit as st
from llama_index.core.llms import ChatMessage
from pymongo import MongoClient
import logging
import time
import ollama
import pandas as pd
import fitz  # PyMuPDF for PDF processing

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://AdvancedProgramming:AdvancedProgramming@cluster0.uemob.mongodb.net/test?retryWrites=true&w=majority")
db = client.support_bot
dialogue_collection = db.dialogues

# Function to load dataset into MongoDB
def load_dataset():
    try:
        train_data = pd.read_csv("EmpatheticDialogues/train.csv")
        dialogues = train_data[["prompt", "utterance"]].drop_duplicates().dropna()
        dialogue_collection.insert_many(dialogues.to_dict(orient="records"), ordered=False)
        logging.info("EmpatheticDialogues dataset loaded into MongoDB.")
    except Exception as e:
        logging.info("Dataset already exists or encountered an error.")
load_dataset()

# Function to find response from MongoDB
def find_response(user_input):
    result = dialogue_collection.find_one({"prompt": {"$regex": user_input, "$options": "i"}})
    return result["utterance"] if result else "I am here to listen and help you. Please tell me more."

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

        mongo_response = find_response(user_input)
        logging.info(f"MongoDB Response: {mongo_response}")

        formatted_messages = [
            {"role": "system", "content": "You are an empathetic assistant."},
            {"role": "assistant", "content": mongo_response},
            {"role": "user", "content": user_input},
        ]

        response = ollama.chat(model=model, messages=formatted_messages)
        return response.message.content if response and hasattr(response, 'message') and hasattr(response.message, 'content') else "I'm sorry, I couldn't process your request."
    
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        return "An error occurred. Please try again later."

# Function to handle file upload
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "pdf":
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            file_text = "\n".join([page.get_text("text") for page in doc])
        else:
            file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        return file_text[:500]  # Preview the first 500 characters
    return ""

# Main app function
def main():
    st.title("Chat with Robert ['-']")
    logging.info("App started")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    logging.info(f"Model selected: {model}")

    for message in reversed(st.session_state.messages):
        with st.chat_message(message.role):
            st.write(message.content)

    prompt = st.text_input("Enter your question:", key="user_prompt")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
    send_button = st.button("Send")

    if send_button:
        file_text = handle_file_upload(uploaded_file)
        full_prompt = f"{prompt}\n\n[File Content Preview]: {file_text}" if file_text else prompt

        if not full_prompt.strip():
            st.error("Please enter text or upload a file.")
        else:
            st.session_state.messages.append(ChatMessage(role="user", content=full_prompt))
            logging.info(f"User input: {full_prompt}")

            with st.chat_message("assistant"):
                response_container = st.empty()
                response_text = ""
                start_time = time.time()

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

                        store_query_response(full_prompt, response_text)
                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append(ChatMessage(role="assistant", content=error_message))
                        st.error(error_message)
                        logging.error(error_message)

if __name__ == "__main__":
    main()

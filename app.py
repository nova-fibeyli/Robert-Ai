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
db = client.support_bot  # Replace with your actual database name
dialogue_collection = db.dialogues  # Replace with your actual collection name

# Function to find response from MongoDB
def find_response(user_input):
    """
    Query MongoDB to find a relevant response based on the user prompt.
    Args:
        user_input (str): The user's input.
    Returns:
        str: The retrieved response or None if not found.
    """
    result = dialogue_collection.find_one({"prompt": {"$regex": user_input, "$options": "i"}})
    return result["utterance"] if result else None

# Function to store query and response in MongoDB
def store_query_response(user_input, assistant_response):
    """
    Store the user query and assistant response in MongoDB.
    Args:
        user_input (str): The user's input message.
        assistant_response (str): The assistant's response.
    """
    dialogue_collection.insert_one({
        "prompt": user_input,
        "utterance": assistant_response,
        "timestamp": time.time()  # Storing the time of the query
    })
    logging.info(f"Stored query and response in MongoDB: {user_input} - {assistant_response}")

# Function to handle chat streaming
def stream_chat(model, messages):
    """
    Generates a response by combining MongoDB's context and Ollama's chat model.
    
    Args:
        model (str): The name of the Ollama model to use.
        messages (list): A list of chat messages, including user and assistant roles.
    
    Returns:
        str: The generated response content.
    """
    try:
        # Extract user input from the last message
        user_input = messages[-1].content if messages else ""
        if not user_input:
            return "I didn’t catch that. Could you say it again?"

        # Fetch response from MongoDB
        mongo_response = find_response(user_input) or "I am here to listen and help you. Please tell me more."

        # Log MongoDB response
        logging.info(f"MongoDB Response: {mongo_response}")

        # Format messages for Ollama, including the MongoDB context
        formatted_messages = [
            {"role": "system", "content": "You are an empathetic assistant."},
            {"role": "assistant", "content": mongo_response},
            {"role": "user", "content": user_input},
        ]

        # Call Ollama chat API
        response = ollama.chat(model=model, messages=formatted_messages)

        # Log Ollama response
        logging.info(f"Ollama Response: {response}")

        # Check the response structure and extract the content from 'message'
        if response and hasattr(response, 'message') and hasattr(response.message, 'content'):
            return response.message.content  # Directly access content inside 'message'
        else:
            logging.error("Ollama response structure is invalid.")
            return "I'm sorry, I couldn't process your request. Could you please rephrase?"

    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        return "An error occurred. Please try again later."

# Main app function
def main():
    """
    The main function for the Streamlit app.
    """
    st.title("Chat with Robert ['-']")
    logging.info("App started")

    # Initialize session state for messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Sidebar: Model selection
    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    logging.info(f"Model selected: {model}")

    # User input
    if prompt := st.chat_input("Your question"):
        # Append user message to session state
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        logging.info(f"User input: {prompt}")

        # Display all messages in the chat
        for message in st.session_state.messages:
            with st.chat_message(message.role):
                st.write(message.content)

        # Generate assistant response
        if st.session_state.messages[-1].role != "assistant":
            with st.chat_message("assistant"):
                # Simulate streaming partial results
                response_container = st.empty()  # Container for real-time updates
                response_text = ""

                start_time = time.time()
                logging.info("Generating response")

                with st.spinner("Generating response..."):
                    try:
                        # Fetch response from the chat function
                        response_message = stream_chat(model, st.session_state.messages)

                        # Simulate real-time streaming
                        for chunk in response_message.split():
                            response_text += chunk + " "
                            response_container.write(response_text)  # Update container
                            time.sleep(0.1)  # Simulate delay (optional)

                        duration = time.time() - start_time
                        response_text += f"\n\nResponse generated in {duration:.2f} seconds."

                        # Append final response to session state
                        st.session_state.messages.append(ChatMessage(role="assistant", content=response_text))
                        logging.info(f"Response: {response_text}, Duration: {duration:.2f} sec.")

                        # Store the query and response in MongoDB
                        store_query_response(prompt, response_text)

                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append(ChatMessage(role="assistant", content=error_message))
                        st.error(error_message)
                        logging.error(error_message)

if __name__ == "__main__":
    main()

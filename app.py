import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
import ollama

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Initialize session_state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to handle chat streaming
def stream_chat(model, messages):
    try:
        # Format messages as needed for ollama
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        # Call ollama.chat method with the formatted messages
        response = ollama.chat(model=model, messages=formatted_messages)
        
        # Log the full response to check its structure
        logging.info(f"Model: {model}, Messages: {messages}, Response: {response}")

        # Assuming the response has a 'message' attribute or something similar
        # Adjust this part based on the actual structure of the response
        if hasattr(response, 'message'):
            return response.message.get('content', "No content found")  # Check if 'message' contains 'content'
        else:
            logging.error("Response does not contain 'message' field.")
            return "Error: No valid response received."

    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        raise e

# Main app function
def main():
    st.title("Chat with Robert ['-']")
    logging.info("App started")

    # Model selection
    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    logging.info(f"Model selected: {model}")

    # User input
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        logging.info(f"User input: {prompt}")

        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message.role):
                st.write(message.content)

        # Generate response
        if st.session_state.messages[-1].role != "assistant":
            with st.chat_message("assistant"):
                # Stream partial results in real-time
                response_container = st.empty()  # Create a container for real-time updates
                response_text = ""

                start_time = time.time()
                logging.info("Generating response")

                with st.spinner("Generating response..."):
                    try:
                        # Fetch response from the chat API
                        response_message = stream_chat(model, st.session_state.messages)
                        
                        # Simulate streaming by updating the container
                        for chunk in response_message.split():
                            response_text += chunk + " "
                            response_container.write(response_text)  # Update the container in real-time
                            time.sleep(0.1)  # Simulate delay (optional)

                        duration = time.time() - start_time
                        response_text += f"\n\nDuration: {duration:.2f} seconds"
                        
                        # Append the final response to session state
                        st.session_state.messages.append(ChatMessage(role="assistant", content=response_text))
                        logging.info(f"Response: {response_text}, Duration: {duration:.2f} sec.")

                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append(ChatMessage(role="assistant", content=error_message))
                        st.error(error_message)
                        logging.error(error_message)

if __name__ == "__main__":
    main()

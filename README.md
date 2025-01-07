# Robert-Ai: Empathic Emotional Support Robo Friend

## Overview

Robert-Ai is an innovative application designed to provide empathetic emotional support. This bot combines cutting-edge technologies to deliver meaningful and helpful interactions for users seeking companionship and understanding. Additionally, Robert-Ai now includes document processing capabilities, allowing users to upload files and interact with their contents through intelligent query responses.

## Key Features

- **Python-Powered**: Developed using Python, a versatile and robust programming language.
- **MongoDB Integration**: Utilizes MongoDB to store and retrieve conversational data for context-aware responses. You can check the story in:
  https://cloud.mongodb.com/v2/677182969e97fe1106690865#/metrics/replicaSet/677183b107aecd340960ea9e/explorer/support_bot/dialogues/find
- **Streamlit Framework**: A user-friendly interface built with Streamlit for seamless interaction.
- **Ollama Integration**: Incorporates Ollama's advanced AI models for generating empathetic and human-like responses.
- **File Upload & Document Querying**:
  - Allows users to upload documents and ask questions about their content.
  - Supports **.txt, .pdf, and .docx** file uploads.
  - Extracts and processes content to provide **relevant responses** within the document's context.
  - Enhances user experience by offering meaningful document-based insights.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nova-fibeyli/Robert-Ai.git
   cd Robert-Ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application by running:

   ```bash
   streamlit run src/app.py
   ```

2. Enter your questions or messages, and Robert-Ai will respond empathetically.
3. **Upload files** (.txt, .pdf, .docx) and ask **questions** about their content.
4. Retrieve **document-specific responses** and engage with uploaded materials interactively.

## Examples

### **Conversational AI Example**

Ask a general question:

> "How are you feeling today?"

The bot will provide a thoughtful response, leveraging its training data and advanced AI models.

### **Document Processing Example**

If you upload a **PDF document** and ask:

> "What does this document say about artificial intelligence?"

Robert-Ai will extract relevant information from the document and provide a meaningful response based on its contents.

## Technologies Used

- **Python**: The backbone of this application for efficient scripting and development.
- **MongoDB**: A NoSQL database to store conversation history and facilitate dynamic responses.
- **Streamlit**: An interactive and intuitive framework for creating a friendly UI.
- **Ollama**: Advanced AI language models that enhance Robert-Ai's conversational capabilities.
- **PyMuPDF (fitz)**: Extracts text from uploaded PDF documents.
- **pymongo**: Enables communication between Robert-Ai and MongoDB.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Repository

Visit the project repository at [Robert-Ai GitHub Repository](https://github.com/nova-fibeyli/Robert-Ai.git).

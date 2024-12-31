# Robert AI

## Overview

Robert AI is a project designed to provide an efficient and scalable AI solution. This README provides a step-by-step guide on how to clone, set up, and run the project locally. Additionally, it includes instructions to pull required models (`llama3.2`, `phi3`) for optimal functionality and enable them to respond to user queries.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Git**: [Download Git](https://git-scm.com/)
2. **Python (3.8 or higher)**: [Download Python](https://www.python.org/downloads/)
3. **pip**: Comes with Python installation.

---

### Installation

#### 1. Clone the Repository

To get started, clone the repository from GitHub:
1. SSH key:
```bash
git clone git@github.com:nova-fibeyli/Robert-Ai.git
```
2. HTTPS key:
```bash
git clone https://github.com/nova-fibeyli/Robert-Ai.git
```
Alternatively, you can download the ZIP file of the repository:

1. Go to the repository page on GitHub.
2. Click the **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP file to your desired directory.

#### 2. Navigate to the Project Directory

Change into the project directory:

```bash
cd robert-ai
```

#### 3. Pull Required Models

Before running the AI, you need to pull the required models that enable user query responses:

1. Pull the `llama3.2` model:

   ```bash
   ollama pull llama3.2
   ```

2. Pull the `phi3` model:

   ```bash
   ollama pull phi3
   ```
---

### Usage
### Running the AI Application

#### 1. Start the AI

To start Robert AI, run the main application script:

```bash
streamlit run app.py
```

#### 2. Testing the AI

After starting the AI, you can interact with it via the terminal or through the user interface (if available). The models `llama3.2` and `phi3` will be utilized to provide responses.

---
### Examples
#### 1. Input a query:
```bash
What is the capital of France?
```
AI Response:
```bash
The capital of France is Paris.
```

---

### Additional Information

#### Configuration

- Configuration files (if any) are located in the `config/` directory.
- Update the configuration as per your requirements before starting the application.

#### Logs

Logs are stored in the `logs/` directory. Check this directory for debugging or tracking AI behavior.

---

## Troubleshooting

### Common Issues

- **Dependency Errors**: Ensure all dependencies in `requirements.txt` are installed.
- **Python Version Issues**: Check your Python version and upgrade if necessary.
- **Git Errors**: Ensure your Git credentials are configured properly.
  
---

### Support

If you encounter any issues, please raise them on the GitHub Issues page for this repository.

---

## License

This project is licensed under the Apache License. See the LICENSE file for more details.

---

Thank you for using Robert AI!



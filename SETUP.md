# 🛠️ Complete Setup Guide (From Scratch)

If you have just cloned this repository and want to run it on your system, follow this step-by-step guide. This covers everything from installing the AI engine (Ollama) to setting up the Python environment.

---

## Step 1: Install Ollama (The AI Engine)
This project uses **Ollama** to run the AI completely locally on your machine, meaning you do not need OpenAI API keys.

1. Go to the [Ollama Download Page](https://ollama.com/download)
2. Download the installer for your operating system (Windows, macOS, or Linux).
3. Run the installer and complete the setup.
4. Verify it's working by opening your terminal / command prompt and running:
   ```bash
   ollama --version
   ```

## Step 2: Download the Required AI Models
Once Ollama is installed and running in the background, you need to download the two specific models this project relies on.

Open your terminal and run these commands one by one:
1. Download the reasoning model:
   ```bash
   ollama pull llama3.2:3b
   ```
2. Download the embedding model (used to index your PDFs):
   ```bash
   ollama pull nomic-embed-text
   ```
*(This may take a few minutes depending on your internet connection as it downloads a few gigabytes of model data).*

## Step 3: Set up the Python Environment
Now you need to set up the actual Python code environment so it doesn't conflict with other projects on your computer.

1. **Open a terminal in the cloned project folder.**
   ```bash
   cd RAG_chatbot
   ```

2. **Create a fresh virtual environment:**
   - **Windows:**
     ```bash
     python -m venv venv
     ```
   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     .\venv\Scripts\Activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```
   *(You should see `(venv)` appear at the beginning of your terminal prompt).*

4. **Install all required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Configure the Project
The project uses an environment file to store configuration settings safely. 
Copy the provided example file to create your active configuration:

- **Windows:**
  ```powershell
  cp .env.example .env
  ```
- **Mac/Linux:**
  ```bash
  cp .env.example .env
  ```
*(If `.env.example` doesn't exist, don't worry! The code (`src/config.py`) has built-in defaults that connect to Ollama automatically).*

## Step 5: Add your PDFs
Before running the bot, it needs some documents to read!
1. Look for a folder named `rag-dataset/` in the project directory (create it if it doesn't exist).
2. Drop any `.pdf` files you want the chatbot to read into that folder.

## Step 6: Run the Chatbot!
Now everything is set up. To launch the chatbot and have it read your PDFs for the first time, run:

```bash
python -m src.main --rebuild --interactive
```

- `--rebuild` tells the program to read the PDFs in `rag-dataset/` and build the vector database.
- `--interactive` launches a continuous chat prompt in your terminal.

**For future runs** (once the database is already built), you can skip the rebuild flag to start instantly:
```bash
python -m src.main --interactive
```

---
🎉 **You're all set!** Type your questions into the terminal and the AI will answer based on your PDFs.

## 🚀 Alternative: Install via PyPI
If you prefer not to clone the repository, you can now install this project directly from PyPI (Python Package Index)!

1. Ensure Ollama is installed and the models are downloaded (Follow Steps 1 & 2 above).
2. Install the package using pip:
   ```bash
   pip install rag-pdf-chatbot
   ```
3. Run the chatbot:
   ```bash
   python -m src.main --interactive
   ```
*(Note: You will still need to configure your environment variables and provide a `rag-dataset/` folder in the directory where you run the command).*

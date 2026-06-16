# ZYLIEX-AI

**Zyliex-AI is a modular, local-first automation framework designed to streamline your daily workflow through a conversational interface.**

By leveraging the power of local LLMs (**Llama3 via Ollama**), Zyliex-AI allows you to control your operating system using natural language, ensuring your data remains **private and secure offline**.

---

## 🚀 KEY FEATURES

* **Local Intelligence:** Processes all commands locally using Llama3. No data leaves your machine.
* **App Launcher:** Search and launch any application directly from the interface.
* **Intelligent Code Builder:** Generate Python scripts on the fly and open them in your IDE.
* **Knowledge Management:** Quick-capture system for your notes and integrated web research.
* **Modern UI:** A clean, distraction-free, chat-based dashboard.

---

## 🛠 PREREQUISITES

* **Python 3.8+**
* **Ollama:** [Download here](https://ollama.com/) to run the Llama3 model locally.
* **VS Code:** Recommended for handling generated scripts.

---

## 📥 INSTALLATION

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zyliexy/Zyliex-AI.git
   cd Zyliex-AI

2. **Install dependencies:**
    ```bash
    pip install customtkinter requests pyperclip pyttsx3 duckduckgo-search
    
3. **Setup Ollama:**
Ensure Ollama is running in the background and pull the model
   ```bash
   ollama pull llama3
   
4. **Usage:**
   Run the application with:
    ```bash
   python main.py
    
Try these commands:

Open apps: open chrome

Generate code: build a calculator

Search the web: search what is python

Built with passion for those who prefer their AI local and their system automated.
This tool can run offline, but it connects to the internet when you need to perform web searches.

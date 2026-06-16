import customtkinter as ctk
import sqlite3
import threading
import requests
import subprocess
import psutil
import pyperclip
import datetime
import os
import pyttsx3
import glob
from duckduckgo_search import DDGS

class ZyliexOS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zyliex OS - System Management")
        self.geometry("950x700")
        
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "English" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        
        self.init_db()
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = ctk.CTkScrollableFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.chat_area = ctk.CTkTextbox(self, width=650, height=500, state="disabled")
        self.chat_area.grid(row=0, column=1, padx=10, pady=10)
        
        self.entry = ctk.CTkEntry(self, width=500, placeholder_text="Enter command...")
        self.entry.grid(row=1, column=1, pady=10)
        
        self.btn_send = ctk.CTkButton(self, text="Execute", command=self.run_process)
        self.btn_send.grid(row=2, column=1, pady=5)
        
        self.refresh_history()

    def init_db(self):
        self.conn = sqlite3.connect("zyliex.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, title TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS messages (chat_id INTEGER, role TEXT, content TEXT)")
        self.conn.commit()

    def refresh_history(self):
        for widget in self.sidebar.winfo_children(): widget.destroy()
        self.cursor.execute("SELECT * FROM chats ORDER BY id DESC")
        for chat in self.cursor.fetchall():
            ctk.CTkButton(self.sidebar, text=chat[1], command=lambda c=chat[0]: self.load_chat(c)).pack(pady=5)

    def load_chat(self, chat_id):
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", "end")
        self.cursor.execute("SELECT role, content FROM messages WHERE chat_id = ?", (chat_id,))
        for msg in self.cursor.fetchall(): self.chat_area.insert("end", f"{msg[0]}: {msg[1]}\n")
        self.chat_area.configure(state="disabled")

    def log_message(self, text):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", text + "\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def vocalize(self, text):
        def run_engine():
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.say(text); engine.runAndWait()
        threading.Thread(target=run_engine, daemon=True).start()

    def find_and_run(self, app_name):
        search_paths = [r"C:\Program Files\*", r"C:\Program Files (x86)\*"]
        for path in search_paths:
            for exe in glob.glob(os.path.join(path, f"**/{app_name}*.exe"), recursive=True):
                subprocess.Popen([exe]); return True
        return False

    def run_process(self):
        cmd = self.entry.get()
        if not cmd: return
        
        # Girişi kilitle
        self.entry.configure(state="disabled")
        self.btn_send.configure(state="disabled")
        
        self.entry.delete(0, 'end')
        self.cursor.execute("INSERT INTO chats (title) VALUES (?)", (cmd[:20],))
        self.conn.commit()
        chat_id = self.cursor.lastrowid
        
        self.log_message(f"User: {cmd}")
        self.log_message("System: Thinking... 💭")
        
        threading.Thread(target=self.execute_logic, args=(cmd, chat_id)).start()

    def execute_logic(self, cmd, chat_id):
        try:
            if "open" in cmd.lower():
                app = cmd.lower().replace("open", "").strip()
                response = f"Launched {app}" if self.find_and_run(app) else f"Could not find {app}"
            elif "build" in cmd.lower() or "create" in cmd.lower():
                prompt = f"Write Python code for: {cmd}. Provide only the clean, functional code."
                res = requests.post("http://localhost:11434/api/generate", json={"model": "llama3", "prompt": prompt, "stream": False}).json()['response']
                code = res.replace("```python", "").replace("```", "").strip()
                with open("output.py", "w", encoding="utf-8") as f: f.write(code)
                subprocess.Popen(["code", "output.py"])
                response = "Script generated."
            elif "status" in cmd.lower():
                response = f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%"
            elif cmd.lower().startswith("note:"):
                with open("notes.txt", "a", encoding="utf-8") as f: f.write(f"{datetime.datetime.now()}: {cmd[5:]}\n")
                response = "Note saved."
            elif any(k in cmd.lower() for k in ["search", "what is"]):
                with DDGS() as ddgs:
                    results = list(ddgs.text(cmd, max_results=1))
                    response = results[0]['body'] if results else "Not found."
            else:
                response = requests.post("http://localhost:11434/api/generate", json={"model": "llama3", "prompt": cmd, "stream": False}).json()['response']

            self.cursor.execute("INSERT INTO messages VALUES (?,?,?)", (chat_id, "System", response))
            self.conn.commit()
            
            # Arayüzü güncelle ve giriş kutusunu aç
            self.after(0, lambda: self.log_message(f"System: {response}"))
            self.after(0, lambda: self.refresh_history())
            self.after(0, lambda: self.entry.configure(state="normal"))
            self.after(0, lambda: self.btn_send.configure(state="normal"))
            
            pyperclip.copy(response)
            self.vocalize(response)
        except Exception as e:
            self.after(0, lambda: self.log_message(f"Error: {str(e)}"))
            self.after(0, lambda: self.entry.configure(state="normal"))
            self.after(0, lambda: self.btn_send.configure(state="normal"))

if __name__ == "__main__":
    app = ZyliexOS()
    app.mainloop()
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import re

SYSTEM_PROMPT = """
You are a chatbot.

IMPORTANT:

The conversation history provided to you is true.

Use the conversation history to answer questions.

If the user asks:
"What is my name?"

Look into the conversation history and answer using the name already provided.

Never say that you cannot access previous conversation.
"""

conversation_history = ""


def send_message():

    global conversation_history

    user_message = entry.get()

    if not user_message.strip():
        return

    chat_area.insert(tk.END, "\n👤 You\n", "user")
    chat_area.insert(tk.END, f"{user_message}\n\n")

    entry.delete(0, tk.END)

    full_prompt = f"""
{SYSTEM_PROMPT}

Conversation so far:

{conversation_history}

User: {user_message}
Assistant:
"""

    result = subprocess.run(
        ["ollama", "run", "gemma3:1b", full_prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    response = result.stdout.strip()

    response = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', response)
    response = re.sub(r'\[[0-9;]*[A-Za-z]', '', response)
    response = re.sub(r'\[[0-9]+[A-Z]', '', response)

    chat_area.insert(tk.END, "══════════════════════════════\n")
    chat_area.insert(tk.END, "🤖 Assistant\n", "assistant")
    chat_area.insert(tk.END, f"\n{response}\n\n")   

    conversation_history += f"\nUser: {user_message}\nAssistant: {response}"

    if len(conversation_history) > 3000:
        conversation_history = conversation_history[-3000:]

    chat_area.see(tk.END)


root = tk.Tk()
root.title("🤖 AI Assistant")

root.geometry("900x700")
root.configure(bg="#1E1E1E")

root.resizable(True, True)
root.minsize(900, 600)

title_label = tk.Label(
    root,
    text="🤖 AI Assistant",
    font=("Segoe UI", 22, "bold"),
    bg="#1E1E1E",
    fg="white"
)

title_label.pack(pady=(15, 5))

subtitle_label = tk.Label(
    root,
    text="Powered by Ollama + Gemma3",
    font=("Segoe UI", 10),
    bg="#1E1E1E",
    fg="lightgray"
)

subtitle_label.pack()

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    bg="#252526",
    fg="white",
    insertbackground="white",
    font=("Segoe UI", 12),
    bd=0
)
chat_area.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

chat_area.tag_config(
    "user",
    foreground="#4FC3F7",
    font=("Segoe UI", 12, "bold")
)

chat_area.tag_config(
    "assistant",
    foreground="#7CFC00",
    font=("Segoe UI", 12)
)

entry = tk.Entry(
    root,
    font=("Segoe UI", 12),
    bg="#3C3C3C",
    fg="white",
    insertbackground="white",
    bd=0
)
entry.pack(padx=10, pady=5, fill=tk.X)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    root,
    text="🚀 Send",
    command=send_message,
    font=("Segoe UI", 11, "bold"),
    bg="#007ACC",
    fg="white",
    bd=0,
    padx=20,
    pady=8
)
send_button.pack(pady=5)

root.mainloop()
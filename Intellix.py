import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai

# === Configure Gemini Model ===
API_KEY = "AIzaSyApDScdZNxCJL-P4d2naOt6dzJJvDrZMOk"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# === Send message to Gemini ===
def send_to_gemini():
    user_input = user_entry.get().strip()
    if user_input == "":
        return

    if user_input.lower() == "exit":
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, "👋 Exiting...\n", "gemini")
        chat_display.configure(state='disabled')
        chat_display.update()
        root.after(500, root.destroy)  # Safe exit with slight delay
        return

    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    chat_display.configure(state='disabled')
    chat_display.yview(tk.END)
    user_entry.delete(0, tk.END)

    try:
        response = chat.send_message(user_input)
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, f"Gemini: {response.text}\n\n", "gemini")
        chat_display.configure(state='disabled')
        chat_display.yview(tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI Setup ===
root = tk.Tk()
root.title("Intellix")
root.geometry("600x650")
root.configure(bg="#1e1e2f")

# === Set custom icon (must be .ico and in same folder) ===
try:
    root.iconbitmap("ai.ico")
except Exception as e:
    print("Icon error:", e)

# === Styling ===
style_font = ("Segoe UI", 11)
header_font = ("Segoe UI", 16, "bold")

# === Header ===
header = tk.Label(root, text="💬 Chat with Intellix", font=header_font, bg="#1e1e2f", fg="#00d4ff", pady=10)
header.pack()

# === Chat Display Area ===
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=style_font, bg="#2e2e3e", fg="white", bd=0, padx=10, pady=10)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.tag_config("user", foreground="#00ffae")
chat_display.tag_config("gemini", foreground="#00d4ff")
chat_display.configure(state='disabled')

# === Input Field and Button ===
bottom_frame = tk.Frame(root, bg="#1e1e2f")
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

user_entry = tk.Entry(bottom_frame, font=style_font, bg="#2e2e3e", fg="white", insertbackground="white", relief="flat")
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
user_entry.bind("<Return>", lambda event: send_to_gemini())

send_button = tk.Button(bottom_frame, text="➤ Send", font=("Segoe UI", 10, "bold"), bg="#00d4ff", fg="black", padx=20, pady=6, relief="flat", activebackground="#00aacc", activeforeground="white", command=send_to_gemini)
send_button.pack(side=tk.RIGHT)

# === Start GUI ===
root.mainloop()

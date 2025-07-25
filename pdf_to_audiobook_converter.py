import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pyttsx3
from gtts import gTTS
from playsound import playsound
import os


# 1. Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        text = page.get_text()
        if text.strip():
            full_text += text + "\n"
    return full_text.strip()


# 2. Text-to-speech using pyttsx3
def text_to_speech_pyttsx3(text, rate=150, volume=1.0):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# 3. Export to MP3 using gTTS
def export_to_mp3(text, filename="output.mp3"):
    try:
        tts = gTTS(text)
        tts.save(filename)
        messagebox.showinfo("Exported", f"Saved as {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))


# 4. File picker
def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        try:
            text = extract_text_from_pdf(file_path)
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read PDF: {e}")


# 5. Play Audio with speed/volume controls
def play_audio():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No text to read.")
        return
    rate = int(speed_slider.get())
    volume = float(volume_slider.get())
    text_to_speech_pyttsx3(text, rate, volume)


# 6. Export to MP3
def export_audio():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No text to export.")
        return
    export_to_mp3(text)


# ---- GUI Setup ----
root = tk.Tk()
root.title("PDF to Audiobook Converter")
root.geometry("700x600")
root.resizable(False, False)

tk.Button(root, text="📂 Load PDF", font=("Arial", 12), command=open_pdf).pack(pady=10)

text_box = tk.Text(root, wrap="word", height=20, width=80, font=("Arial", 10))
text_box.pack(pady=10)


# Controls
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Label(control_frame, text="Speed:", font=("Arial", 10)).grid(row=0, column=0)
speed_slider = tk.Scale(control_frame, from_=100, to=300, orient="horizontal")
speed_slider.set(150)
speed_slider.grid(row=0, column=1, padx=10)

tk.Label(control_frame, text="Volume:", font=("Arial", 10)).grid(row=0, column=2)
volume_slider = tk.Scale(control_frame, from_=0.0, to=1.0, resolution=0.1, orient="horizontal")
volume_slider.set(1.0)
volume_slider.grid(row=0, column=3, padx=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="🔊 Play Audio", font=("Arial", 12), command=play_audio).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="💾 Export MP3", font=("Arial", 12), command=export_audio).grid(row=0, column=1, padx=10)

root.mainloop()

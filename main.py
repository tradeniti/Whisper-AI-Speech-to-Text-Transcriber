import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import whisper
import os
import tempfile
import wave
import subprocess

# Graceful handling for pyaudio (Mic support)
try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False

# Graceful handling for gTTS (Text-to-Speech)
try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

class WhisperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper AI Speech to text Transcriber")
        self.root.geometry("850x700")

        # --- Dark Mode Theme Colors ---
        self.bg_color = "#1E1E1E"
        self.fg_color = "#FFFFFF"
        self.accent_bg = "#2D2D30"
        self.btn_green = "#43A047"
        self.btn_orange = "#F57C00"
        self.btn_blue = "#1E88E5"
        self.btn_gray = "#546E7A"
        self.btn_purple = "#8E24AA" # Read button color

        self.root.configure(bg=self.bg_color)

        # Font settings for Hindi/Marathi support and zooming
        self.font_family = "Arial"
        self.font_size = 14

        self.model = None
        self.is_recording = False
        self.record_seconds = 0

        # TTS variables
        self.is_reading = False
        self.ffplay_process = None

        # Set Custom Application Icon (Optional)
        try:
            icon_img = tk.PhotoImage(file="mic.png")
            self.root.iconphoto(False, icon_img)
        except Exception:
            pass

        # --- UI Elements ---

        # Top Frame for Action Buttons
        self.top_frame = tk.Frame(root, bg=self.bg_color)
        self.top_frame.pack(pady=15)

        self.select_btn = tk.Button(
            self.top_frame, text="🎵 Select Audio File", command=self.start_file_transcription,
            font=("Segoe UI", 11, "bold"), bg=self.btn_green, fg=self.fg_color,
            activebackground="#2E7D32", activeforeground=self.fg_color,
            relief=tk.FLAT, cursor="hand2", padx=15, pady=8
        )
        self.select_btn.pack(side=tk.LEFT, padx=10)

        self.record_btn = tk.Button(
            self.top_frame, text="🎤 Start Recording", command=self.toggle_recording,
            font=("Segoe UI", 11, "bold"), bg=self.btn_orange, fg=self.fg_color,
            activebackground="#EF6C00", activeforeground=self.fg_color,
            relief=tk.FLAT, cursor="hand2", padx=15, pady=8
        )
        self.record_btn.pack(side=tk.LEFT, padx=10)

        # Recording Timer Label (New Timer Feature)
        self.timer_label = tk.Label(
            self.top_frame, text="00:00", font=("Consolas", 14, "bold"),
            bg=self.bg_color, fg=self.btn_orange
        )
        self.timer_label.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            root, text="Status: Ready. Choose a file or start recording.",
            font=("Segoe UI", 10, "italic"), bg=self.bg_color, fg="#B0BEC5"
        )
        self.status_label.pack(pady=5)

        # Header Frame for Label + Zoom Buttons
        self.text_header_frame = tk.Frame(root, bg=self.bg_color)
        self.text_header_frame.pack(fill=tk.X, padx=20, pady=(10,0))

        self.text_label = tk.Label(
            self.text_header_frame, text="Editable Transcription Result:",
            font=("Segoe UI", 10, "bold"), bg=self.bg_color, fg=self.fg_color
        )
        self.text_label.pack(side=tk.LEFT)

        # Zoom In/Out Buttons
        self.zoom_in_btn = tk.Button(
            self.text_header_frame, text="A +", command=self.zoom_in,
            font=("Segoe UI", 9, "bold"), bg=self.accent_bg, fg=self.fg_color,
            relief=tk.FLAT, cursor="hand2", padx=8, pady=2
        )
        self.zoom_in_btn.pack(side=tk.RIGHT, padx=5)

        self.zoom_out_btn = tk.Button(
            self.text_header_frame, text="A -", command=self.zoom_out,
            font=("Segoe UI", 9, "bold"), bg=self.accent_bg, fg=self.fg_color,
            relief=tk.FLAT, cursor="hand2", padx=8, pady=2
        )
        self.zoom_out_btn.pack(side=tk.RIGHT, padx=5)

        # Text Area (Resizable)
        self.text_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=80, height=15,
            font=(self.font_family, self.font_size), bd=1, padx=10, pady=10,
            bg=self.accent_bg, fg=self.fg_color, insertbackground=self.fg_color
        )
        self.text_area.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # Bottom Frame
        self.bottom_frame = tk.Frame(root, bg=self.bg_color)
        self.bottom_frame.pack(pady=15)

        self.save_btn = tk.Button(
            self.bottom_frame, text="💾 Save", command=self.save_file,
            font=("Segoe UI", 11, "bold"), bg=self.btn_blue, fg=self.fg_color,
            relief=tk.FLAT, cursor="hand2", state=tk.DISABLED, padx=12, pady=8
        )
        self.save_btn.pack(side=tk.LEFT, padx=8)

        self.copy_btn = tk.Button(
            self.bottom_frame, text="📋 Copy", command=self.copy_to_clipboard,
            font=("Segoe UI", 11, "bold"), bg=self.btn_gray, fg=self.fg_color,
            relief=tk.FLAT, cursor="hand2", state=tk.DISABLED, padx=12, pady=8
        )
        self.copy_btn.pack(side=tk.LEFT, padx=8)

        self.clear_btn = tk.Button(
            self.bottom_frame, text="🗑️ Clear", command=self.clear_text,
            font=("Segoe UI", 11, "bold"), bg="#D32F2F", fg=self.fg_color,
            relief=tk.FLAT, cursor="hand2", state=tk.DISABLED, padx=12, pady=8
        )
        self.clear_btn.pack(side=tk.LEFT, padx=8)

        # Read Aloud Button
        self.read_btn = tk.Button(
            self.bottom_frame, text="🔊 Read Aloud", command=self.toggle_reading,
            font=("Segoe UI", 11, "bold"), bg=self.btn_purple, fg=self.fg_color,
            relief=tk.FLAT, cursor="hand2", state=tk.DISABLED, padx=12, pady=8
        )
        self.read_btn.pack(side=tk.LEFT, padx=8)

    # --- Feature Methods ---

    def zoom_in(self):
        if self.font_size < 30:
            self.font_size += 2
            self.text_area.config(font=(self.font_family, self.font_size))

    def zoom_out(self):
        if self.font_size > 8:
            self.font_size -= 2
            self.text_area.config(font=(self.font_family, self.font_size))

    def update_timer(self):
        if self.is_recording:
            mins, secs = divmod(self.record_seconds, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}", fg="#FF5252")
            self.record_seconds += 1
            self.root.after(1000, self.update_timer)

    def start_file_transcription(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.ogg")])
        if not file_path:
            return
        self.prepare_ui_for_processing()
        threading.Thread(target=self.process_audio, args=(file_path, False), daemon=True).start()

    def toggle_recording(self):
        if not HAS_PYAUDIO:
            messagebox.showwarning("Missing Dependency", "PyAudio is not installed.")
            return

        if not self.is_recording:
            self.is_recording = True
            self.record_seconds = 0
            self.record_btn.config(text="🛑 Stop Recording", bg="#D32F2F")
            self.select_btn.config(state=tk.DISABLED)
            self.update_timer() # Start the timer loop
            threading.Thread(target=self.record_audio_thread, daemon=True).start()
        else:
            self.is_recording = False
            self.record_btn.config(text="🎤 Start Recording", bg=self.btn_orange)
            self.timer_label.config(text="00:00", fg=self.btn_orange)

    def record_audio_thread(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []

        self.root.after(0, lambda: self.status_label.config(text="Status: Recording... Speak into your mic 🎙️", fg="#FF5252"))

        while self.is_recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "whisper_live_record.wav")

        wf = wave.open(temp_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.prepare_ui_for_processing()
        self.process_audio(temp_file, is_temp_file=True)

    def prepare_ui_for_processing(self):
        self.status_label.config(text="Status: AI is processing the audio... Please wait ⏳", fg="#64B5F6")
        self.select_btn.config(state=tk.DISABLED)
        self.record_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.read_btn.config(state=tk.DISABLED)

    def process_audio(self, file_path, is_temp_file=False):
        try:
            if self.model is None:
                self.root.after(0, lambda: self.status_label.config(text="Status: Loading AI model into memory... ⏳", fg="#FFCA28"))
                self.model = whisper.load_model("base")

            self.root.after(0, lambda: self.status_label.config(text="Status: Transcribing audio to text... 🎧", fg="#64B5F6"))

            result = self.model.transcribe(file_path, fp16=False)
            transcribed_text = result["text"]

            self.root.after(0, self.update_ui_success, transcribed_text)

        except Exception as e:
            self.root.after(0, self.update_ui_error, str(e))

        finally:
            if is_temp_file and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

    def update_ui_success(self, text):
        current_text = self.text_area.get(1.0, tk.END).strip()
        if current_text:
            self.text_area.insert(tk.END, "\n\n" + text.strip())
        else:
            self.text_area.insert(tk.END, text.strip())

        self.status_label.config(text="Status: Transcription completed successfully! ✅", fg="#81C784")
        self.select_btn.config(state=tk.NORMAL)
        self.record_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.copy_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)
        self.read_btn.config(state=tk.NORMAL)

    def update_ui_error(self, error_msg):
        messagebox.showerror("Processing Error", f"An error occurred:\n{error_msg}")
        self.status_label.config(text="Status: Error during processing ❌", fg="#E57373")
        self.select_btn.config(state=tk.NORMAL)
        self.record_btn.config(state=tk.NORMAL)

    # --- Read Aloud Feature ---

    def toggle_reading(self):
        if not HAS_GTTS:
            messagebox.showwarning("Missing Dependency", "gTTS is not installed.\nPlease run in terminal:\npip install gTTS")
            return

        if not self.is_reading:
            self.is_reading = True
            self.read_btn.config(text="⏹️ Stop Reading", bg="#D32F2F")
            threading.Thread(target=self.read_text_thread, daemon=True).start()
        else:
            self.is_reading = False
            if self.ffplay_process:
                self.ffplay_process.terminate()

    def highlight_paragraph(self, line_num):
        start_idx = f"{line_num}.0"
        end_idx = f"{line_num}.end"
        self.text_area.tag_add("highlight", start_idx, end_idx)
        self.text_area.tag_config("highlight", background="#000000", foreground="#FFFFFF", borderwidth=1, relief="solid")
        self.text_area.see(start_idx) # Auto-scroll to the reading line

    def remove_highlight(self, line_num):
        start_idx = f"{line_num}.0"
        end_idx = f"{line_num}.end"
        self.text_area.tag_remove("highlight", start_idx, end_idx)

    def read_text_thread(self):
        # Calculate total lines in the text area
        total_lines = int(self.text_area.index('end-1c').split('.')[0])

        self.root.after(0, lambda: self.status_label.config(text="Status: Reading text aloud... 🔊", fg="#E040FB"))

        for i in range(1, total_lines + 1):
            if not self.is_reading:
                break

            line_text = self.text_area.get(f"{i}.0", f"{i}.end").strip()
            if not line_text:
                continue

            # 1. Highlight the paragraph
            self.root.after(0, self.highlight_paragraph, i)

            temp_file = None
            try:
                # 2. Generate Audio
                tts = gTTS(text=line_text, lang='hi')
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, f"whisper_tts_{i}.mp3")
                tts.save(temp_file)

                # 3. Play Audio using ffplay
                self.ffplay_process = subprocess.Popen(
                    ["ffplay", "-nodisp", "-autoexit", temp_file],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                self.ffplay_process.wait() # Wait until paragraph finishes reading

            except Exception as e:
                print("TTS Error:", e)
            finally:
                # 4. PERMANENTLY DELETE TEMP AUDIO FILE
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except Exception:
                        pass

            # 5. Remove Highlight
            self.root.after(0, self.remove_highlight, i)

        # Reset button when done or stopped
        self.is_reading = False
        self.root.after(0, lambda: self.read_btn.config(text="🔊 Read Aloud", bg=self.btn_purple))
        self.root.after(0, lambda: self.status_label.config(text="Status: Reading completed. ✅", fg="#81C784"))

    # --- Utility Methods ---

    def copy_to_clipboard(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            self.status_label.config(text="Status: Text copied to clipboard! 📋", fg="#81C784")

    def save_file(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Success", f"File saved successfully at:\n{save_path}")

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.save_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.read_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Text cleared. Ready for next.", fg="#B0BEC5")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhisperApp(root)
    root.mainloop()

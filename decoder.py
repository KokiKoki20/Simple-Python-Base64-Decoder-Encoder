import customtkinter as ctk
import base64
import os
import sys
import pyperclip

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DecoderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Base64 Tool")
        self.geometry("450x550")
        self.mode = "Decode"

        # Icon Setup
        icon_path = resource_path("myicon.ico")
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))

        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.label = ctk.CTkLabel(self, text="Base64 Decoder", font=("Roboto", 24, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # Input Section
        self.input_label = ctk.CTkLabel(self, text="Paste Encoded Text:", font=("Roboto", 12))
        self.input_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.input_text = ctk.CTkTextbox(self, height=100, corner_radius=15)
        self.input_text.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Action Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=3)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.action_btn = ctk.CTkButton(self.button_frame, text="Decode String", command=self.process_logic, 
                                        corner_radius=10, fg_color="#6366f1", hover_color="#4f46e5", font=("Roboto", 14, "bold"))
        self.action_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.reverse_btn = ctk.CTkButton(self.button_frame, text="⇌", width=40, command=self.toggle_mode, 
                                         corner_radius=10, fg_color="#3b3b3b", hover_color="#4a4a4a", font=("Roboto", 18, "bold"))
        self.reverse_btn.grid(row=0, column=1, sticky="ew")

        # Output Section
        self.output_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.output_header_frame.grid(row=4, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.output_header_frame.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self.output_header_frame, text="Decoded Result:", font=("Roboto", 12))
        self.output_label.grid(row=0, column=0, sticky="w")

        self.copy_btn = ctk.CTkButton(self.output_header_frame, text="Copy Result", width=80, height=24, 
                                      command=self.copy_to_clipboard, corner_radius=8, fg_color="#444", font=("Roboto", 11))
        self.copy_btn.grid(row=0, column=1, sticky="e")
        
        # Initialize Output Box as DISABLED (Read-Only)
        self.output_text = ctk.CTkTextbox(self, height=100, corner_radius=15, fg_color="#2b2b2b", state="disabled")
        self.output_text.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

    def toggle_mode(self):
        if self.mode == "Decode":
            self.mode = "Encode"
            self.label.configure(text="Base64 Encoder")
            self.input_label.configure(text="Paste Plain Text:")
            self.output_label.configure(text="Encoded Result:")
            self.action_btn.configure(text="Encode String", fg_color="#10b981", hover_color="#059669")
        else:
            self.mode = "Decode"
            self.label.configure(text="Base64 Decoder")
            self.input_label.configure(text="Paste Encoded Text:")
            self.output_label.configure(text="Decoded Result:")
            self.action_btn.configure(text="Decode String", fg_color="#6366f1", hover_color="#4f46e5")
        self.clear_fields()

    def clear_fields(self):
        self.input_text.delete("0.0", "end")
        
        # Temporarily unlock to clear
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.configure(state="disabled") # Lock it back
        
        self.copy_btn.configure(text="Copy Result", fg_color="#444")

    def copy_to_clipboard(self):
        result = self.output_text.get("1.0", "end-1c").strip()
        if result:
            pyperclip.copy(result)
            self.copy_btn.configure(text="Copied!", fg_color="#2e7d32")
            self.after(1500, lambda: self.copy_btn.configure(text="Copy Result", fg_color="#444"))

    def process_logic(self):
        data = self.input_text.get("1.0", "end-1c").strip()
        if not data: return
        
        try:
            if self.mode == "Decode":
                result = base64.b64decode(data).decode("utf-8").strip()
            else:
                result = base64.b64encode(data.encode("utf-8")).decode("utf-8").strip()
            
            # Unlock -> Write -> Lock
            self.output_text.configure(state="normal")
            self.output_text.delete("0.0", "end")
            self.output_text.insert("0.0", result)
            self.output_text.configure(state="disabled")
            
        except Exception:
            self.output_text.configure(state="normal")
            self.output_text.delete("0.0", "end")
            self.output_text.insert("0.0", "Error: Invalid input")
            self.output_text.configure(state="disabled")

if __name__ == "__main__":
    app = DecoderApp()
    app.mainloop()
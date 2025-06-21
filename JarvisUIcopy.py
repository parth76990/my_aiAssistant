import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SmartAssistantUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.title("Smart Assistant")
        self.resizable(False, False)

        # Load and place background image using a CTkLabel
        bg_image = Image.open("C:\\Users\\tech0\\Downloads\\Jun 21, 2025, 10_10_43 AM.png").resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="", bg_color="transparent")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create widgets on top of background
        self.create_widgets()

    def create_widgets(self):
        # Labels
        ctk.CTkLabel(self, text="Hi, Parth", font=("Segoe UI", 40, "bold"), text_color="white").place(relx=0.08, rely=0.12)
        ctk.CTkLabel(self, text="How can I help you?", font=("Segoe UI", 34), text_color="white").place(relx=0.08, rely=0.20)
        ctk.CTkLabel(self, text="Your smart assistant is ready", font=("Segoe UI", 20), text_color="lightgray").place(relx=0.08, rely=0.28)

        # Buttons
        button_font = ("Segoe UI", 16, "bold")
        btn_fg = "#007ca1"

        ctk.CTkButton(self, text="🖼  Generate image", font=button_font, corner_radius=30, fg_color=btn_fg).place(relx=0.08, rely=0.4)
        ctk.CTkButton(self, text="🌙  Goodnight stories", font=button_font, corner_radius=30, fg_color=btn_fg).place(relx=0.32, rely=0.4)
        ctk.CTkButton(self, text="❌  Inspiring novels", font=button_font, corner_radius=30, fg_color=btn_fg).place(relx=0.56, rely=0.4)
        ctk.CTkButton(self, text="🎵  Play music", font=button_font, corner_radius=30, fg_color=btn_fg).place(relx=0.08, rely=0.5)

        # Mic button
        mic_btn = ctk.CTkButton(self, width=60, height=60, text="", fg_color="#007ca1", corner_radius=100)
        mic_btn.place(relx=0.5, rely=0.65, anchor="center")
        ctk.CTkLabel(mic_btn, text="🎤", font=("Segoe UI", 24, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Input field
        ctk.CTkEntry(self, placeholder_text="Type a message...", width=1000, height=40, corner_radius=20, font=("Segoe UI", 14)).place(relx=0.5, rely=0.85, anchor="center")

if __name__ == "__main__":
    app = SmartAssistantUI()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, Scrollbar
from dotenv import load_dotenv
import os
from chatModels.claude import *
import threading
from tkinter import PhotoImage
import system_web
import system_desktop
import system_file
from PIL import Image, ImageTk, ImageDraw
import speech_text as st
import sys
import time
from pathlib import Path
from datetime import datetime
import queue
from voice_models.eleven_labs_model import *

load_dotenv()

APP_TITLE = "3D Assistant"
AI_METAVERSE_PAGE = "AI Metaverse"
CHATBOT_PAGE = "Chatbot"
CLAUDE_MODEL_PAGE = "Claude Model"
API_PAGE = "API Page"


# --------------------- SET API KEYS AREA ------------------------
try:
    claude_api_key =  os.getenv("CLAUDE_API_KEY")
    Set_Claude_Api_Key(claude_api_key)

    elevenLabs_api_key =  os.getenv("ELEVEN_LABS_API_KEY")
    print(elevenLabs_api_key)
    Set_Eleven_API_KEY(elevenLabs_api_key)
except:
    print("API Keys are not init")
    

class Message:

    def __init__(self, chatter, msg) -> None:
        self.sender = chatter
        self.message = msg


class ChatApp:


    def __init__(self, root, interface, path):
        self.root = root
        self.root.title(APP_TITLE)
        self.voice_text_interface = interface
        self.abspath = path

        # Define colors
        self.bg_color = "#1b1f23"
        self.text_color = "#e1e4e8"
        self.entry_bg_color = "#2d333b"
        self.button_bg_color = "#21262d"
        self.button_text_color = "#e1e4e8"
        self.border_color = "#636e7b"
        self.accent_color = "#58a6ff"
        self.client_msg_color = "#373e47"
        self.bot_msg_color = "#2d333b"
        self.darkgrey = "#001F3F"
        self.button_bg_color = "#21262d"  # Example background color
        self.highlight_color = "#4CAF50"  # Highlight color for the selected radio button
        self.bright_blue = "#1E90FF"
        self.ai_metaverse_purple = "#8A2BE2"
        self.purple_dark_shade = "#7A22D0"
        self.bg_light_shade = "#2d333b"
        self.dark_blue = "#0D1117"

        self.root.geometry("800x600")
        root.configure(bg=self.bg_color)

        # root.columnconfigure(0, weight=1)
        # root.columnconfigure(1, weight=6)
        # root.columnconfigure(2, weight=1)
        # root.rowconfigure(0, weight=1)
        # root.rowconfigure(1, weight=7)
        # root.rowconfigure(2, weight=2)

        self.image_paths = {
            "send": Path(str(self.abspath / "Images/send.png")),
            "voice": Path(str(self.abspath / "Images/voice.png")),
            "upload": Path(str(self.abspath / "Images/upload.png")),
            "lead_icon": Path(str(self.abspath/ "Images/m.png")),
            "anime": Path(str(self.abspath/ "Images/anime.jpg")),
            "ai": Path(str(self.abspath/ "Images/ai.png")),
            "ai1": Path(str(self.abspath/ "Images/ai1.png")),
            "hologram": Path(str(self.abspath/ "Images/hologram.png")),
            "assistant": Path(str(self.abspath/ "Images/assistant1.jpeg")),
            "info": Path(str(self.abspath/ "Images/info.png")),
            "settings": Path(str(self.abspath/ "Images/setting.png")),
            "metaverse_bg": Path(str(self.abspath/ "Images/metaverse_bg2.jpg"))
        }

        self.hologram_msgs = ['こんにちは, nice to have you here.',
                              'Experience 3D METAVERSE',
                              'Idea tunred into reality'
                              ]

        self.root.wm_attributes('-alpha', 0.9)  # Sets the window transparency to 70%
        
        # Circular progress bar parameters
        self.angle = 0  # Start angle
        self.progress = None  # Placeholder for the arc object

        self.file_content_explain = ""
        # arr for holding chat (text) msgs
        self.msgs = []
        self.msgs_index = 0

        self.Communication = "Text"
        self.Task = "AI Bot"

        self.show_ai_metaverse_page()
        # self.show_chat_page()


    def read_env_file(self, file_path):
        api_keys = {}
        
        with open(file_path, 'r') as file:
            for line in file:
                # Remove any leading/trailing whitespace or newlines
                line = line.strip()
                if line:  # Check if the line is not empty
                    # Split the line into key and value
                    key, value = line.split('=', 1)
                    api_keys[key] = value
        
        return api_keys

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_image_w_h(self,img, width, height):

        self.metaverse_bg_image = Image.open(img)
        self.metaverse_bg_image = self.metaverse_bg_image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(self.metaverse_bg_image)


    def wrap_text(self, text, max_width):
        # Create a temporary Tkinter Text widget to measure text width
        temp_text = tk.Text(self.root, wrap='word', font=('Verdana', 16))
        temp_text.insert(tk.END, text)
        temp_text.update_idletasks()

        # Get the width of the text widget in pixels
        text_width = temp_text.winfo_width()

        # Wrap the text manually
        lines = []
        current_line = ""
        for word in text.split():
            # Append the word to the current line
            test_line = f"{current_line} {word}".strip()
            
            # Update text widget with test line
            temp_text.delete(1.0, tk.END)
            temp_text.insert(tk.END, test_line)
            temp_text.update_idletasks()
            
            # Check if the line exceeds max width
            if temp_text.winfo_width() > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line)
        wrapped_text = "\n".join(lines)
        return wrapped_text
    
    def show_ai_metaverse_page(self):
        self.clear_screen()

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Create a Canvas widget that fills the screen
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)


        # Load and resize the image to fit the screen
        self.photo_image = self.create_image_w_h(self.image_paths["metaverse_bg"], screen_width, screen_height)

        # Display the image on the Canvas
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo_image)

        self.window_round = self.create_rounded_rectangle(self.canvas, 300, 200, 1700, 1000, radius=40, fill=self.dark_blue, outline=self.bright_blue)

        padding_y = 50  # Padding from the top edge
        self.canvas.create_text(screen_width // 2, padding_y, 
                               text="WELCOME TO THE METAVERSE", 
                               fill=self.bright_blue, font=('Helvetica', 28, 'bold'), anchor='n')
        
        
        self.canvas.create_text(screen_width // 2 - 250, (screen_height // 2) - 320, 
                               text="FIND YOUR INNER GATE", 
                               fill="white", font=('Verdana', 30, 'bold'), anchor='n')
        
        # Description text
        description = ("Welcome to a world where you can experience everything. "
                       "A place beyond imagination where dreams manifest into reality. "
                       "Designed by the world's greatest programmers.")
        
        # Wrap the text
        wrapped_text = self.wrap_text(description, screen_width - 40)  # 40 pixels padding on each side
        
        # Display wrapped text on the canvas
        self.canvas.create_text(screen_width // 2, (screen_height // 2) - 150,
                               text=wrapped_text,
                               fill=self.bright_blue, font=('Verdana', 16), anchor='n', width=screen_width - 800, justify="center")
        
        Chat_Page_Btn = tk.Button(root, text="3D Assistant", command=lambda: self.nav_to_page("claude"), bg=self.purple_dark_shade, fg="white", font=('Verdana', 24))
        self.canvas.create_window(screen_width // 2, screen_height // 2 + 50, anchor='center', window=Chat_Page_Btn, width=600, height=80)

        Settings_btn = tk.Button(root, text="Settings", command=lambda: self.settings_page(), bg=self.purple_dark_shade, fg="white", font=('Verdana', 24))
        self.canvas.create_window(screen_width // 2, screen_height // 2 + 200, anchor='center', window=Settings_btn, width=600, height=80)

        
        # ---------------------------------------------------------

        # w = self.root.winfo_screenwidth()
        # h = self.root.winfo_screenheight()
        # self.main_page_bg_image = self.create_image_w_h(w, h)

        # self.metaverse_bg_label = tk.Label(self.root, image=self.main_page_bg_image, bg=self.bg_color)
        # self.metaverse_bg_label.place(relwidth=1, relheight=1)

        # # Modern Header Frame anchored at the top
        # self.header_frame = tk.Frame(self.root, bg="black")
        # self.header_frame.pack(side='top', fill='x')
        
        # # Header Title Label
        # self.title_label = tk.Label(
        #     self.header_frame,
        #     text="Welcome to the AI Metaverse!",
        #     font=('Verdana', 24, 'bold'),
        #     fg=self.bright_blue,
        #     bg="black",
        #     pady=20  # Adjusts vertical padding
        # )
        # self.title_label.pack()


        # self.ai_metaverse_frame_header = tk.Frame(self.metaverse_bg_label, bg=self.bg_color)
        # self.ai_metaverse_frame_header.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # self.title_label = tk.Label(self.ai_metaverse_frame_header, text="Welcome to the AI Metaverse!",
        #                             font=('Verdana', 24, 'bold'), fg=self.bright_blue, bg=self.bg_color, pady=20)
        # self.title_label.pack(fill=tk.BOTH, pady=10)


        # self.ai_metaverse_frame = tk.Frame(self.root, bg=self.bg_color)
        # self.ai_metaverse_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # self.chatbot_frame = tk.Frame(self.ai_metaverse_frame, bg=self.ai_metaverse_purple)
        # self.chatbot_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # # Upper Frame with Two Labels
        # self.LeadWrapperFrame = tk.Frame(self.chatbot_frame, bg=self.ai_metaverse_purple)
        # self.LeadWrapperFrame.pack(side=tk.TOP, padx=10, fill=tk.X, expand=True)

        # self.chatbot_label = tk.Label(self.LeadWrapperFrame, text="FIND YOUR INNER",
        #                               font=('Verdana', 26, 'bold'), fg="white", bg=self.ai_metaverse_purple, pady=10)
        # self.chatbot_label.pack(side=tk.LEFT)

        # self.chatbot_label1 = tk.Label(self.LeadWrapperFrame, text="GATE",
        #                                font=('Verdana', 30, 'bold'), fg="black", bg=self.ai_metaverse_purple, pady=10)
        # self.chatbot_label1.pack(side=tk.LEFT)

        


        # self.select_chatbot_btn = tk.Button(self.ai_metaverse_frame, text="EXPERIENCE 3D COMPANION", bg=self.purple_dark_shade, fg=self.bg_color,
        #                                     highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 18),
        #                                     relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
        #                                     command=lambda: self.nav_to_page("claude"))
        # self.select_chatbot_btn.pack(fill=tk.X, pady=20, expand=True, padx=10)


        # New Frame 

        # self.SettingsFrame = tk.Frame(self.root, bg=self.bg_color)
        # self.SettingsFrame.pack(padx=20, pady=20, fill="both", expand=True)

        # self.imageSettings = self.create_image(self.image_paths["settings"], 150)  # Replace with your image file path

        # # Create the square button with image
        # self.setting_Btn = tk.Button(self.SettingsFrame, image=self.imageSettings, bg=self.bg_color, fg=self.bg_color,
        #                                 highlightbackground=self.border_color, highlightthickness=2,
        #                                 relief=tk.FLAT, activebackground=self.button_bg_color,
        #                                 activeforeground=self.button_text_color, command=lambda: self.settings_page(),
        #                                 width=200, height=200)  # Width and height set to make the button square
        # self.setting_Btn.pack(side=tk.LEFT,padx=5, pady=10)

        # self.select_claude_btn = tk.Button(self.ai_metaverse_frame, text="Select Claude Model", bg=self.accent_color, fg=self.bg_color,
        #                                    highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 12, 'bold'),
        #                                    relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
        #                                    command=lambda: self.nav_to_page("claude"))
        # self.select_claude_btn.pack(fill=tk.X, pady=10)

    def settings_page(self):
        self.clear_screen()


        # Frame in center 
        self.SettingsConfigFrame = tk.Frame(self.root, bg=self.bg_color)
        self.SettingsConfigFrame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.title_label = tk.Label(self.SettingsConfigFrame, text="API Keys Configuration",
                                    font=('Verdana', 24, 'bold'), fg=self.bright_blue, bg=self.bg_color, pady=20)
        self.title_label.pack(fill=tk.BOTH, pady=10)
        

        self.title_label = tk.Label(self.SettingsConfigFrame, text="GPT API Key",
                                    font=('Verdana', 17, 'bold'), fg=self.bright_blue, bg=self.bg_color, pady=20)
        self.title_label.pack(fill=tk.BOTH, pady=10)

        self.MsgBoxContainer = tk.Frame(self.SettingsConfigFrame, bg="white", padx=2, pady=2)
        self.MsgBoxContainer.pack(fill=tk.X,padx=5, pady=10, expand=True)

        self.message_entry_gpt = tk.Entry(self.MsgBoxContainer, bg=self.entry_bg_color, fg=self.text_color,
                                      insertbackground=self.text_color, font=('Verdana', 15), relief=tk.FLAT,
                                      borderwidth=2, highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.message_entry_gpt.pack(fill=tk.X, expand=True, ipady= 12, ipadx=12)

        self.title_label = tk.Label(self.SettingsConfigFrame, text="CLaude API Key",
                                    font=('Verdana', 17, 'bold'), fg=self.bright_blue, bg=self.bg_color, pady=20)
        self.title_label.pack(fill=tk.BOTH, pady=10)

        self.MsgBoxContainer = tk.Frame(self.SettingsConfigFrame, bg="white", padx=2, pady=2)
        self.MsgBoxContainer.pack(fill=tk.X,padx=5, pady=10, expand=True)

        self.message_entry_claude = tk.Entry(self.MsgBoxContainer, bg=self.entry_bg_color, fg=self.text_color,
                                      insertbackground=self.text_color, font=('Verdana', 15), relief=tk.FLAT,
                                      borderwidth=2, highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.message_entry_claude.pack( fill=tk.X, expand=True, ipady= 12, ipadx=12)

        self.title_label = tk.Label(self.SettingsConfigFrame, text="Eleven Labs API Key",
                                    font=('Verdana', 17, 'bold'), fg=self.bright_blue, bg=self.bg_color, pady=20)
        self.title_label.pack(fill=tk.BOTH, pady=10)

        self.MsgBoxContainer = tk.Frame(self.SettingsConfigFrame, bg="white", padx=2, pady=2)
        self.MsgBoxContainer.pack( fill=tk.X,padx=5, pady=10, expand=True)

        self.message_entry_eleven = tk.Entry(self.MsgBoxContainer, bg=self.entry_bg_color, fg=self.text_color,
                                      insertbackground=self.text_color, font=('Verdana', 15), relief=tk.FLAT,
                                      borderwidth=2, highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.message_entry_eleven.pack( fill=tk.X, expand=True, ipady= 12, ipadx=12)

        self.save_changes = tk.Button(self.SettingsConfigFrame, text="Save Changes", bg=self.button_bg_color, fg=self.button_text_color, highlightbackground=self.border_color, highlightthickness=2, font=('Helvetica', 15),
        relief=tk.FLAT, activebackground=self.accent_color, activeforeground=self.bg_color,
        command=self.save_keys_then_nav_to_main_page)
        self.save_changes.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

        api_keys = self.read_env_file('.env')

        if api_keys:
            if api_keys['OPEN_API_KEY']:
                self.message_entry_gpt.insert(0, api_keys['OPEN_API_KEY'])
            if api_keys['CLAUDE_API_KEY']:
                self.message_entry_claude.insert(0, api_keys['CLAUDE_API_KEY'])
            if api_keys['ELEVEN_LABS_API_KEY']:
                self.message_entry_eleven.insert(0, api_keys['ELEVEN_LABS_API_KEY'])

    
    def save_keys_then_nav_to_main_page(self):
        api_keys = {
            'OPEN_API_KEY': self.message_entry_gpt.get(),
            'CLAUDE_API_KEY': self.message_entry_claude.get(),
            'ELEVEN_LABS_API_KEY': self.message_entry_eleven.get()
        }

        # Write the dictionary to the .env file
        with open('.env', 'w') as file:
            for key, value in api_keys.items():
                file.write(f"{key}={value}\n")
        
        self.show_ai_metaverse_page()




    def nav_to_page(self, model):

        api_keys = self.read_env_file('.env')
        self.selected_model = model
        if self.selected_model == "chatbot":
            if os.getenv("CLAUDE_API_KEY") or api_keys['CLAUDE_API_KEY']:
                self.show_chat_page()

                return
                
        elif self.selected_model == "claude":
            if os.getenv("CLAUDE_API_KEY") or api_keys['CLAUDE_API_KEY']:
                self.show_chat_page()
                return

        self.show_api_page(model=model)

    def show_api_page(self, model):
        self.clear_screen()
        self.selected_model = model

        self.api_frame = tk.Frame(self.root, bg=self.bg_color)
        self.api_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.api_title_label = tk.Label(self.api_frame, text="API Configuration", font=('Verdana', 18, 'bold'),
                                        fg=self.accent_color, bg=self.bg_color, pady=10)
        self.api_title_label.pack(fill=tk.BOTH, pady=10)

        self.api_key_entry = tk.Entry(self.api_frame, bg=self.entry_bg_color, fg=self.text_color,
                                      insertbackground=self.text_color, font=('Verdana', 12), relief=tk.FLAT, 
                                      borderwidth=2, highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.api_key_entry.pack(fill=tk.X, pady=10)

        self.save_api_btn = tk.Button(self.api_frame, text="Save API Key", bg=self.accent_color, fg=self.bg_color,
                                      highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 12, 'bold'),
                                      relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
                                      command=lambda: self.check_api_key(model))
        self.save_api_btn.pack(fill=tk.X, pady=10)

        self.back_btn = tk.Button(self.api_frame, text="Back to AI Metaverse", bg=self.button_bg_color, fg=self.button_text_color,
                                  highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 12, 'bold'),
                                  relief=tk.FLAT, activebackground=self.accent_color, activeforeground=self.bg_color,
                                  command=self.show_ai_metaverse_page)
        self.back_btn.pack(fill=tk.X, pady=10)

    def check_api_key(self, model):
        api_key = self.api_key_entry.get()

        if not api_key:
            messagebox.showerror("Error", "Invalid API Key. Please enter the correct API key.")
            return

        if model == "chatbot":
            self.set_api_key("CLAUDE_API_KEY", api_key)
            self.show_chat_page()
            # Here I want to load message after above function renders ui
            
            return
        
        if model == "claude":
            self.set_api_key("CLAUDE_API_KEY", api_key)
            self.show_chat_page()
            return
        

    
    def load_msgs(self):
        if self.msgs_index < len(self.msgs):
            self.display_message(self.msgs[self.msgs_index].message,self.msgs[self.msgs_index].sender)
            self.msgs_index += 1
            print("load msgs => ", self.msgs_index)
            self.root.after(1000, self.load_msgs)
            


    def set_api_key(self, key_para, value_para):
        env_file = ".env"
        Set_Claude_Api_Key(value_para)

        # Read the existing content of the .env file
        env_data = {}
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                for line in f:
                    if line.strip():  # Ignore empty lines
                        key, value = line.strip().split('=', 1)
                        env_data[key] = value

        # Update the API_KEY or add it if it doesn't exist
        env_data[key_para] = value_para
        # Write the updated content back to the .env file
        with open(env_file, "w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")
            
            f.close()

    def on_frame_configure(self, event):
        print(event)
        # Update scrollregion when chat_frame_inner is resized
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def create_round_image(self,image_path, size):
        # Open the image
        image = Image.open(image_path).resize((size, size), Image.LANCZOS)
        
        # Create a mask for the round shape
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        
        
        # Apply the mask to create a round image
        round_image = Image.new('RGBA', (size, size))
        round_image.paste(image, (0, 0), mask=mask)

        return ImageTk.PhotoImage(round_image)
    
    def create_image(self,image_path, size):
        # Open the image
        image = Image.open(image_path).resize((size, size), Image.LANCZOS)
        
        # Create a mask for the round shape
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((0, 0, size, size), fill=255)

        
        
        # Apply the mask to create a round image
        round_image = Image.new('RGBA', (size, size))
        round_image.paste(image, (0, 0), mask=mask)

        return ImageTk.PhotoImage(round_image)


    def show_chat_page(self):

        self.dark_blue = "#0D1117"

        self.clear_screen()

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=6)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=7)
        self.root.rowconfigure(2, weight=2)
        
        # Top Frame / Header Frame

        self.HeaderFrame = tk.Frame(self.root, bg=self.bg_color)
        self.HeaderFrame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.WrapperFrameLead = tk.Frame(self.HeaderFrame, bg=self.bg_color)
        self.WrapperFrameLead.pack(fill="both", padx=200, pady=10)

        self.LeadingImagePhoto = self.create_round_image(self.image_paths["lead_icon"], 90)
        self.LeadingImage = tk.Label(self.WrapperFrameLead, image=self.LeadingImagePhoto, bg=self.bg_color)
        self.LeadingImage.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.chat_title_label = tk.Label(self.WrapperFrameLead, text="LOVE COMPANION ASSISTANT", font=('Verdana', 22, 'bold'),
                                         fg=self.accent_color, bg=self.bg_color, pady=10)
        self.chat_title_label.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        
        

        # Chat Frame
        
        self.chat_frame = tk.Frame(self.root, bg=self.bg_color)
        self.chat_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # Outer frame (acts as the border)
        self.outer_frame = tk.Frame(self.chat_frame, bg=self.bright_blue, padx=2, pady=2, height=90)
        self.outer_frame.pack(padx=10, pady=10, fill="both")

        # Inner frame (where your content goes)
        self.inner_frame = tk.Frame(self.outer_frame, bg=self.dark_blue, height=100)
        self.inner_frame.pack(fill="both")

        self.round_image = self.create_round_image(self.image_paths["anime"], 50)
        self.image_label = tk.Label(self.inner_frame, image=self.round_image, bg=self.dark_blue)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=8)

        # Info Image

        self.info_image_photo = self.create_round_image(self.image_paths["info"], 40)
        self.info_image = tk.Label(self.inner_frame, image=self.info_image_photo, bg=self.dark_blue)
        self.info_image.pack(side=tk.RIGHT, padx=10, pady=8)

        self.WrapperFrame = tk.Frame(self.inner_frame, bg=self.dark_blue)
        self.WrapperFrame.pack(side=tk.LEFT, fill="both", pady=8)

        # Display Assistant Name next to the image
        text_label = tk.Label(self.WrapperFrame, text="Love Assistant", font=("Helvetica", 14), bg=self.dark_blue, fg="white")
        text_label.pack(side=tk.TOP, padx=10, pady=5)

        # Display date on right side of frame
        text_label = tk.Label(self.WrapperFrame, text="created by @Sohaib", font=("Helvetica", 10), bg=self.dark_blue, fg="white")
        text_label.pack(side=tk.TOP, padx=10)

        self.chat_area = tk.Frame(self.chat_frame, bg=self.dark_blue)
        self.chat_area.pack(fill=tk.BOTH,padx=10, pady=10, expand=True)

        # Add a canvas for scrolling

        self.chat_canvas = tk.Canvas(self.chat_area, bg=self.dark_blue)
        self.chat_scrollbar = Scrollbar(self.chat_area, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

        # Create a frame to hold chat messages
        self.chat_frame_inner = tk.Frame(self.chat_canvas, bg=self.dark_blue)
        self.chat_canvas.create_window((0, 0), window=self.chat_frame_inner, anchor="nw", width=1230)
        # Bind the configure event to update canvas scrollregion
        self.chat_frame_inner.bind("<Configure>", self.on_frame_configure)

        
        

        


        # File Upload Button
        self.image = self.create_image(self.image_paths["upload"], 40)  # Replace with your image file path

        # Create the square button with image
        self.upload_file_btn = tk.Button(self.chat_frame, image=self.image, bg=self.bright_blue, fg=self.bg_color,
                                        highlightbackground=self.border_color, highlightthickness=2,
                                        relief=tk.FLAT, activebackground=self.button_bg_color,
                                        activeforeground=self.button_text_color, command=self.upload_file,
                                        width=50, height=50)  # Width and height set to make the button square
        self.upload_file_btn.pack(side=tk.LEFT,padx=5, pady=10)

        # Message Entry

        self.MsgBoxContainer = tk.Frame(self.chat_frame, bg="white", padx=2, pady=2)
        self.MsgBoxContainer.pack(side=tk.LEFT, fill=tk.X,padx=5, pady=10, expand=True)

        self.message_entry = tk.Entry(self.MsgBoxContainer, bg=self.entry_bg_color, fg=self.text_color,
                                      insertbackground=self.text_color, font=('Verdana', 15), relief=tk.FLAT,
                                      borderwidth=2, highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady= 12, ipadx=12)

        # Set the placeholder text
        self.message_entry.insert(0, "Type a message...")

        # Bind events
        self.message_entry.bind("<FocusIn>", self.on_entry_click)
        self.message_entry.bind("<FocusOut>", self.on_focus_out)

        self.default_text = "Type a message..."

        # Send Message Button
        self.image1 = self.create_image(self.image_paths["send"], 40)

        
        
        self.send_btn = tk.Button(self.chat_frame, image=self.image1, bg=self.bright_blue, fg=self.bg_color,
                                        highlightbackground=self.border_color, highlightthickness=2,
                                        relief=tk.FLAT, activebackground=self.button_bg_color,
                                        activeforeground=self.button_text_color, command=self.Propagate_Task,
                                        width=50, height=50)  # Width and height set to make the button square
        self.send_btn.pack(side=tk.LEFT,padx=5, pady=10)




        # New Frame for Bot Options

        # ai_metaverse_purple = "#8A2BE2"


        self.OptionsFrame = tk.Frame(self.root, bg=self.bg_color)
        self.OptionsFrame.grid(row=1, column=2, sticky="nsew", padx=5)

        self.chat_title_label = tk.Label(self.OptionsFrame, text="Bot Options", font=('Verdana', 14, 'bold'),
                                         fg="white", bg=self.bg_color, pady=10, wraplength=250)
        self.chat_title_label.pack(fill=tk.BOTH, pady=10, padx=10)

        


        # Radio buttons 

        # self.RadioFrameOutLine = tk.Frame(self.OptionsFrame, bg=self.bright_blue, padx=2, pady=2)
        # self.RadioFrameOutLine.pack(padx=10, pady=10, fill=tk.X)

        self.RadioFrame = tk.Frame(self.OptionsFrame, bg=self.button_bg_color)
        self.RadioFrame.pack(fill=tk.X, padx=10, pady=10)

        self.selected_option = tk.StringVar()
        self.selected_option.set("Text")  # Set a default value

        font_settings = ("Helvetica", 16)  # Font family and size


        self.radio1 = tk.Radiobutton(self.RadioFrame, text="Text (文章)", variable=self.selected_option, value="Text", font=font_settings, bg=self.highlight_color, fg="white" , command= self.onRadioChange)
        self.radio2 = tk.Radiobutton(self.RadioFrame, text="Voice (声)", variable=self.selected_option, value="Voice", font=font_settings, bg=self.button_bg_color, fg="white", command= self.onRadioChange)

        self.radio1.pack(anchor=tk.W, padx=10, pady=8, ipadx=8)
        self.radio2.pack(anchor=tk.W, padx=10, pady=8, ipadx=8)
        

        # Task Menu

        self.task_select = tk.StringVar()
        self.task_select.set("AI Bot")
        self.task_menu = tk.OptionMenu(self.OptionsFrame, self.task_select, "Web", "Desktop", "AI Bot")
        self.task_menu.config(bg=self.bright_blue, fg="white", font=('Helvetica', 15))
        self.task_menu.pack(side=tk.TOP, padx=10, pady=20, fill=tk.X)

        self.task_select.trace("w",self.onTaskSelected)

        # 3d Avatar Button
        self.avatar_icon = tk.Button(self.OptionsFrame, text="Create Avatar ( アバター )", bg=self.bright_blue, fg="white",
                                    highlightbackground=self.border_color, highlightthickness=2, font=('Helvetica', 14),
                                    relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
                                    command=self.load_avatar)
        self.avatar_icon.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # Hologram Frame

        self.hologramframeOutline1 = tk.Frame(self.OptionsFrame, bg=self.bright_blue, padx=2, pady=2)
        self.hologramframeOutline1.pack(padx=10, pady=5, fill=tk.X)

        self.hologramframe1 = tk.Frame(self.hologramframeOutline1, bg=self.darkgrey)
        self.hologramframe1.pack(expand=True, fill=tk.BOTH)  # External padding for the frame

        self.hologram1 = self.create_image(self.image_paths['ai1'],230)
        self.container1 = tk.Label(self.hologramframe1, image=self.hologram1, bg=self.darkgrey)
        self.container1.pack( pady=5)

        self.hologramframeOutline = tk.Frame(self.OptionsFrame, bg=self.bright_blue, padx=2, pady=2, height=190)
        self.hologramframeOutline.pack(padx=10, pady=5)

        self.hologramframe = tk.Frame(self.hologramframeOutline, bg=self.darkgrey)
        self.hologramframe.pack(expand=True, fill=tk.BOTH)  # External padding for the frame


        

        # # Create a label to display the image inside the frame
        self.hologramtext = tk.Label(self.hologramframe,text="",  bg=self.darkgrey, fg="white", font=('Helvetica', 12), wraplength=200)
        self.hologramtext.pack(padx=10, pady=5, fill=tk.X, expand=True, ipadx=10)

        # New Frame for File upload and translation

        self.VisualDisplayFrame = tk.Frame(self.root, bg=self.bg_color)
        self.VisualDisplayFrame.grid(row=1, column=0, sticky="nsew", padx=5)


        self.visual_text = tk.Label(self.VisualDisplayFrame, text="Visual Elements Display", font=('Verdana', 14, 'bold'),
                                         fg="white", bg=self.bg_color, pady=10, wraplength=180)
        self.visual_text.pack(fill=tk.BOTH, pady=5, padx=10)


        self.new_canvas = tk.Canvas(self.VisualDisplayFrame, width=250,height=2,  bg=self.bg_color, highlightthickness=0)
        self.new_canvas.pack(fill="both")


        # Draw a rounded rectangle
        # self.rounded_rect = self.create_rounded_rectangle(self.new_canvas, 20, 50, 220, 250, radius=20, fill=self.dark_blue, outline=self.bright_blue)

        self.back_to_metaverse_btn = tk.Button(self.VisualDisplayFrame, text="Back", bg=self.dark_blue, fg=self.button_text_color, highlightbackground=self.border_color, highlightthickness=2, font=('Helvetica', 15),
        relief=tk.FLAT, activebackground=self.accent_color, activeforeground=self.bg_color,
        command=self.show_ai_metaverse_page)
        self.back_to_metaverse_btn.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)



        
        self.type_text("こんにちは, nice to have you here.")

        if len(self.msgs) > 0:
            self.msgs_index = 0
            self.root.update_idletasks()  # Force UI rendering
            self.root.after(1000, self.load_msgs)
    

    def start_loading(self):
        self.FileText = tk.Label(self.VisualDisplayFrame,text="File Uploading . . .",  bg=self.bg_color, fg=self.bright_blue, font=('Helvetica', 12,'bold'), wraplength=250)
        self.FileText.pack(padx=10, pady=10, fill=tk.X, ipadx=10)
        # Draw the initial progress arc
        # Create a custom style for the progress bar
        style = ttk.Style(self.VisualDisplayFrame)
        style.theme_use('clam')

        # Customizing the progress bar colors
        style.configure("TProgressbar",
                        troughcolor='#21262d',  # Dark background color
                        background=self.bright_blue,   # Light blue fill color
                        thickness=10)            # Thickness of the progress bar

        # Create an indeterminate progress bar widget with the custom style
        self.progress_bar = ttk.Progressbar(self.VisualDisplayFrame, orient="horizontal", length=250, mode="indeterminate", style="TProgressbar")
        self.progress_bar.pack(pady=20)
        print("bar loading")
        # File (filename) upload started 
        # self.progress = self.new_canvas.create_arc(70, 100, 180, 210, start=self.angle, extent=0, fill=self.bright_blue, outline=self.bright_blue)
        self.update_progress()

    def update_progress(self):
        self.progress_bar.start(10)
        # Increase the angle to simulate progress
        # self.angle += 5
        # if self.angle > 360:
        #     self.angle = 0
        # self.new_canvas.itemconfig(self.progress, extent=self.angle)
        # # Continue updating the progress bar
        # self.root.after(50, self.update_progress)

    def stop_loading(self):

        self.progress_bar.pack_forget()
        self.FileText.pack_forget()
        # Stop the animation by not calling update_progress anymore
        # if self.progress:
        #     self.new_canvas.delete(self.progress)
        # self.angle = 0

    def type_text(self, text, delay=100):
        """
        Display text in a widget character by character in a separate thread.
        
        :param widget: The Tkinter widget where text will appear (e.g., a Label).
        :param text: The full text to display.
        :param delay: The delay in milliseconds between each character.
        """
        def worker(q, index):
            while True:
                for char in self.hologram_msgs[index]:
                    q.put(char)
                    time.sleep(delay / 1000)  # Convert milliseconds to seconds
                q.put("RESET")  # Signal to reset the text after one cycle
                if index < len(self.hologram_msgs)-1:
                    index += 1
                else:
                    index = 0

        
        def update_text():
            try:
                char = q.get_nowait()
                if char == "RESET":
                    self.hologramtext.config(text="")  # Clear the text to restart the animation
                else:
                    self.hologramtext.config(text=self.hologramtext.cget("text") + char)
            except queue.Empty:
                pass
            finally:
                self.hologramtext.after(delay, update_text)

        index = 0
        q = queue.Queue()
        threading.Thread(target=worker, args=(q,index), daemon=True).start()
        self.hologramtext.after(delay, update_text)
    
    def type_text1(self, text, delay=100):
        """
        Display text in a widget character by character in a separate thread.
        
        :param widget: The Tkinter widget where text will appear (e.g., a Label).
        :param text: The full text to display.
        :param delay: The delay in milliseconds between each character.
        """
        def worker(q):
            while True:
                for char in text:
                    q.put(char)
                    time.sleep(delay / 1000)  # Convert milliseconds to seconds
                q.put("RESET")  # Signal to reset the text after one cycle
        
        def update_text():
            try:
                char = q.get_nowait()
                if char == "RESET":
                    self.chatbot_description.config(text="")  # Clear the text to restart the animation
                else:
                    self.chatbot_description.config(text=self.hologramtext.cget("text") + char)
            except queue.Empty:
                pass
            finally:
                self.chatbot_description.after(delay, update_text)

        q = queue.Queue()
        threading.Thread(target=worker, args=(q,), daemon=True).start()
        self.chatbot_description.after(delay, update_text)
    
    def onRadioChange(self):
        self.Communication = self.selected_option.get()

        image_path = ""
        if self.Communication == "Text":
            self.radio1.config(bg=self.highlight_color)
            self.radio2.config(bg=self.button_bg_color)
            image_path = self.image_paths["send"]
            self.message_entry.config(state=tk.NORMAL)    # Enable entry
        elif self.Communication == "Voice":
            self.radio2.config(bg=self.highlight_color)
            self.radio1.config(bg=self.button_bg_color)
            image_path = self.image_paths["voice"]
            self.message_entry.config(state=tk.DISABLED)  # Disable entry
        
        # Update the button image
        self.image1 = self.create_image(image_path, 40)
        self.send_btn.config(image=self.image1)
        self.send_btn.image = self.image1

        
    
    def onTaskSelected(self, *args):
        self.Task = self.task_select.get()
        print(f"New task selected: {self.Task}")


    def Propagate_Task(self):
        message = self.message_entry.get()
        message = message.strip()
        self.message_entry.delete(0, tk.END)
        
        if self.Communication == "Text":
            if self.Task == "AI Bot":
                self.send_message(message)
            elif self.Task == "Web":
                self.web_task(message)
            elif self.Task == "Desktop":
                self.desktop_task(message)
            
        if self.Communication == "Voice":
            self.send_btn.config(bg="red")
            self.send_btn.update_idletasks()
            threading.Thread(target=self.get_voice_input_and_handle).start()
        
    
    def get_voice_input_and_handle(self):
        # Call the voice recognition function
        message = self.voice_text_interface.get_voice_input()

        # Update the button back to the original color (this needs to be done in the main thread)
        self.send_btn.config(bg=self.accent_color)
        self.send_btn.update_idletasks()

        if self.Task == "AI Bot":
            self.send_message(message)
        elif self.Task == "Web":
            web_request = "Right here serving your web request. Just wait a bit."
            threading.Thread(target=self.process_text_to_speech, args=(web_request,)).start()
            self.web_task(message)
        elif self.Task == "Desktop":
            desktop_request = "Alright, I understand. Going to serve your desktop request"
            threading.Thread(target=self.process_text_to_speech, args=(desktop_request,)).start()
            self.desktop_task(message)

        

    def send_message(self, message):

        if message:
            # Display the user message
            Contextual_query = ""
            for msg in self.msgs:
                Contextual_query += msg.message + "\n"
            Contextual_query += "Here is my query => " + message
            self.msgs.append(Message("user", message))
            self.display_message(message, "user")
        
            # Start a thread for the bot response
            threading.Thread(target=self.handle_bot_response, args=(Contextual_query,), daemon=True).start()
    
    def web_task(self, query):
        
        system_web.web_module(query)

    def desktop_task(self, query):
        
        system_desktop.desktop_module(query=query)
    
    def center_image(self):
        # Get window dimensions
        window_width = self.original_size[0]
        window_height = self.original_size[1]

        # Resize the window to fit the image
        self.root.geometry(f"{window_width}x{window_height}")

        # Calculate initial position to center the image
        self.base_x = 0
        self.base_y = 0

        # Position the image in the center
        self.image_label.place(x=self.base_x, y=self.base_y)

    def handle_bot_response(self, message):
        # Simulate a delay or long-running task
        response = chat_with_claude(message)  # Assuming this function blocks
        if self.Communication == "Voice":
            threading.Thread(target=self.process_text_to_speech, args=(response,)).start()
        self.msgs.append(Message("bot", response))
        # Update UI in the main thread
        self.root.after(0, self.display_message, response, "bot")
            
    def process_text_to_speech(self, response):
        if len(response) < 400:
            self.voice_text_interface.text_to_speech(response)
        else:
            response = "I have a provided a detailed textual material. Hope it will serve you right"
            self.voice_text_interface.text_to_speech(response)

    def display_message(self, message, sender):


        # Create a frame for each message
        name = ""
        side = "w"
        if sender == "user":
            name = "Claire"
        else:
            name = "Love Assistant"
            side = "e"

        message_frame = tk.Frame(self.chat_frame_inner, bg=self.ai_metaverse_purple, padx=10, pady=5)
        message_frame.pack(anchor=side, padx=20, pady=10)

        # Display the user's name in bold
        user_name_label = tk.Label(message_frame, text=name, font=('Verdana', 10, 'bold'), 
                                   bg=self.ai_metaverse_purple, anchor=side, fg="white")
        user_name_label.pack(fill=tk.X)

        # Display the message text
        message_label = tk.Label(message_frame, text=message, font=('Verdana', 10), 
                                 bg=self.ai_metaverse_purple, anchor=side, wraplength=400, fg="white")
        message_label.pack(fill=tk.X, pady=(0, 5))


        now = datetime.now()

        # Format time as hour:minute AM/PM
        formatted_time = now.strftime("%I:%M %p")

        message_time = tk.Label(message_frame, text=formatted_time, font=('Verdana', 7), 
                                 bg=self.ai_metaverse_purple, anchor=side, wraplength=180, fg="white")
        message_time.pack(fill=tk.X, pady=(0, 5))


        self.root.update_idletasks()  # Ensure layout updates are applied
        canvas_height = self.chat_canvas.winfo_height()

        print(canvas_height)
        scroll_region = self.chat_canvas.bbox('all')
        content_height = scroll_region[3] - scroll_region[1]  # Height of the scroll region
        print(content_height)
        # Scroll by the amount needed to reach the end
        if content_height > canvas_height:
            self.chat_canvas.yview_scroll(int(content_height / canvas_height), 'pages')
        # Set the size of the message frame explicitly
        # message_frame.pack_propagate(False)


    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.start_loading()
            # Handle file upload logic here
            print("File Uploaded", f"File {file_path} uploaded successfully.")
            # Start the file processing in a separate thread
            threading.Thread(target=self.process_file, args=(file_path,)).start()
    
    def process_file(self, file_path):
        # Handle file upload logic here
        print("File Uploaded", f"File {file_path} uploaded successfully.")
        context = system_file.file_module(file_path)  # Your file processing function
        print(context)
        self.display_message(context, "bot")
        self.stop_loading()

    def load_avatar(self):
        # Placeholder for loading a 3D avatar
        new_window = tk.Toplevel(self.root)
        new_window.title("Second Window")
        new_window.geometry("400x400")
        
        # Add content to the new window

        self.assistant_avatar = self.create_image(self.image_paths["anime"],400)
        self.container2 = tk.Label(new_window, image=self.assistant_avatar)
        self.container2.pack(fill="both")

        # Disable the maximize button
        new_window.resizable(False, False)
        new_window.update_idletasks()  # Update to apply resizable settings
        


    def select_text_to_text(self):
        # Placeholder for selecting text-to-text option
        messagebox.showinfo("Selection", "Text-to-Text option selected.")

    def select_speech_to_text(self):
        # Placeholder for selecting speech-to-text option
        messagebox.showinfo("Selection", "Speech-to-Text option selected.")

    def show_claude_model_page(self):
        self.clear_screen()
        self.claude_model_frame = tk.Frame(self.root, bg=self.bg_color)
        self.claude_model_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.claude_model_title_label = tk.Label(self.claude_model_frame, text="Claude Model Interaction",
                                                 font=('Verdana', 18, 'bold'), fg=self.accent_color, bg=self.bg_color, pady=10)
        self.claude_model_title_label.pack(fill=tk.BOTH, pady=10)

        self.back_to_metaverse_btn = tk.Button(self.claude_model_frame, text="Back to AI Metaverse", bg=self.button_bg_color, fg=self.button_text_color,
                                               highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 12, 'bold'),
                                               relief=tk.FLAT, activebackground=self.accent_color, activeforeground=self.bg_color,
                                               command=self.show_ai_metaverse_page)
        self.back_to_metaverse_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10)


    def on_entry_click(self, event):
        """Function to clear the placeholder text when the entry is clicked."""
        if self.message_entry.get() == self.default_text:
            self.message_entry.delete(0, tk.END)  # delete all the text in the entry
            self.message_entry.config(fg=self.text_color)  # set the text color to normal

    def on_focus_out(self, event):
        """Function to restore the placeholder text if the entry is empty when it loses focus."""
        if self.message_entry.get() == "":
            self.message_entry.insert(0, self.default_text)
            self.message_entry.config(fg='gray')  # set the text color to gray

    def run(self):
        self.root.mainloop()



base_path = ""
if hasattr(sys, '_MEIPASS'):
    # When running from the bundled executable
    base_path = Path(sys._MEIPASS)
else:
    # When running from the script
    base_path = Path(__file__).resolve().parent

print(base_path)

if __name__== '__main__':

    voice_text_interface = st.ChatInterface()
    root = tk.Tk()
    app = ChatApp(root, voice_text_interface, base_path)
    app.run()



# def create_round_image(image_path, size):
#     # Open the image
#     image = Image.open(image_path).resize((size, size), Image.LANCZOS)
    
#     # Create a mask for the round shape
#     mask = Image.new('L', (size, size), 0)
#     draw = ImageDraw.Draw(mask)
#     draw.ellipse((0, 0, size, size), fill=255)
    
#     # Apply the mask to create a round image
#     round_image = Image.new('RGBA', (size, size))
#     round_image.paste(image, (0, 0), mask=mask)
    
#     return ImageTk.PhotoImage(round_image)



# Create the Tkinter window
# root = tk.Tk()
# root.geometry("400x100")

# # Create a frame to hold the image and text
# # Outer frame (acts as the border)
# outer_frame = tk.Frame(root, bg="white", padx=2, pady=2, height=90)
# outer_frame.pack(padx=10, pady=10, fill="both")

# # Inner frame (where your content goes)
# inner_frame = tk.Frame(outer_frame, bg="black", height=90)
# inner_frame.pack(fill="both")

# # Load and display the round image
# round_image = create_round_image("assistant1.jpeg", 50)
# image_label = tk.Label(inner_frame, image=round_image, bg="black")
# image_label.pack(side=tk.LEFT, padx=10)

# def changeName(label : tk.Label):

#     if label.cget("bg") == "black":
#         label.config(bg="white")
#     else:
#         label.config(bg="black")
#     # time.sleep(5)
#     # label.config(bg= "black")

# # Display text next to the image
# text_label = tk.Label(inner_frame, text="This is some text next to the round image.", font=("Helvetica", 14), bg="black", fg="white")
# text_label.pack(side=tk.LEFT, padx=10)



# btn = tk.Button(inner_frame, text="Change text color", command= lambda : changeName(text_label))
# btn.pack()


# root.mainloop()


# import tkinter as tk
# import random

# class RecordingUI(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("Recording")
#         self.geometry("400x400")
#         self.configure(bg="white")
#         self.resizable(False, False)

#         self.BiggerFrame = tk.Frame(self, bg="red")
#         self.BiggerFrame.pack(fill=tk.BOTH, expand=True)
#         # Container for the recording bar
#         self.frame = tk.Frame(self.BiggerFrame, bg="white", bd=0)
#         self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

#         # Canvas to draw the waveform
#         self.canvas = tk.Canvas(self.frame, width=350, height=60, bg="black", highlightthickness=0)
#         self.canvas.pack()

#         # Start the waveform effect
#         self.waveform()

#     def waveform(self):
#         self.canvas.delete("all")

#         # Number of lines to represent the waveform
#         num_lines = 30

#         # Draw lines with varying heights to simulate a waveform
#         for i in range(num_lines):
#             x = i * 12 + 10  # Horizontal spacing between lines
#             line_height = random.randint(10, 50)  # Random height for the lines
#             self.canvas.create_line(x, 30 - line_height // 2, x, 30 + line_height // 2, fill="white", width=4)

#         # Schedule the next waveform update
#         self.after(100, self.waveform)

# if __name__ == "__main__":
#     app = RecordingUI()
#     app.mainloop()



# def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
#     points = [x1+radius, y1,
#               x1+radius, y1,
#               x2-radius, y1,
#               x2-radius, y1,
#               x2, y1,
#               x2, y1+radius,
#               x2, y1+radius,
#               x2, y2-radius,
#               x2, y2-radius,
#               x2, y2,
#               x2-radius, y2,
#               x2-radius, y2,
#               x1+radius, y2,
#               x1+radius, y2,
#               x1, y2,
#               x1, y2-radius,
#               x1, y2-radius,
#               x1, y1+radius,
#               x1, y1+radius,
#               x1, y1]

#     return canvas.create_polygon(points, **kwargs, smooth=True)

# root = tk.Tk()

# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=6)
# root.columnconfigure(2, weight=1)
# root.rowconfigure(0, weight=2)
# root.rowconfigure(1, weight=7)
# root.rowconfigure(2, weight=2)

# frame = tk.Frame(root, bg="white")
# frame.grid(row=1, column=1, sticky="nsew")


# canvas = tk.Canvas(frame, width=300, height=200, bg="white", highlightthickness=0)
# canvas.pack(fill="both", expand=True)


# # Draw a rounded rectangle
# rounded_rect = create_rounded_rectangle(canvas, 50, 50, 1250, 150, radius=20, fill="red", outline="black")

# # Place a frame inside the rounded rectangle
# frame = tk.Frame(canvas, bg="black")
# frame.pack(fill="both", expand=True, padx=10, pady=10)

# # # Add content to the frame
# # label = tk.Label(frame, text="Hello, Tkinter!", bg="lightblue")
# # label.pack(pady=20)

# root.mainloop()

# def type_text(widget, text, delay=100):
#     """
#     Display text in a widget character by character in a separate thread.
    
#     :param widget: The Tkinter widget where text will appear (e.g., a Label).
#     :param text: The full text to display.
#     :param delay: The delay in milliseconds between each character.
#     """
#     def worker(q):
#         while True:
#             for char in text:
#                 q.put(char)
#                 time.sleep(delay / 1000)  # Convert milliseconds to seconds
#             q.put("RESET")  # Signal to reset the text after one cycle
    
#     def update_text():
#         try:
#             char = q.get_nowait()
#             if char == "RESET":
#                 widget.config(text="")  # Clear the text to restart the animation
#             else:
#                 widget.config(text=widget.cget("text") + char)
#         except queue.Empty:
#             pass
#         finally:
#             widget.after(delay, update_text)

#     q = queue.Queue()
#     threading.Thread(target=worker, args=(q,), daemon=True).start()
#     widget.after(delay, update_text)

# # Create the main Tkinter window
# root = tk.Tk()
# root.title("Typing Text Effect")
# root.geometry("400x200")

# # Create a label where the text will appear
# label = tk.Label(root, font=("Arial", 20))
# label.pack(pady=20)

# # Start the typing effect in a separate thread that runs throughout the app's lifetime
# type_text(label, "This text will continuously type...", delay=100)

# root.mainloop()

# def start_progress():
#     progress_bar.start(10)  # Start the indeterminate animation with a 10ms interval

# def stop_progress():
#     progress_bar.stop()  # Stop the indeterminate animation

# def hide_progress_bar():
#     progress_bar.pack_forget()  # Hide the progress bar

# def show_progress_bar():
#     progress_bar.pack(pady=20)  # Show the progress bar again

# # Create the main window
# root = tk.Tk()
# root.title("Hide Progress Bar Example")
# root.geometry("300x200")

# # Create a custom style for the progress bar
# style = ttk.Style(root)
# style.theme_use('clam')

# # Customizing the progress bar colors
# style.configure("TProgressbar",
#                 troughcolor='#21262d',  # Dark background color
#                 background='#00aaff',   # Light blue fill color
#                 thickness=20)            # Thickness of the progress bar

# # Create an indeterminate progress bar widget with the custom style
# progress_bar = ttk.Progressbar(root, orient="horizontal", length=250, mode="indeterminate", style="TProgressbar")
# progress_bar.pack(pady=20)

# # Create buttons to start, stop, hide, and show the progress bar
# start_button = tk.Button(root, text="Start", command=start_progress)
# start_button.pack(pady=5)

# stop_button = tk.Button(root, text="Stop", command=stop_progress)
# stop_button.pack(pady=5)

# hide_button = tk.Button(root, text="Hide", command=hide_progress_bar)
# hide_button.pack(pady=5)

# show_button = tk.Button(root, text="Show", command=show_progress_bar)
# show_button.pack(pady=5)

# # Run the application
# root.mainloop()


# import tkinter as tk
# from PIL import Image, ImageTk
# from pathlib import Path

# APP_TITLE = "AI Metaverse"

# class MainPage:
#     def __init__(self, root, interface):
#         self.root = root
#         self.root.title(APP_TITLE)
#         self.voice_text_interface = interface

#         # Define colors
#         self.bg_color = "#6A0D91"  # Background color of the window
#         self.header_bg_color = "#4B0082"  # Deep purple for the header
#         self.text_color = "#EDEDED"  # Light gray text color for better readability
#         self.button_bg_color = "#6A0D91"  # Purple background for buttons
#         self.button_text_color = "#EDEDED"  # Light gray text color for buttons
#         self.border_color = "#9370DB"  # Bright purple for borders
#         self.accent_color = "#9370DB"  # Medium purple for accents
#         self.bright_blue = "#1E90FF"  # Bright blue for accent
#         self.ai_metaverse_purple = "#4B0082"  # Vivid purple for specific elements
#         self.purple_dark_shade = "#4B0082"  # Dark purple for shadows and dark elements
#         self.medium_purple = "#9370DB"  # Medium purple for the gate label

#         # Window configuration
#         self.root.geometry("1000x700")
#         self.root.configure(bg=self.bg_color)
#         self.root.wm_attributes('-alpha', 1)  

#         # Image paths (Relative to the current script)
#         self.image_paths = {
#             "settings": Path("Images/setting.png"),
#             "ai_logo": Path("Images/ai.png"),
#             "metaverse_bg": Path("Images/metaverse_bg3.jpg")  # Updated image file
#         }

#         self.show_ai_metaverse_page()

#     def clear_screen(self):
#         for widget in self.root.winfo_children():
#             widget.destroy()

#     def create_image(self, image_path, size):
#         image = Image.open(image_path).resize((size, size), Image.LANCZOS)
#         return ImageTk.PhotoImage(image)

#     def create_round_button(self, parent, text, command, width=350, height=60, color=None, text_color=None):
#         canvas = tk.Canvas(parent, width=width, height=height, bg=color, bd=0, highlightthickness=0, relief=tk.FLAT)
#         canvas.pack_propagate(False)  # Prevent canvas from resizing to fit content

#         r = min(width, height) // 2  # Use radius based on button dimensions

#         # Draw rounded rectangle
#         canvas.create_oval((0, 0, 2*r, 2*r), fill=color, outline=color)  # Top-left corner
#         canvas.create_oval((width-2*r, 0, width, 2*r), fill=color, outline=color)  # Top-right corner
#         canvas.create_oval((0, height-2*r, 2*r, height), fill=color, outline=color)  # Bottom-left corner
#         canvas.create_oval((width-2*r, height-2*r, width, height), fill=color, outline=color)  # Bottom-right corner
        
#         canvas.create_rectangle((r, 0, width-r, height), fill=color, outline=color)  # Center rectangle (top)
#         canvas.create_rectangle((0, r, width, height-r), fill=color, outline=color)  # Center rectangle (left)

#         # Add text
#         canvas.create_text(width//2, height//2, text=text, fill=text_color, font=('Verdana', 16, 'bold'))
#         canvas.bind("<Button-1>", lambda e: command())
        
#         return canvas

#     def show_ai_metaverse_page(self):
#         self.clear_screen()

#         # Metaverse Background Image
#         self.metaverse_bg_image = Image.open(self.image_paths["metaverse_bg"])
#         self.metaverse_bg_image = self.metaverse_bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
#         self.metaverse_bg_photo = ImageTk.PhotoImage(self.metaverse_bg_image)

#         # Set background image as a label filling the whole screen
#         self.metaverse_bg_label = tk.Label(self.root, image=self.metaverse_bg_photo, bg=self.bg_color)
#         self.metaverse_bg_label.place(relwidth=1, relheight=1)

#         # Modern Header Frame
#         self.header_frame = tk.Frame(self.root, bg=self.header_bg_color)
#         self.header_frame.place(relx=0.5, rely=0.05, anchor='n', relwidth=1)

#         # Header Design
#         self.title_label = tk.Label(self.header_frame, text="Welcome to the AI Metaverse!",
#                                     font=('Verdana', 24, 'bold'), fg=self.bright_blue, bg=self.header_bg_color, pady=10)
#         self.title_label.pack()

#         # Settings Button
#         self.settings_button_frame = tk.Frame(self.header_frame, bg=self.header_bg_color)
#         self.settings_button_frame.pack(side=tk.RIGHT)

#         self.imageSettings = self.create_image(self.image_paths["settings"], 50)
#         self.setting_Btn = tk.Button(self.settings_button_frame, image=self.imageSettings, bg=self.header_bg_color, fg=self.header_bg_color,
#                                      highlightbackground=self.border_color, highlightthickness=2, relief=tk.FLAT,
#                                      activebackground=self.button_bg_color, activeforeground=self.button_text_color,
#                                      command=lambda: self.settings_page(), width=50, height=50)
#         self.setting_Btn.pack(side=tk.RIGHT)

#         # Logo at the top center
#         self.ai_logo_image = self.create_image(self.image_paths["ai_logo"], 100)  # Larger size for visibility
#         self.ai_logo_label = tk.Label(self.header_frame, image=self.ai_logo_image, bg=self.header_bg_color)
#         self.ai_logo_label.pack(side=tk.TOP, pady=10)

#         # Main Frame
#         self.ai_metaverse_frame = tk.Frame(self.root, bg=self.bg_color)
#         self.ai_metaverse_frame.place(relx=0.5, rely=0.5, anchor='center')

#         # Using canvas for rounded button
#         self.chatbot_frame = tk.Canvas(self.ai_metaverse_frame, bg=self.ai_metaverse_purple, bd=0, highlightthickness=0)
#         self.chatbot_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

#         # Upper Frame with Two Labels
#         self.LeadWrapperFrame = tk.Frame(self.chatbot_frame, bg=self.ai_metaverse_purple)
#         self.LeadWrapperFrame.pack(side=tk.TOP, padx=10, fill=tk.X, expand=True)

#         # "FIND YOUR INNER GATE" Button
#         self.find_inner_gate_btn = self.create_round_button(
#             self.LeadWrapperFrame, text="FIND YOUR INNER GATE",
#             command=lambda: self.nav_to_page("claude"),
#             color=self.purple_dark_shade, text_color=self.bg_color
#         )
#         self.find_inner_gate_btn.pack(side=tk.LEFT, padx=10, pady=10)

#         # "EXPERIENCE 3D COMPANION" Button
#         self.experience_3d_companion_btn = self.create_round_button(
#             self.ai_metaverse_frame, text="EXPERIENCE 3D COMPANION",
#             command=lambda: self.nav_to_page("claude"),
#             color=self.purple_dark_shade, text_color=self.bg_color,
#             width=400, height=70  # Increased width and height
#         )
#         self.experience_3d_companion_btn.pack(fill=tk.X, pady=20, expand=True, padx=10)

#     def nav_to_page(self, page):
#         if page == "claude":
#             self.show_chat_page()

#     def settings_page(self):
#         # Implement settings page navigation here
#         pass

#     def show_chat_page(self):
#         # Implement chatbot page navigation here
#         pass

#     def read_env_file(self, file_path):
#         api_keys = {}
#         with open(file_path, 'r') as file:
#             for line in file:
#                 line = line.strip()
#                 if line:
#                     key, value = line.split('=', 1)
#                     api_keys[key] = value
#         return api_keys

# # Example Usage

# root = tk.Tk()
# interface = None
# app = MainPage(root, interface)
# root.mainloop()


# class FullScreenApp:
#     def __init__(self, root, image_path):
#         self.root = root

#         # Make the window full-screen
#         # self.root.attributes('-fullscreen', True)
#         # self.root.bind("<Escape>", self.exit_fullscreen)

#         # Get the screen dimensions
#         screen_width = root.winfo_screenwidth()
#         screen_height = root.winfo_screenheight()

#         # Create a Canvas widget that fills the screen
#         self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
#         self.canvas.pack(fill="both", expand=True)

#         # Load and resize the image to fit the screen
#         self.image = Image.open(image_path)
#         self.image = self.image.resize((screen_width, screen_height), Image.ANTIALIAS)
#         self.photo_image = ImageTk.PhotoImage(self.image)

#         # Display the image on the Canvas
#         self.canvas.create_image(0, 0, anchor='nw', image=self.photo_image)

#         # Add text on top of the image
#         self.canvas.create_text(screen_width // 2, screen_height // 2, 
#                                text="Welcome to the Full-Screen App!", 
#                                fill="white", font=('Arial', 24, 'bold'), anchor='center')

#         # Example: Add a button on top of the image
#         button = tk.Button(root, text="Exit", command=self.exit_fullscreen, bg="red", fg="white", font=('Arial', 16, 'bold'))
#         self.canvas.create_window(screen_width // 2, screen_height // 2 + 50, anchor='center', window=button)

#     def exit_fullscreen(self, event=None):
#         self.root.attributes('-fullscreen', False)
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()

#     # Replace with the path to your image
#     image_path = "Images/metaverse_bg3.jpg"
#     app = FullScreenApp(root, image_path)

#     root.mainloop()
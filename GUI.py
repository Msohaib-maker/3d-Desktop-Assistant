import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar
from dotenv import load_dotenv
import os
from chatModels.claude import *
import threading
from tkinter import PhotoImage
import system_web
import system_desktop
from PIL import Image, ImageTk, ImageDraw
import speech_text as st
import sys
import time
from pathlib import Path

load_dotenv()

APP_TITLE = "3D Assistant"
AI_METAVERSE_PAGE = "AI Metaverse"
CHATBOT_PAGE = "Chatbot"
CLAUDE_MODEL_PAGE = "Claude Model"
API_PAGE = "API Page"


# SET API KEYS AREA

claude_api_key =  os.getenv("CLAUDE_API_KEY")
Set_Claude_Api_Key(claude_api_key)
    

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

        self.root.geometry("800x600")
        root.configure(bg=self.bg_color)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=6)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=7)
        root.rowconfigure(2, weight=2)

        self.image_paths = {
            "send": Path(str(self.abspath / "send.png")),
            "voice": Path(str(self.abspath / "voice.png")),
            "upload": Path(str(self.abspath / "upload.png"))
        }

        # arr for holding chat (text) msgs
        self.msgs = []
        self.msgs_index = 0

        self.Communication = "Text"
        self.Task = "AI Bot"

        self.show_ai_metaverse_page()
        # self.show_chat_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_ai_metaverse_page(self):
        self.clear_screen()
        self.ai_metaverse_frame = tk.Frame(self.root, bg=self.bg_color)
        self.ai_metaverse_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.title_label = tk.Label(self.ai_metaverse_frame, text="Welcome to the AI Metaverse!",
                                    font=('Verdana', 18, 'bold'), fg=self.accent_color, bg=self.bg_color, pady=10)
        self.title_label.pack(fill=tk.BOTH, pady=10)

        self.chatbot_frame = tk.Frame(self.ai_metaverse_frame, bg="#2d333b", bd=2, relief=tk.RAISED)
        self.chatbot_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.chatbot_label = tk.Label(self.chatbot_frame, text="GPT 4-o Model",
                                      font=('Verdana', 16, 'bold'), fg=self.accent_color, bg="#2d333b", pady=10)
        self.chatbot_label.pack(fill=tk.BOTH, pady=5)
        
        self.chatbot_description = tk.Label(self.chatbot_frame, text="Interact with an AI chatbot for general queries and assistance.",
                                            font=('Verdana', 12), fg=self.text_color, bg="#2d333b", padx=10, pady=10, wraplength=700)
        self.chatbot_description.pack(fill=tk.BOTH, pady=5)

        self.claude_model_frame = tk.Frame(self.ai_metaverse_frame, bg="#2d333b", bd=2, relief=tk.RAISED)
        self.claude_model_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.claude_model_label = tk.Label(self.claude_model_frame, text="Claude Model",
                                          font=('Verdana', 16, 'bold'), fg=self.accent_color, bg="#2d333b", pady=10)
        self.claude_model_label.pack(fill=tk.BOTH, pady=5)
        
        self.claude_model_description = tk.Label(self.claude_model_frame, text="Engage with the Claude model for advanced AI interactions.",
                                                 font=('Verdana', 12), fg=self.text_color, bg="#2d333b", padx=10, pady=10, wraplength=700)
        self.claude_model_description.pack(fill=tk.BOTH, pady=5)

        self.select_chatbot_btn = tk.Button(self.ai_metaverse_frame, text="Select Chatbot", bg=self.accent_color, fg=self.bg_color,
                                            highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 12, 'bold'),
                                            relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
                                            command=lambda: self.nav_to_page("chatbot"))
        self.select_chatbot_btn.pack(fill=tk.X, pady=10)

        self.select_claude_btn = tk.Button(self.ai_metaverse_frame, text="Select Claude Model", bg=self.accent_color, fg=self.bg_color,
                                           highlightbackground=self.border_color, highlightthickness=2, font=('Verdana', 12, 'bold'),
                                           relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
                                           command=lambda: self.nav_to_page("claude"))
        self.select_claude_btn.pack(fill=tk.X, pady=10)

    def nav_to_page(self, model):
        self.selected_model = model
        if self.selected_model == "chatbot":
            if os.getenv("CLAUDE_API_KEY"):
                self.show_chat_page()

                return
                
        elif self.selected_model == "claude":
            if os.getenv("CLAUDE_API_KEY"):
                self.show_claude_model_page()
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
            self.show_claude_model_page()
            return
    
    def load_msgs(self):
        if self.msgs_index < len(self.msgs):
            self.display_message(self.msgs[self.msgs_index].message,self.msgs[self.msgs_index].sender)
            self.msgs_index += 1
            print("load msgs => ", self.msgs_index)
            self.root.after(1000, self.load_msgs)
            


    def set_api_key(self, key_para, value_para):
        env_file = ".env"

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

        dark_blue = "#0D1117"

        self.clear_screen()
        
        # Top Frame / Header Frame

        self.HeaderFrame = tk.Frame(self.root, bg=self.bg_color)
        self.HeaderFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.chat_title_label = tk.Label(self.HeaderFrame, text="LOVE COMPANION", font=('Verdana', 20, 'bold'),
                                         fg=self.accent_color, bg=self.bg_color, pady=10)
        self.chat_title_label.pack(fill=tk.BOTH, pady=10)
        

        # Chat Frame
        
        self.chat_frame = tk.Frame(self.root, bg=self.bg_color)
        self.chat_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # Outer frame (acts as the border)
        self.outer_frame = tk.Frame(self.chat_frame, bg="white", padx=2, pady=2, height=90)
        self.outer_frame.pack(padx=10, pady=10, fill="both")

        # Inner frame (where your content goes)
        self.inner_frame = tk.Frame(self.outer_frame, bg=dark_blue, height=90)
        self.inner_frame.pack(fill="both")

        self.round_image = self.create_round_image("assistant1.jpeg", 50)
        self.image_label = tk.Label(self.inner_frame, image=self.round_image, bg=dark_blue)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=8)

        # Display text next to the image
        text_label = tk.Label(self.inner_frame, text="Love Assistant", font=("Helvetica", 14), bg=dark_blue, fg="white")
        text_label.pack(side=tk.LEFT, padx=10, pady=8)

        self.chat_area = tk.Frame(self.chat_frame, bg=dark_blue, relief=tk.RAISED)
        self.chat_area.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Add a canvas for scrolling

        

        self.chat_canvas = tk.Canvas(self.chat_area, bg=dark_blue)
        self.chat_scrollbar = Scrollbar(self.chat_area, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

        # Create a frame to hold chat messages
        print(self.chat_canvas.winfo_width())
        self.chat_frame_inner = tk.Frame(self.chat_canvas, bg=dark_blue)
        self.chat_canvas.create_window((0, 0), window=self.chat_frame_inner, anchor="nw", width=1200)
        # Bind the configure event to update canvas scrollregion
        self.chat_frame_inner.bind("<Configure>", self.on_frame_configure)
        

        


        # File Upload Button
        self.image = self.create_image(self.image_paths["upload"], 40)  # Replace with your image file path

        # Create the square button with image
        self.upload_file_btn = tk.Button(self.chat_frame, image=self.image, bg=self.accent_color, fg=self.bg_color,
                                        highlightbackground=self.border_color, highlightthickness=2,
                                        relief=tk.FLAT, activebackground=self.button_bg_color,
                                        activeforeground=self.button_text_color, command=self.upload_file,
                                        width=50, height=50)  # Width and height set to make the button square
        self.upload_file_btn.pack(side=tk.LEFT,padx=5, pady=10)

        # Message Entry
        self.message_entry = tk.Entry(self.chat_frame, bg=self.entry_bg_color, fg=self.text_color,
                                      insertbackground=self.text_color, font=('Verdana', 15), relief=tk.FLAT,
                                      borderwidth=2, highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10, expand=True, ipady= 12, ipadx=12)

        # Set the placeholder text
        self.message_entry.insert(0, "Type a message...")

        # Bind events
        self.message_entry.bind("<FocusIn>", self.on_entry_click)
        self.message_entry.bind("<FocusOut>", self.on_focus_out)

        self.default_text = "Type a message..."

        # Send Message Button
        self.image1 = self.create_image(self.image_paths["send"], 40)

        
        
        self.send_btn = tk.Button(self.chat_frame, image=self.image1, bg=self.accent_color, fg=self.bg_color,
                                        highlightbackground=self.border_color, highlightthickness=2,
                                        relief=tk.FLAT, activebackground=self.button_bg_color,
                                        activeforeground=self.button_text_color, command=self.Propagate_Task,
                                        width=50, height=50)  # Width and height set to make the button square
        self.send_btn.pack(side=tk.LEFT,padx=5, pady=10)




        # New Frame

        ai_metaverse_purple = "#8A2BE2"


        self.OptionsFrame = tk.Frame(self.root, bg=self.bg_color)
        self.OptionsFrame.grid(row=1, column=2, sticky="nsew", padx=5)

        self.chat_title_label = tk.Label(self.OptionsFrame, text="Bot Custom Options", font=('Verdana', 15, 'bold'),
                                         fg="white", bg=self.bg_color, pady=10)
        self.chat_title_label.pack(fill=tk.BOTH, pady=10, padx=10)

        self.RadioFrame = tk.Frame(self.OptionsFrame, bg=self.button_bg_color)
        self.RadioFrame.pack(padx=10, pady=10, fill=tk.X)


        # Radio buttons 
        self.selected_option = tk.StringVar()
        self.selected_option.set("Text")  # Set a default value

        font_settings = ("Helvetica", 16)  # Font family and size

        

        self.radio1 = tk.Radiobutton(self.RadioFrame, text="Text", variable=self.selected_option, value="Text", font=font_settings, bg=self.highlight_color, fg="white" , command= self.onRadioChange)
        self.radio2 = tk.Radiobutton(self.RadioFrame, text="Voice", variable=self.selected_option, value="Voice", font=font_settings, bg=self.button_bg_color, fg="white", command= self.onRadioChange)

        self.radio1.pack(anchor=tk.W, padx=10, pady=8, ipadx=8)
        self.radio2.pack(anchor=tk.W, padx=10, pady=8, ipadx=8)
        

        # Task Menu

        self.task_select = tk.StringVar()
        self.task_select.set("AI Bot")
        self.task_menu = tk.OptionMenu(self.OptionsFrame, self.task_select, "Web", "Desktop", "AI Bot")
        self.task_menu.config(bg=ai_metaverse_purple, fg="white", font=('Helvetica', 15))
        self.task_menu.pack(side=tk.TOP, padx=10, pady=20, fill=tk.X)

        self.task_select.trace("w",self.onTaskSelected)

        # 3d Avatar Button
        self.avatar_icon = tk.Button(self.OptionsFrame, text="3D Avatar", bg=ai_metaverse_purple, fg="white",
                                    highlightbackground=self.border_color, highlightthickness=2, font=('Helvetica', 15),
                                    relief=tk.FLAT, activebackground=self.button_bg_color, activeforeground=self.button_text_color,
                                    command=self.load_avatar)
        self.avatar_icon.pack(side=tk.TOP, padx=10, pady=20, fill=tk.X)

        # Hologram Frame

        self.hologramframe = tk.Frame(self.OptionsFrame, bg=self.button_bg_color, padx=20, pady=10)
        self.hologramframe.pack(padx=10, pady=20, expand=True, fill=tk.X)  # External padding for the frame


        self.hologram1 = self.create_image("ai1.png",300)
        self.container1 = tk.Label(self.hologramframe, image=self.hologram1, bg=self.button_bg_color)
        self.container1.pack(side=tk.BOTTOM, pady=40)

        # # Create a label to display the image inside the frame
        self.hologramtext = tk.Label(self.hologramframe,text="Hologram Display Here",  bg=self.button_bg_color, fg="white", font=('Helvetica', 15))
        self.hologramtext.pack(padx=10, pady=10, fill=tk.X, expand=True, ipadx=10)

        

        self.back_to_metaverse_btn = tk.Button(self.OptionsFrame, text="Back", bg=self.button_bg_color, fg=self.button_text_color,
                                            highlightbackground=self.border_color, highlightthickness=2, font=('Helvetica', 15),
                                            relief=tk.FLAT, activebackground=self.accent_color, activeforeground=self.bg_color,
                                            command=self.show_ai_metaverse_page)
        self.back_to_metaverse_btn.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)


        # Label for Listening ...

        # Create and pack the label

        self.NewFrame = tk.Frame(self.root, padx=10)
        self.NewFrame.grid(column=0, row=1)

        self.status_label = tk.Label(self.NewFrame, text="", font=("Helvetica", 12), bg=self.bg_color, fg="white")
        self.status_label.pack(pady=10)



        if len(self.msgs) > 0:
            self.msgs_index = 0
            self.root.update_idletasks()  # Force UI rendering
            self.root.after(1000, self.load_msgs)

    
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
            pass
            
        if self.Communication == "Voice":
            self.send_btn.config(bg="red")
            self.send_btn.update_idletasks()
            message = self.voice_text_interface.get_voice_input()
            self.send_btn.config(bg=self.accent_color)
        
        if self.Task == "AI Bot":
            self.send_message(message)
        elif self.Task == "Web":
            self.web_task(message)
        elif self.Task == "Desktop":
            self.desktop_task(message)

    def send_message(self, message):

        if message:
            # Display the user message
            self.msgs.append(Message("user", message))
            self.display_message(message, "user")
        
            # Start a thread for the bot response
            threading.Thread(target=self.handle_bot_response, args=(message,), daemon=True).start()
    
    def web_task(self, query):
        
        system_web.web_module(query)

    def desktop_task(self, query):
        
        system_desktop.desktop_module(query=query)

    def handle_bot_response(self, message):
        # Simulate a delay or long-running task
        response = chat_with_claude(message)  # Assuming this function blocks
        self.msgs.append(Message("bot", response))
        # Update UI in the main thread
        self.root.after(0, self.display_message, response, "bot")
            

    def display_message(self, message, sender):


        # Create a frame for each message
        name = ""
        side = "w"
        if sender == "user":
            name = "Claire"
        else:
            name = "Love Assistant"
            side = "e"

        message_frame = tk.Frame(self.chat_frame_inner, bg=self.darkgrey, padx=10, pady=5, width=200, height=80)
        message_frame.pack(anchor=side, padx=10, pady=5)

        # Display the user's name in bold
        user_name_label = tk.Label(message_frame, text=name, font=('Verdana', 10, 'bold'), 
                                   bg=self.darkgrey, anchor=side, fg="white")
        user_name_label.pack(fill=tk.X)

        # Display the message text
        message_label = tk.Label(message_frame, text=message, font=('Verdana', 10), 
                                 bg=self.darkgrey, anchor=side, wraplength=180, fg="white")
        message_label.pack(fill=tk.X, pady=(0, 5))

        # Set the size of the message frame explicitly
        # message_frame.pack_propagate(False)


    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Handle file upload logic here
            messagebox.showinfo("File Uploaded", f"File {file_path} uploaded successfully.")

    def load_avatar(self):
        # Placeholder for loading a 3D avatar
        messagebox.showinfo("Load Avatar", "3D Avatar feature is not yet implemented.")

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

# if __name__== '__main__':

#     voice_text_interface = st.ChatInterface()
#     root = tk.Tk()
#     app = ChatApp(root, voice_text_interface, base_path)
#     app.run()



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


import tkinter as tk
import random

class RecordingUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Recording")
        self.geometry("400x100")
        self.configure(bg="white")
        self.resizable(False, False)

        # Container for the recording bar
        self.frame = tk.Frame(self, bg="white", bd=0)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas to draw the waveform
        self.canvas = tk.Canvas(self.frame, width=350, height=60, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Start the waveform effect
        self.waveform()

    def waveform(self):
        self.canvas.delete("all")

        # Number of lines to represent the waveform
        num_lines = 30

        # Draw lines with varying heights to simulate a waveform
        for i in range(num_lines):
            x = i * 12 + 10  # Horizontal spacing between lines
            line_height = random.randint(10, 50)  # Random height for the lines
            self.canvas.create_line(x, 30 - line_height // 2, x, 30 + line_height // 2, fill="white", width=4)

        # Schedule the next waveform update
        self.after(100, self.waveform)

if __name__ == "__main__":
    app = RecordingUI()
    app.mainloop()


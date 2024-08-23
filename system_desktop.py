from chatModels.claude import *
from Desktop_Module.action_interpreter import *
import speech_text as st
import re


# pip install anthropic + Desktop_Module/action_performer.py mein jo libs ha

# Outside both desktop Module and chatModels

# Testing part 1

    # voice input from the user
    # voice input convert to text
    # text interpret claude api
    # For example - open the notepad , open the word application, close the word application
    # claude chat function - prompt it to find the [open | close ] , [ notepad | application ] keywords
    # Application open successfully - Bot will say

# Voice input and conversion


def extract_single_quoted_words(text):
    # Use regex to find all single-quoted words
    quoted_words = re.findall(r"'(.*?)'", text)
    # Remove duplicates by converting the list to a set and then back to a list
    unique_quoted_words = list(set(quoted_words))
    return unique_quoted_words



def desktop_module(query):

    # text interpretation 

    claude_prompt = "Hey, Can you find specific keywords like open, close, notepad, word from the text and highlight them using single quotes. However, it could be some other desktop application or some browser other notepad or word so if you know you should highlight it too. Here goes the line => " + query

    result = chat_with_claude(claude_prompt)

    cmd_arr = extract_single_quoted_words(result)

    apps = ["telegram", "Whatsapp","Browser","Chrome","Microsoft", "file explorer","explorer"]

    for app in apps:
        if app.lower() in result.lower():
            cmd_arr.append(app)

    print(result,"  ", cmd_arr)

    translate_action(cmd_arr)

    

    

# interface = st.ChatInterface()
# audio_text = interface.speech_to_text()
# system_desktop(audio_text)
# bot_response = "Your request is served"
# interface.text_to_speech(bot_response)



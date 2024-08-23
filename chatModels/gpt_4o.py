import openai
from dotenv import load_dotenv
import os

load_dotenv()


openai.api_key = ""

def set_api_key(self, key_str):
    openai.api_key = key_str



# This model allows us to create chatbot
def chat_with_gpt(prompt):

    if openai.api_key:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()
    
    return "No API Key"




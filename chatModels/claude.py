import os
from anthropic import Anthropic


client = None


def Set_Claude_Api_Key(key):
    global client

    print("CLAUDE INIT (API KEY) DONE . . .")
    client = Anthropic(
        # This is the default and can be omitted
        api_key=key,
    )
    print(key)

def chat_with_claude(prompt):

    global client

    if client:
        message = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-opus-20240229",
        )

        # Extract the assistant's response text
        assistant_message = message.content[0].text
        
        return assistant_message
    
    return "Simulated Response from the System. No Real Bot avaliable. Api Key Not Set"


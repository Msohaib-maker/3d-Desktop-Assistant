import json
import os
import uuid
from curl_cffi import requests
import requests as req
import re


class Client:

  def __init__(self, cookie):
    self.cookie = cookie
    self.organization_id = self.get_organization_id()

  def get_organization_id(self):
    url = "https://claude.ai/api/organizations"

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://claude.ai/chats',
        'Content-Type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': f'{self.cookie}'
    }

    response = requests.get(url, headers=headers,impersonate="chrome110")
    res = json.loads(response.text)
    uuid = res[0]['uuid']

    return uuid

  def get_content_type(self, file_path):
    # Function to determine content type based on file extension
    extension = os.path.splitext(file_path)[-1].lower()
    if extension == '.pdf':
      return 'application/pdf'
    elif extension == '.txt':
      return 'text/plain'
    elif extension == '.csv':
      return 'text/csv'
    # Add more content types as needed for other file types
    else:
      return 'application/octet-stream'

  # Lists all the conversations you had with Claude
  def list_all_conversations(self):
    url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations"

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://claude.ai/chats',
        'Content-Type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': f'{self.cookie}'
    }

    response = requests.get(url, headers=headers,impersonate="chrome110")
    conversations = response.json()

    # Returns all conversation information in a list
    if response.status_code == 200:
      return conversations
    else:
      print(f"Error: {response.status_code} - {response.text}")

  # Send Message to Claude
  def send_message(self, prompt, conversation_id, attachment=None,timeout=500):
    url = "https://claude.ai/api/append_message"

    # Upload attachment if provided
    attachments = []
    if attachment:
      attachment_response = self.upload_attachment(attachment)
      if attachment_response:
        attachments = [attachment_response]
      else:
        return {"Error: Invalid file format. Please try again."}

    # Ensure attachments is an empty list when no attachment is provided
    if not attachment:
      attachments = []

    payload = json.dumps({
      "completion": {
        "prompt": f"{prompt}",
        "timezone": "Asia/Kolkata",
        "model": "claude-2"
      },
      "organization_uuid": f"{self.organization_id}",
      "conversation_uuid": f"{conversation_id}",
      "text": f"{prompt}",
      "attachments": attachments
    })

    headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
      'Accept': 'text/event-stream, text/event-stream',
      'Accept-Language': 'en-US,en;q=0.5',
      'Referer': 'https://claude.ai/chats',
      'Content-Type': 'application/json',
      'Origin': 'https://claude.ai',
      'DNT': '1',
      'Connection': 'keep-alive',
      'Cookie': f'{self.cookie}',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'TE': 'trailers'
    }

    response = requests.post( url, headers=headers, data=payload,impersonate="chrome110",timeout=2000)

    print(response.content)

    decoded_data = response.content.decode("utf-8")
    decoded_data = re.sub('\n+', '\n', decoded_data).strip()
    data_strings = decoded_data.split('\n')
    completions = []
    for data_string in data_strings:
      json_str = data_string[6:].strip()
      
      data = json.loads(json_str)
      if 'completion' in data:
        completions.append(data['completion'])

    answer = ''.join(completions)

    # Returns answer
    return answer

  # Deletes the conversation
  def delete_conversation(self, conversation_id):
    url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

    payload = json.dumps(f"{conversation_id}")
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Content-Length': '38',
        'Referer': 'https://claude.ai/chats',
        'Origin': 'https://claude.ai',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': f'{self.cookie}',
        'TE': 'trailers'
    }

    response = requests.delete( url, headers=headers, data=payload,impersonate="chrome110")

    # Returns True if deleted or False if any error in deleting
    if response.status_code == 204:
      return True
    else:
      return False

  # Returns all the messages in conversation
  def chat_conversation_history(self, conversation_id):
    url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations/{conversation_id}"

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://claude.ai/chats',
        'Content-Type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': f'{self.cookie}'
    }

    response = requests.get( url, headers=headers,impersonate="chrome110")
    

    # List all the conversations in JSON
    return response.json()

  def generate_uuid(self):
    random_uuid = uuid.uuid4()
    random_uuid_str = str(random_uuid)
    formatted_uuid = f"{random_uuid_str[0:8]}-{random_uuid_str[9:13]}-{random_uuid_str[14:18]}-{random_uuid_str[19:23]}-{random_uuid_str[24:]}"
    return formatted_uuid

  def create_new_chat(self):
    url = f"https://claude.ai/api/organizations/{self.organization_id}/chat_conversations"
    uuid = self.generate_uuid()

    payload = json.dumps({"uuid": uuid, "name": ""})
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://claude.ai/chats',
        'Content-Type': 'application/json',
        'Origin': 'https://claude.ai',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Cookie': self.cookie,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    response = requests.post( url, headers=headers, data=payload,impersonate="chrome110")

    # Returns JSON of the newly created conversation information
    return response.json()

  # Resets all the conversations
  def reset_all(self):
    conversations = self.list_all_conversations()

    for conversation in conversations:
      conversation_id = conversation['uuid']
      delete_id = self.delete_conversation(conversation_id)

    return True

  def upload_attachment(self, file_path):
    if file_path.endswith('.txt'):
      file_name = os.path.basename(file_path)
      file_size = os.path.getsize(file_path)
      file_type = "text/plain"
      with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

      return {
          "file_name": file_name,
          "file_type": file_type,
          "file_size": file_size,
          "extracted_content": file_content
      }
    url = 'https://claude.ai/api/convert_document'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://claude.ai/chats',
        'Origin': 'https://claude.ai',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': f'{self.cookie}',
        'TE': 'trailers'
    }

    file_name = os.path.basename(file_path)
    content_type = self.get_content_type(file_path)

    files = {
        'file': (file_name, open(file_path, 'rb'), content_type),
        'orgUuid': (None, self.organization_id)
    }

    response = req.post(url, headers=headers, files=files)
    if response.status_code == 200:
      return response.json()
    else:
      return False
      

    
  # Renames the chat conversation title
  def rename_chat(self, title, conversation_id):
    url = "https://claude.ai/api/rename_chat"

    payload = json.dumps({
        "organization_uuid": f"{self.organization_id}",
        "conversation_uuid": f"{conversation_id}",
        "title": f"{title}"
    })
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Referer': 'https://claude.ai/chats',
        'Origin': 'https://claude.ai',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': f'{self.cookie}',
        'TE': 'trailers'
    }

    response = requests.post(url, headers=headers, data=payload,impersonate="chrome110")

    if response.status_code == 200:
      return True
    else:
      return False


cookie_Str = "activitySessionId=0c8c75ea-a073-48b6-95b4-969f1375ab91; cf_clearance=V78J5v8nmNOBskl3y_umBGm6lt.rPGZVrllUnmJOHms-1723859049-1.2.1.1-2PIYcZ_NEEVelqfJqxD22jxGU5_LoUKRoqemdUrVyrLxd2GrDHhPOrCfkzBjk5Hj5bHGFGt83b8F7fNGY37OWqiBxtlRArReS.YrGWLLxvJMaSjLkSlbIX9x3uzb15c283uZKZy9WXUVZhbveMyj55dHjc.IQXWnO946vbRFbaxeh7ooj_JodAjfMh7HWZ0lbJQQFx6AeX.Cj0DT_ZeqlOrjq0V4o7qo_.kf8t8990yUeG4Q0nBLny7SMkujD1WV94SowlGuPFa6hkDvapa8fUck3MNecCF_aum14oKtJbdkOg9SJxTr_q_mY5R2zQRJBXTCHC9rYafFZ.6BljGLKyxIEHwItgYdh21JZmgUGPOKcrzaeXFJwr_HCbRHnsZ.; CH-prefers-color-scheme=dark; __ssid=1bd75327ecd321f07c822ff24801046; sessionKey=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; lastActiveOrg=72b4ea0b-4d3a-4820-b279-94004092fb03; intercom-device-id-lupk8zyo=2f5614b1-217f-4ce3-b1c5-c0c20d691e61; __cf_bm=977HpETfjaeLeJFN2W8ueJwe_xLB1a04EMvH09jDvs0-1723859946-1.0.1.1-TswUdQdDaERXHd0UwJojDVH25b.kGZDKo3yC9czqEgRCw6AwsoXErIPNG_8ysxzh6F5cNmW7IaAhfkV_TCGUjA; intercom-session-lupk8zyo=ekk2dU85dmFpaHhjdDBPZzA3bnJZT2tES25CZFM3Yld4TnYzSU40VnV6dCtRMEZMV0Y5M2ZReXJ3bklST2Vqdi0tK2Q1YTVzR0duOS9oTDVQNXpuaFRLQT09--3f6489d0c19e539805a5eec20a48b5265bcb593a"
cl = Client(cookie_Str)
prompt = "Hello, Claude!"
# conversation_id = "<conversation_id>" or claude_api.create_new_chat()['uuid']
response = cl.send_message(prompt, "<conversation_id>")
print(response)
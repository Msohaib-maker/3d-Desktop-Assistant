from chatModels.claude import *
from Screen_Vision_Module.interpret_screen import *
from Screen_Vision_Module.screen_capture import *



misinterpret_text = extract_text_from_image(capture_full_screen())


prompt = "Hi, I am sharing a misinterpret text which is translated using tesseract ocr from image. can you summarize it? Here the text : \n\n" + misinterpret_text


print(chat_with_claude(prompt))
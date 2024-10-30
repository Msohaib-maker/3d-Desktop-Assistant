from File_Upload_Module.extract_file import *
from chatModels.claude import *
import pytesseract

def analyze(content):
    
    prompt = "hey, I want to interpret the text I am going to give you. Here is the text : " + content
    return chat_with_claude(prompt=prompt)
     


def file_module(filename):

    _ , file_ext = os.path.splitext(filename)

    
    content = extract_file_contents(filename, file_ext=file_ext)


    if file_ext == ".jpg" or file_ext == ".png":
        image = Image.open(filename)
        image_text = pytesseract.image_to_string(image)
        
        return analyze(content=image_text)
    
    
    interpretation = analyze(content=content)
    return interpretation
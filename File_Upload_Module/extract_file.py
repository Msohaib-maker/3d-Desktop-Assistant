import csv
import pandas as pd
import PyPDF2
from PIL import Image
import os
import pytesseract
import pyautogui
import pygetwindow as gw

def extract_file_contents(filename,file_ext, pages=1):

    # Get the file extension
    
    
    if file_ext == ".txt":
        with open(filename, 'r') as file:
            content = file.read()
            return content

    elif file_ext == ".csv":
        reader = csv.reader(file)
        content = ''
        for row in reader:
            row_string = ','.join(row)  # Convert the list to a single string
            content += row_string + '\n'  # Add the row string to content with a newline

        return content
        # df = pd.read_csv('example.csv')
        # print(df.head())

    elif file_ext == ".pdf":
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page = 0
            page_content = ""
            while page < pages:
                page_text = reader.pages[page].extract_text()
                page += 1
                page_content += page_text
            
            return page_content


    elif file_ext == ".jpg" or file_ext == ".png":
        image = Image.open(filename)
        
        return image








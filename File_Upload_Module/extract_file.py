import csv
import pandas as pd
import PyPDF2
from PIL import Image
import os
import pytesseract
import pyautogui
import pygetwindow as gw

def extract_file_contents(filename):

    # Get the file extension
    _ , file_ext = os.path.splitext(filename)
    
    if file_ext == ".txt":
        with open(filename, 'r') as file:
            content = file.read()
            print(content)

    elif file_ext == ".csv":
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

        # df = pd.read_csv('example.csv')
        # print(df.head())

    elif file_ext == ".pdf":
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[0]
            print(page.extract_text())

    elif file_ext == ".jpg" or file_ext == ".png":
        image = Image.open(filename)
        image.show()







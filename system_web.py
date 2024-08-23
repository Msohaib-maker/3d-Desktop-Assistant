import speech_recognition as sr
import pyttsx3
import re
from speech_text import ChatInterface
from Web_Module.webQuery.wiki_search import *
from Web_Module.webQuery.duck_go_search import *
from chatModels.claude import *
from Web_Module.webQuery.google_search import *
from Web_Module.webQuery.youtube_search import *
from Web_Module.webQuery.twitter_search import *
from Web_Module.webQuery.latest_news_search import *

def extract_single_quoted_text(text):
    match = re.search(r"'(.*?)'", text)
    return match.group(1) if match else None

def check_search_source(response_first_line: str) -> str:
    match = re.search(r"'(.*?)'", response_first_line)
    return match.group(1) if match else "Neither"

def search_result(res, query):
    if res.lower() == "wikipedia":
        return Wiki_Search(query)
    if res.lower() == 'duck go':
        return Duck_Search(query)

def google_browsing(query):
    google_search(query)

def search_and_execute(query, result):
    if result.lower() == "google":
        google_search_and_open_first_link(query)
    elif result.lower() == "youtube":
        play_youtube_video(query)
    elif result.lower() == "twitter":
        open_twitter()
    elif result.lower() == "show latest news":
        get_latest_google_news(query)
    else:
        print(search_result(result,query=query))

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for your query...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"Voice input received: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""



def web_module(query):

    prompt = query + "\n\n Is the query above supposed to be wikipedia search, duck go search, google, youtube, or twitter? Answer with the appropriate name wrapped in single quotes."
    prompt1 = query + "\n Given text above. Can you extract and return only the part which is actual query to be searched?"

    platform = chat_with_claude(prompt)
    actual_query = chat_with_claude(prompt1)

    print(f"Platform: {platform}")
    print(f"Actual query: {actual_query}")

    platform = check_search_source(platform)

    search_and_execute(actual_query, platform)

    print("\n ***************************************** \n")
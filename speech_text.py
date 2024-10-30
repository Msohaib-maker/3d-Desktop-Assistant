import speech_recognition as sr
import pyttsx3
from voice_models.eleven_labs_model import *


class ChatInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()


    def get_voice_input(self):

        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for your query...")
            audio = self.recognizer.listen(source)
            try:
                query = self.recognizer.recognize_google(audio)
                print(f"Voice input received: {query}")
                return query
            except sr.UnknownValueError:
                print("Sorry, I did not understand the audio. Please try again.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""

    def text_to_speech(self, query):
        try:
            
            if query:
                try:
                    generate_voice(query)
                except:
                    bot_response = self.get_bot_response(query)
                    print(f"Chatbot: {bot_response}")

                    self.tts_engine.say(bot_response)
                    
                    self.tts_engine.runAndWait()

        except KeyboardInterrupt:
            print("\nReturning to menu...")

    def get_bot_response(self, user_query):
        # For testing, return the same input as the chatbot's response
        return user_query

# def main():
#     interface = ChatInterface()

#     while True:
#         print("\nMenu:")
#         print("1. Speech to Text")
#         print("2. Text to Speech")
#         print("3. Exit")
#         choice = input("Choose an option: ")

#         if choice == "1":
#             interface.speech_to_text()
#         elif choice == "2":
#             interface.text_to_speech()
#         elif choice == "3":
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "_main_":
    




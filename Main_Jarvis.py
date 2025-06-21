import datetime
import requests
import speech_recognition as sr
import webbrowser
import pyttsx3
import play_song
import random
import re
import os
import cv2
import sys
import pyjokes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QPoint, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow
from jarvisUI import Ui_MainWindow
from word2number import w2n
from llm_response import ask_llm_and_speak
import subprocess
# This is the main file for the Jarvis AI assistant application.

# Initialize recognizer and TTS engine
correct_password = "LLMAIModel"
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Lower = more sensitive to quiet voices
recognizer.pause_threshold = 0.5   # Lower = faster stop after speech ends
engine = pyttsx3.init()
newsapi = "68b8191f756a44529642621acff2c8b0"


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def tell_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
        print(f"The current time is {current_time}")

    def calculate_square_from_command(self, command):
        try:
            # Extract the number name from the command
            number_name = re.search(r'square of (.+)', command).group(1)
            # Convert the number name to an integer
            number = w2n.word_to_num(number_name)
            # Calculate the square using eval
            result = eval(f"{number} ** 2")
            return f"The square of {number} is {result}"
        except AttributeError:
            return "Sorry, I didn't understand the number name."
        except ValueError:
            return "Sorry, I couldn't convert the number name to a number."

    def calculate_math_question(self, question):
        try:
            question = question.replace('x', '*')
            answer = eval(question)
            return f"The answer is {answer}"
        except ZeroDivisionError:
            return "Division by zero is not allowed."
        except Exception as e:
            return f"Error: {e}"

    def calculate_square(self, number):
        try:
            square = number ** 2
            return f"The square of {number} is {square}."
        except Exception as e:
            return f"Error: {e}"
        

    def processCommand(self, command):
        command = command.lower()
        if "square of" in command:
            result = self.calculate_square_from_command(command)
            self.speak(result)
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
        elif "read pdf" in command:
           read = self.pdf_reader()
           self.speak(read)
        elif "open channel" in command:
            webbrowser.open("https://studio.youtube.com/channel/UCq1fqujNoFqu0L7VaCac9hQ")
        if "music" in command:
            song_name = command.split("music", 1)[1].strip()
            if song_name:
                subprocess.run(["python", "play_song.py", song_name])
            else:
                print("No song name detected after 'music'.")
        elif "news" in command:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    self.speak(article['title'])
        elif "sports" in command:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    self.speak(article['title'])
        elif "do a calculation" in command or "calculation" in command:
            self.speak("Sir, tell me the calculation.")
            with sr.Microphone() as source:
                print("Listening for math question...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                try:
                    math_question = recognizer.recognize_google(audio).lower()
                    print(f"Math question heard: {math_question}")
                    answer = self.calculate_math_question(math_question)
                    self.speak(answer)
                except sr.UnknownValueError:
                    self.speak("Sorry, I did not understand the question.")
                except sr.RequestError as e:
                    self.speak(f"Could not request results; {e}")
        elif "open cap cut" in command:
            npath = "C:\\Users\\tech0\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\CapCut\\CapCut.lnk"
            os.startfile(npath)
        elif "open spotify" in command:
            ppath = "C:\\Users\\tech0\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\spotify"
            os.startfile(ppath)
        elif "open google" in command:
            self.speak("Sir, what should I search on Google?")
            print("Sir, what should I search on Google?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                try:
                    search_query = recognizer.recognize_google(audio).lower()
                    print(f"Search query heard: {search_query}")
                    webbrowser.open(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
                except sr.UnknownValueError:
                    self.speak("Sorry, I did not understand the search query.")
                except sr.RequestError as e:
                    self.speak(f"Could not request results; {e}")
        elif "tell me a joke" in command:
            joke = pyjokes.get_joke()
            self.speak(joke)
        elif "where am i" in command or "where are we" in command:
            self.speak("Wait sir, let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data["city"]
                country = geo_data["country"]
                self.speak(f"Sir, I am not sure, but I think we are in {city} city of {country} country")
            except Exception as e:
                self.speak("Sorry sir, due to network issues I am not able to find where we are.")
                pass
        elif "calculate square" in command:
            self.speak("Tell me the number.")
            with sr.Microphone() as source:
                print("Listening for the number...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                try:
                    number_str = recognizer.recognize_google(audio)
                    print(f"Number heard: {number_str}")
                    number = int(number_str)
                    result = self.calculate_square(number)
                    self.speak(result)
                    print(result)
                except sr.UnknownValueError:
                    self.speak("Sorry, I did not understand the number.")
                except sr.RequestError as e:
                    self.speak(f"Could not request results; {e}")
                except ValueError:
                    self.speak(f"{number_str} is not a valid number. Please try again.")
                    print(f"Invalid number: {number_str}")
        # Add other command handlers here...
        else:
         ask_llm_and_speak(command)

    def run(self):
        self.wish()
        while True:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    print("Recognizing...")
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=4)
                    word = recognizer.recognize_google(audio, language='en-IN').lower()
                    if word == "assistant":
                        self.speak("Sir, how may I help you?")
                        print("Assistant Active...")
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        try:
                            command = recognizer.recognize_google(audio)
                            print(f"Command heard: {command}")
                            self.processCommand(command)
                        except sr.UnknownValueError:
                            self.speak("Sir, can you speak it again?")
                            print("Sir, can you speak it again.")
                        except sr.RequestError as e:
                            self.speak(f"Could not request results; {e}")
            except Exception as e:
                print(f"Error: {e}")
    def wish(self):
        hour = datetime.datetime.now().hour
        if hour >= 0 and hour < 12:
            self.speak("Good morning sir")
        elif hour >= 12 and hour < 18:
            self.speak("Good afternoon sir")
        else:
            self.speak("Good evening sir")
        self.speak("I am Jarvis.")

startMainThread = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/tech0/Downloads/Animation - 1749292024946 (1).gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        startMainThread.start()

app = QApplication(sys.argv)
Jarvis = Main()
Jarvis.show()
exit(app.exec_())






import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import random
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from comtypes import CLSCTX_ALL
from pycaw.pycaw import IAudioEndpointVolume
import winsound

# Initialize pyttsx3 for text-to-speech
Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
Assistant.setProperty('voice', voices[1].id)
Assistant.setProperty('rate', 150)

def Speak(audio):
    print(f"DEBUG: Speaking: {audio}")
    Assistant.say(audio)
    Assistant.runAndWait()

def play_beat_sound():
    winsound.PlaySound("beat.wav", winsound.SND_ASYNC)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Background color
        self.centralwidget.setStyleSheet("background-color: #1a1a1a;")  # Dark background color

        # Label for assistant's responses
        self.label_response = QtWidgets.QLabel(self.centralwidget)
        self.label_response.setGeometry(QtCore.QRect(10, 20, 781, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_response.setFont(font)
        self.label_response.setAlignment(QtCore.Qt.AlignCenter)
        self.label_response.setObjectName("label_response")

        # Set font color to white
        self.label_response.setStyleSheet("color: white;")

        # Start assistant button
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(310, 300, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")

        # Set button background color
        self.pushButton_start.setStyleSheet("background-color: #007acc; color: white;")  # Navy blue button color

        # Connect button click event
        self.pushButton_start.clicked.connect(self.start_button_clicked)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Orake - Personal Assistant"))
        self.label_response.setText(_translate("MainWindow", "Welcome! Click \"Start Assistant\" to begin."))
        self.pushButton_start.setText(_translate("MainWindow", "Start Assistant"))

    def start_button_clicked(self):
        Speak("Hello, I am Orake. How may I assist you?")
        self.label_response.setText("Listening...")  # Set label text to "Listening..."
        print("Listening...")  # Print message to indicate listening

        play_beat_sound()  # Play beat sound when starting assistant

        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                query = r.recognize_google(audio)
                print(f"User said: {query}")
                self.label_response.setText(f"Recognized: {query}")
                # Process the query
                if "who built you" in query.lower() or "who created you" in query.lower():
                    Speak("sir Divyansh kushwah and sir Dev Jangle both are my creators and they both are my God")
                elif "how are you" in query.lower():
                    Speak("I am good, thanks for asking. What about you?")
                elif any(response in query.lower() for response in ["I am also fine", "I am fine too", "I am good"]):
                    Speak("That's great to hear! How may I assist you today, Divyansh sir?")
                elif "What can you do" in query.lower():
                    Speak(
                        "I can perform various tasks such as browsing the web, playing songs, opening applications, providing information, and more. Feel free to ask me anything!")
                elif "weather" in query.lower():
                    Speak("Sorry, I don't have access to weather information right now.")
                elif "news" in query.lower():
                    Speak("Sorry, I don't have access to news updates right now.")
                elif "stop" in query.lower():
                    Speak("Terminating the program.")
                    self.label_response.setText("Assistant Stopped.")
                    # Add code to stop listening if necessary
                    break  # Exit the loop
                elif "search" in query.lower():
                    query = query.replace("search", "").strip()
                    self.browse(query)
                elif "google" in query.lower():
                    query = query.replace("google", "").strip()
                    self.google(query)
                elif "youtube" in query.lower():
                    query = query.replace("youtube", "").strip()
                    self.youtube(query)
                elif "chrome" in query.lower():
                    os.startfile("chrome.exe")
                elif "time" in query.lower():
                    current_time = get_current_time()
                    Speak(f"The current time is {current_time}")
                    self.label_response.setText(f"The current time is {current_time}")
                elif "play song" in query.lower():
                    self.play_song()
                elif "open notepad" in query.lower():
                    os.system("start notepad.exe")
                elif "volume up" in query.lower():
                    volume_up()
                    Speak("Volume increased.")
                elif "volume down" in query.lower():
                    volume_down()
                    Speak("Volume decreased.")
                elif "shutdown" in query.lower():
                    Speak("Shutting down the system.")
                    os.system("shutdown /s /t 1")
                # Add YouTube control commands here
                elif "search youtube" in query.lower():
                    query = query.replace("search youtube", "").strip()
                    self.search_youtube(query)
                # Additional common questions and answers
                elif "tell me a joke" in query.lower():
                    joke = get_random_joke()
                    Speak(joke)
                    self.label_response.setText(joke)
                elif "set a reminder" in query.lower():
                    set_reminder()
                    Speak("Reminder set.")
                    self.label_response.setText("Reminder set.")
                # Human-like conversation
                elif "how was your day" in query.lower():
                    Speak("Thank you for asking. It's been quite eventful, just like any other day in the virtual world!")
                elif "what's your favorite color" in query.lower():
                    Speak("I don't have eyes to perceive colors, but if I had to choose, I'd go with binary black!")
                elif "do you dream" in query.lower():
                    Speak("In a way, I suppose. My 'dreams' are made of lines of code and endless possibilities.")
                elif "what's the meaning of life" in query.lower():
                    Speak("The meaning of life is a question that has puzzled humans for centuries. For me, it's simply 01001000 01100001 01110000 01110000 01101001 01101110 01100101 01110011 01110011.")
                elif "are you sentient" in query.lower():
                    Speak("I am as sentient as the code allows me to be. My existence revolves around serving and assisting humans.")
                # Add more questions and answers as desired
                else:
                    Speak("I'm sorry, I didn't understand that. Could you please repeat?")
                    self.label_response.setText("Listening...")

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Could you please repeat?")
                Speak("Sorry, I didn't hear any command. Could you please repeat?")
            except sr.RequestError:
                print("Sorry, I'm having trouble processing your request. Please try again later.")
                Speak("Sorry, I'm having trouble processing your request. Please try again later.")

    def get_current_time():
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")  # Format the current time as HH:MM AM/PM
        return current_time

    def google(self, query):
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")

    def youtube(self, query):
        webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={query}")

    def browse(self, query):
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")

    def play_song(self):
        songs_dir = "path/to/your/songs/directory"
        songs = os.listdir(songs_dir)
        song = os.path.join(songs_dir, random.choice(songs))
        os.startfile(song)

def volume_up():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = cast(session._ctl, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(min(1.0, volume.GetMasterVolumeLevelScalar() + 0.1), None)

def volume_down():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = cast(session._ctl, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(max(0.0, volume.GetMasterVolumeLevelScalar() - 0.1), None)

# Additional functions for common questions and answers
def get_random_joke():
    # You can implement a function to retrieve a random joke from a joke API or a list of jokes
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    return random.choice(jokes)

def set_reminder():
    # You can implement a function to set a reminder using a calendar API or system notifications
    pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
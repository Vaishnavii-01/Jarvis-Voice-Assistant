import pyttsx3 
import datetime
import speech_recognition as sr
import webbrowser as wb
import pywhatkit
import pyjokes
import pyautogui
import pygame
import os
import random

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        say("Good Morning!")
    elif hour >=12 and hour < 18:
        say("Good Afternoon!")
    elif hour >=18 and hour < 24:
        say("Good Evening!")
    else:
        say("Good Night!")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception:
            return "Some Error Occurred. Sorry from Jarvis"

def takeScreenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot_{timestamp}.png")
    say("Screenshot saved")

pygame.mixer.init()

def get_music_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav', '.ogg'))]

def play_random_music():
    music_folder = os.path.join(os.environ['HOMEPATH'], 'Music')
    if os.path.exists(music_folder):
        music_files = get_music_files(music_folder)
        if music_files:
            chosen_music = os.path.join(music_folder, random.choice(music_files))
            pygame.mixer.music.load(chosen_music)
            pygame.mixer.music.play()
            say("Playing Music")
        else:
            say("No music files found in the Music folder.")
    else:
        say("Music folder not found.")

music_playing = False

def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        say("Music Stopped")
    else:
        play_random_music()
    music_playing = not music_playing

if __name__ == '__main__':
    say("I am JARVIS, your Virtual Artificial Intelligence")
    greeting()
    say("JARVIS at your service, please tell me how can I help you?")
   
    while True:
        query = takeCommand().lower()

        if 'remember' in query:
            say("What do you want me to remember?")
            data = takeCommand()
            say("You told me to remember that " + data)
            with open('data.txt', 'a') as remember:
                remember.write(data + '\n')

        elif 'know anything' in query:
            with open('data.txt', 'r') as remember:
                say("You told me to remember that " + remember.read())

        elif 'camera' in query:
            wb.open('microsoft.windows.camera:')

        elif 'youtube' in query:
            say("What should I search on YouTube?")
            topic = takeCommand()
            pywhatkit.playonyt(topic)

        elif 'search' in query:
            say("What should I search on Google?")
            search = takeCommand()
            wb.open('https://www.google.com/search?q=' + search)

        elif 'instagram' in query:
            say("Opening Instagram")
            wb.open('https://www.instagram.com')

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            say(joke)
            print(joke)

        elif 'screenshot' in query:
            takeScreenshot()

        elif 'music' in query:
            toggle_music()

        elif 'offline' in query or 'bye' in query:
            say("Thank you! Goodbye")
            quit()
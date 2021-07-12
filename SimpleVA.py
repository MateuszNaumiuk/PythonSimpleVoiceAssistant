import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests

engine = pyttsx3.init()
engine.setProperty("rate", 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
    
def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=8 and hour<20:
        speak("Dzień dobry")
        print("Dzień dobry")
    else:
        speak("Dobry wieczór")
        print("Dobry wieczór")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='pl-pl')
            print(f"Uzytkownik powiedział:{statement}\n")

        except Exception as e:
            speak("Nie zrozumiałem, powtórz")
            return "None"
        return statement

print("Ładowanie asystenta głosowego")
speak("Ładowanie")
wishMe()

#Głowna petla
if __name__=='__main__':
    while True:
        speak("Jak ci moge pomóc?")
        statement = takeCommand().lower()
        if statement==0:
            continue
        if "wyłącz" in statement or "wyjdź" in statement:
            speak('Wyłaczam się')
            print('koniec')
            break

        if 'wikipedia' in statement:
            speak('Przeszukiwanie wikipedii')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("Nawiazując do wikipedii...")
            print(results)
            speak(results)

        elif 'otwórz youtube' in statement or "youtube" in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Otwieram Youtube")
            time.sleep(5)

        elif 'otwórz google' in statement or "google" in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Otwieram Google")
            time.sleep(5)

        elif 'otwórz gmail' in statement or "gmail" in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Otwieram gmail")
            time.sleep(5)

        elif 'ktora jest godzina' in statement or "godzina" in statement:
            strTime=datetime.datetime.now().strftime("%H:%M")
            speak(f"Jest godzina {strTime}")

        elif 'wyszukaj w internecie' in statement or "wyszukaj" in statement:
            statement = statement.replace("wyszukaj w internecie", "") or statement.replace("wyszukaj", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)
            
        elif "pogoda" in statement:
            api_key="API KEY"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("W jakim miescie wyszukac pogode?")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperatura wynosi... " +
                      str(current_temperature) +
                      "\n Wilgotnosc powietrza wynosi " +
                      str(current_humidiy) +
                      "\n Dodatkowy opis:  " +
                      str(weather_description))
                print(" Temperatura wynosi... " +
                      str(current_temperature) +
                      "\n Wilgotnosc powietrza wynosi " +
                      str(current_humidiy) +
                      "\n Dodatkowy opis:  " +
                      str(weather_description))
            elif "wyloguj" in statement:
                speak("Zostaniesz wylogowany")
                subprocess.call(["shutdown", "/l"])
			
time.sleep(3)

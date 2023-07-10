import os
import pyttsx3  # to convert text to speech
import datetime  # to get date and time
import speech_recognition as sr  # to recognize voice
import wikipedia  # to search on wikipedia
import webbrowser  # to open websites directly
import random
import pyjokes
import requests
from bs4 import BeautifulSoup
import subprocess
from twilio.rest import Client
import wolframalpha
import pyaudio


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
# print(voices)
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def note(text):
    date=datetime.datetime.now()
    file_name=str(date).replace(":","-")+"-note.txt"
    with open(file_name, 'w') as f:
        f.write(text)
    subprocess.Popen(["notepad.exe",file_name])

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning  !")
        speak("Good Morning  !")

    elif hour >= 12 and hour < 18:
        print("Good Afternoon  !")
        speak("Good Afternoon  !")

    else:
        print("Good Evening  !")
        speak("Good Evening!")

    speak("Hi! I am Jarvis.. , What can I do for you...? ")
    print("Hi! I am Jarvis.. , What can I do for you...? ")


def takeCommand():
    # It takes mic input from user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User : {query}\n")

    except Exception as e:
        # print(e) commented this out to hide errors on the console or terminal.
        speak("Say that again please...")
        print("Say that again please...")
        return "None"

    return query


if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()

        if 'information' in query:
            speak('Yes sure.... ,  Information about which topic...? ')
            print('Yes sure.... ,  Information about which topic...? ')

            query = takeCommand().lower()
            results = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia")
            print("According to wikipedia : ")

            try:
                print(results)
                speak(results)
            except Exception as e:
                speak(results)

        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia..")
            print("According to wikipedia : ")
            try:
                print(results)
                speak(results)
            except Exception as e:
                speak(results)
        
        elif 'open youtube' in query:
            speak("Opening YouTube...")
            print("Opening YouTube...")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google...")
            print("Opening Google...")
            webbrowser.open("google.com")

        elif 'open a k g' in query or 'open a kg' in query:
            print("Opening AKGEC Website...")
            speak("Opening A K G E C Website...")
            webbrowser.open("https://www.akgec.ac.in/")

        elif 'open stack overflow' in query:
            speak("Opening Stack overflow...")
            print("Opening Stack overflow...")
            webbrowser.open("stackoverflow.com")

        elif 'search' in query and 'youtube' in query:
            r=query.replace('search','').replace('youtube','').replace(' on ','').lstrip().rstrip()
            search=r.replace(' ','+')
            url=f"https://www.youtube.com/results?search_query={search}"
            speak(f"Searching {r} on youtube...")
            print(f"Searching {r} on youtube...")
            webbrowser.open(url)

        elif 'search' in query and 'google' in query:
            r=query.replace('search','').replace('google','').replace(' on ','').lstrip().rstrip()
            search=r.replace(' ','+')
            url=f"https://www.google.com/search?q={search}"
            speak(f"Searching {r} on Google...")
            print(f"Searching {r} on Google...")
            webbrowser.open(url)

        elif ('temperature' in query or 'weather' in query):
            i=query.split().index("in")
            city="".join(query.split()[i+1:])
            search=f"temperature in {city}"
            url=f"https://www.google.com/search?q={search}"
            r= requests.get(url)
            data=BeautifulSoup(r.text,"html.parser")
            temp= data.find("div", class_="BNeawe").text
            speak(f"Current {search} is {temp}")
            print(f"Current {search} is {temp}")

        elif 'joke' in query:
            joke=pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'send message' in query or 'send a message' in query:
            acc_sid='AC74ed4c8183f3cf36c3ea6943f9705197'
            auth_token='609946575f1557e524ca6729f6f1f681'
            client =Client(acc_sid,auth_token)
            speak("What should I send?")
            print("What should I send?")
            message=client.messages.create(body=takeCommand(),from_='+18595358964',to='+919871694139')
            print('Message sent successfully')
            speak('Message sent successfully')

        elif 'play music' in query:
            music_dir=r'C:\Users\91958\Desktop\Shubhs\Projects\Music Player'
            songs=os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,random.choice(songs)))
        
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Mam , The time is {strTime}")
            print(f"Mam , The time is {strTime}")

        elif 'how are' in query and 'you' in query:
            print("I am absolutely fine mam ! , what can i do for you ??")
            speak("I am absolutely fine mam ! , what can i do for you ??")

        elif 'who are you' in query:
            intro="Hello! I am Jarvis. I am your virtual assisstant and I'm here to make your life easier."
            speak(intro)
            print(intro)
            
        elif 'calculate' in query:
            app_id='T2RPQL-86EJH4JT9A'
            client=wolframalpha.Client(app_id)
            i=query.split().index("calculate")
            query=query.split()[i+1:]
            res=client.query(" ".join(query))
            ans=next(res.results).text
            print(f"The answer is {ans}")
            speak(f"The answer is {ans}")

        elif 'what is' in query or 'who is' in query or 'how are' in query or 'what are' in query or 'who are' in query:
            query=query.replace('are','is')
            app_id='T2RPQL-86EJH4JT9A'
            client=wolframalpha.Client(app_id)
            i=query.split().index("is")
            query=query.split()[i+1:]
            res=client.query(" ".join(query))
            ans=next(res.results).text
            print(f"The answer is {ans}")
            speak(f"The answer is {ans}")

        elif ('open powerpoint' in query or 'open ms powerpoint' in query):
            pptPath=r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft PowerPoint 2010.lnk"
            speak('Opening Powerpoint...')
            print('Opening Powerpoint...')
            os.startfile(pptPath)

        elif ('open excel' in query or 'open ms excel' in query):
            excelPath=r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Excel 2010.lnk"
            speak('Opening MS Excel...')
            print('Opening MS Excel...')
            os.startfile(excelPath)

        elif 'open spotify' in query:
           spotPath=r"C:\Users\91958\AppData\Local\Microsoft\WindowsApps\Spotify.exe"
           speak('Opening Spotify...')
           print('Opening Spotify...')
           os.startfile(spotPath)

        elif 'open code' in query:
            codePath=r"C:\Users\91958\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
            speak("Opening Code...")
            print("Opening Code...")
            os.startfile(codePath)


        elif ('open word' in query or 'open ms word' in query):
            wordPath=r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk"
            speak('Opening MS Word...')
            print('Opening MS Word...')
            os.startfile(wordPath)

        elif 'open chrome' in query:
            chromePath=r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk"
            speak('Opening Chrome...')
            print('Opening Chrome...')
            os.startfile(chromePath)

        elif ('make' in query and 'note' in query) :
            speak("What would you like to write?")
            print("What would you like to write?")
            note_text=takeCommand()
            speak("I have made a note of that")
            print("I have made a note of that")
            note(note_text)

        elif 'where is' in query:
            i=query.split().index("is")
            location="".join(query.split()[i+1:])
            url=f"https://google.com/maps/place/{location}"
            speak(f'Opening {location} on Google Maps...')
            print(f'Opening {location} on Google Maps...')
            webbrowser.open(url)

        elif 'listen to' in query:
            speak("Yes? What is going on in your mind?")
            print("Yes? What is going on in your mind?")
            query=takeCommand().lower()
            if 'demotivated' in query:
                speak("Imagine where you would be next year if you start now. C'mon! You can do it!")
                print("Imagine where you would be next year if you start now. C'mon! You can do it!")

            elif ('tired' in query or 'had a long day' in query):
                speak('You should take a break and have a kit kat!')
                print('You should take a break and have a kit kat!')

            elif 'anxiety' in query:
                speak('Take deep breaths and drink some water')
                print('Take deep breaths and drink some water')

            elif ('feeling low' in query or 'not feeling well' in query):
                speak('You should try talking to a loved one and also get some sleep')
                print('You should try talking to a loved one and also get some sleep')

        elif 'quit' in query:
            speak('BYE BYE ...')
            print('BYE BYE ...')
            break
        
        elif 'stop' in query:
            speak('Sayonara... have a great day ahead..')
            print('Sayonara... have a great day ahead..')
            break

        elif 'exit' in query:
            speak('Signing off... have a great day ahead..')
            print('Signing off... have a great day ahead..')
            break

        else:
            speak("Say it again please...")

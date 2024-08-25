import speech_recognition as sr 
import webbrowser
import pyttsx3
import musicLibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# News API Key
newsapi= "2961598a214e48acaabcf410245267b1"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the library.")
    elif "news" in c.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        r = requests.get(url)
        # Check if the request was successful
        if r.status_code == 200:
            # Parse the JSON response
            headlines = r.json()
            
            # Read the headlines out loud
            for article in headlines['articles']:
                speak(article['title'])
        
        
        
        else:
            speak("Sorry, I couldn't fetch the news.")

if __name__ == "__main__": 
    speak("Initializing Assistant.......")
    while True:
        # Listen for the wake word "Assistant"
        # obtain audio from the microphone

        r = sr.Recognizer()
        
        print("recognizing....")

        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=4, phrase_time_limit=3)
            
            word = r.recognize_google(audio)
            print(f"Recognized word: {word}")  # Debug statement

            if word.lower() == "assistant":
                speak("Yes")
                # Listen for command       
                with sr.Microphone() as source:
                    print("Assistant Active...")
                    audio = r.listen(source) 
                    command = r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error; {e}")

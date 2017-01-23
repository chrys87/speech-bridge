#!/usr/bin/env python3

# TODO needs try except ( check for installation)
import speech_recognition as sr

class Driver():
    def __init__(self):
        self.SpeechRecognizer = sr.Recognizer()
        self.audio = None
    def listenToMicro(self):        
        with sr.Microphone() as source:
            print("Say something!")
            self.audio = self.SpeechRecognizer.listen(source)
    def recognizeSpeech(self):
        # recognize speech using Google Speech Recognition
        text = ''
        try:
            text = self.SpeechRecognizer.recognize_google(self.audio)
            print('Google Speech Recognition Done')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return text

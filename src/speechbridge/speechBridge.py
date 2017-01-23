#!/usr/bin/env python3

from recognitionDriver import GoogleSpeechRecognition

class speechBridge():
    def __init__(self):
        self.env = {}
        self.env['running'] = True
        self.env['recognitionDriver'] = GoogleSpeechRecognition.Driver()
    def proceed(self):
        while self.env['running']:
            self.env['recognitionDriver'].listenToMicro()
            text = self.env['recognitionDriver'].recognizeSpeech()
            if text.upper() == 'EXIT':
                self.env['running'] = False
            else:
                print(text)


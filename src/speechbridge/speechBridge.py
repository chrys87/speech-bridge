#!/usr/bin/env python3

from recognitionDriver import GoogleSpeechRecognition
from core import environment
from core import settingsManager

class speechBridge():
    def __init__(self):
        self.env = environment.environment
        self.env['runtime']['recognitionDriver'] = GoogleSpeechRecognition.Driver()
    def proceed(self):
        while self.env['general']['running']:
            self.env['runtime']['recognitionDriver'].listenToMicro()
            text = self.env['runtime']['recognitionDriver'].recognizeSpeech()
            if text.upper() == 'EXIT':
                self.env['general']['running'] = False
                print('stop')
            else:
                print(text)


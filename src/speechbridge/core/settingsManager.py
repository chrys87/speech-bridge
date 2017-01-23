#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import importlib.util
import os
import __main__
from configparser import ConfigParser
from core import environment 
from core import inputEvent 
from core.settings import settings
from core import debug

class settingsManager():
    def __init__(self):
        self.settings = settings
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def loadSettings(self, settingConfigPath):
        if not os.path.exists(settingConfigPath):
            return False
        self.env['settings'] = ConfigParser()
        self.env['settings'].read(settingConfigPath)
        return True

    def setSetting(self, section, setting, value):
        self.env['settings'].set(section, setting, value)

    def getSetting(self, section, setting):
        value = ''
        try:
            value = self.env['settings'].get(section, setting)
        except:
            value = str(self.settings[section][setting])
        return value

    def getSettingAsInt(self, section, setting):
        value = 0
        try:
            value = self.env['settings'].getint(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsFloat(self, section, setting):
        value = 0.0
        try:
            value = self.env['settings'].getfloat(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsBool(self, section, setting):
        value = False
        try:
            value = self.env['settings'].getboolean(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def loadDriver(self, driverName, driverType):
        try:
            if self.env['runtime'][driverType] != None:
                self.env['runtime'][driverType].shutdown(self.env)    
            spec = importlib.util.spec_from_file_location(driverName, os.path.dirname(os.path.realpath(__main__.__file__)) + "/" + driverType + '/' + driverName + '.py')
            driver_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(driver_mod)
            self.env['runtime'][driverType] = driver_mod.driver()
            self.env['runtime'][driverType].initialize(self.env)
            self.env['runtime']['debug'].writeDebugOut('Loading Driver '  + driverType +" OK",debug.debugLevel.INFO, onAnyLevel=True)             
        except Exception as e:
            self.env['runtime'][driverType] = None
            self.env['runtime']['debug'].writeDebugOut("Loading " + driverType + " Driver : "+ str(e), debug.debugLevel.ERROR)
    
    def shutdownDriver(self, driverType):
        if self.env['runtime'][driverType] == None:
            return
        self.env['runtime'][driverType].shutdown()
        del self.env['runtime'][driverType]          
      
    def initSpeechBridgeConfig(self, environment = environment.environment, settingsRoot = '/etc/speechBridge/', settingsFile='settings.conf'):
        environment['runtime']['debug'] = debug.debug()
        environment['runtime']['debug'].initialize(environment)
        if not os.path.exists(settingsRoot):
            if os.path.exists(os.path.dirname(os.path.realpath(__main__.__file__)) +'/../../config/'):
                settingsRoot = os.path.dirname(os.path.realpath(__main__.__file__)) +'/../../config/'
            else:
                return None

        environment['runtime']['settingsManager'] = self 
        environment['runtime']['settingsManager'].initialize(environment)

        validConfig = environment['runtime']['settingsManager'].loadSettings(settingsRoot + '/settings/' + settingsFile)
        if not validConfig:
            return None

            
        environment['runtime']['debug'].writeDebugOut('\/-------environment-------\/',debug.debugLevel.INFO, onAnyLevel=True)        
        environment['runtime']['debug'].writeDebugOut(str(environment),debug.debugLevel.INFO, onAnyLevel=True)
        environment['runtime']['debug'].writeDebugOut('\/-------settings.conf-------\/',debug.debugLevel.INFO, onAnyLevel=True)        
        environment['runtime']['debug'].writeDebugOut(str(environment['settings']._sections
),debug.debugLevel.INFO, onAnyLevel=True)        
        return environment
     

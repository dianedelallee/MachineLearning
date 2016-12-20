import configparser
import os

class HelperConfig(object):

    def get_config(file):
        config = configparser.ConfigParser()
        myPath=os.path.dirname(os.path.dirname(file))
        myFile=myPath+'\\config.ini'
        config.read(myFile)
        return config

    
    def get_config_personalize(filePath, nameFile):
        config = configparser.ConfigParser()
        myPath=filePath
        myFile=myPath+'\\'+nameFile
        config.read(myFile)
        return config



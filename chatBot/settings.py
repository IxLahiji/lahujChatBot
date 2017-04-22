import os.path
import sys
import time
from .json_ops import JSONReaderWriter


class JSONSettings:


    def __init__(self, program_path, default_settings):
        #create settings reader, and check to make sure it exists
        self.settings = JSONReaderWriter(program_path + os.path.sep + 'settings.JSON')
        self.settings_chk(default_settings)
        #read settings in loaded json file
        try:
            self.parsed_settings = self.settings.read()
        except:
            print ("Error: Invalid settings file. Please either fix or delete the JSON file!")
            time.sleep(3)
            sys.exit()


    def settings_chk(self, default_settings):
        import json
        #Generate settings json if not present
        if not self.settings.exists():
            print("No settings file found. Generating a new settings JSON file...")
            self.settings.write(default_settings)
            
            print("The settings file has been generated. Please add a token for your discord bot before the next execution.")
            time.sleep(3)
            sys.exit()

            
    def get_setting(self, setting):
        #Check to make sure requested item is present
        if (not (setting in self.parsed_settings)):
            print ("Error: Invalid settings file. Please either fix or delete the JSON file!")
            time.sleep(3)
            sys.exit()
        else:
            return self.parsed_settings[setting]

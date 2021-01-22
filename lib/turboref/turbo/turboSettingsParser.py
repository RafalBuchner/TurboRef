from pathlib import Path
import os
from configparser import ConfigParser


HOME = str(Path.home())
TURBO_DIR = os.path.join(HOME,"Documents","turboSettings")
CONFIG_FILE = "config.ini"
FALLBACK_SETTINGS = dict(
        # backgroundColor=(.1,.1,.1,1)
        backgroundColor=(1,0,0,1),
        scrollMargin=20000
    )



def colorFloatsToRGBA(color):
    r,g,b,a = color
    return r*255, g*255, b*255, a*255


def trPath(fileNameOrRelPath):
    return os.path.join(TURBO_DIR, fileNameOrRelPath)


class TurboSettingsParser(object):
    def __init__(self):
        # internal attrs
        self.configparser = ConfigParser()
        self._configObjLoaded = False
        pass
        self.initializeTurboSetup()


    def initializeTurboSetup(self):
        if not os.path.exists(TURBO_DIR):
            os.mkdir(TURBO_DIR)
        self.load()

    # ------------------------------
    # Public Methods
    # ------------------------------

    def save(self):
        self.__save()


    def load(self):
        self.__load()

    # ------------------------------
    # Private Methods
    # ------------------------------

    def __save(self):
        if not self._configObjLoaded:
            self.load()

        with open(trPath(CONFIG_FILE), 'w') as conf:
            self.configparser.write(conf)

    def __load(self):
        if not os.path.exists(trPath(CONFIG_FILE)):
            with open(trPath(CONFIG_FILE), 'w') as conf:
                self.resetToDefault()
                self.configparser.write(conf)
        else:
            self.configparser.read(trPath(CONFIG_FILE))
        self._configObjLoaded = True

    def resetToDefault(self):
        self.configparser["TURBO_GLOBALS"] = FALLBACK_SETTINGS

    def getSetting(self, settingName):
        setting = self.configparser["TURBO_GLOBALS"].get(settingName)
        if setting is None:
            setting = FALLBACK_SETTINGS.get(settingName)
        return setting






if __name__ == '__main__':
    trs = TurboSettingsParser()
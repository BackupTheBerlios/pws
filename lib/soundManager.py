import os, time, sys
import wx
from lib.util import JOWST_PATH

class DummyWxWave:
    def __init__(self, filepath): pass
    def Play(self, async=1): pass


class SoundManager:
    def __init__(self):            
        self._buildSoundDict()
        self.noPlay = []

    def hasSound(self, soundkey):
        return self.soundDict.has_key(soundkey)

    def registerSound(self, soundkey, filename):
        if sys.platform in ['linux', 'linux2']:
            sndObj = DummyWxWave
        else:
            sndObj = wx.Sound

        resPath = os.path.join(JOWST_PATH, "resources")
        resPath = os.path.normpath(resPath)

        self.soundDict[soundkey] = sndObj(os.path.join(resPath, filename))
        
    def enableSound(self, soundon=True):
        if soundon:
            self.noPlay = []
        else:
            self.noPlay = self.soundDict.keys()
            self.noPlay.sort()

    def enableMatchSounds(self, soundon=True):
        sounds = self.soundDict.keys()
        sounds.remove("ROLL_DICE")
        if not soundon:
            for sound in sounds: 
                self.noPlay.append(sound)
            self.noPlay.sort()
        else:
            for sound in sounds:
                self.noPlay.remove(sound)

    def enableDiceSound(self, soundon=True):
        if not soundon:
            self.noPlay.append("ROLL_DICE")
            self.noPlay.sort()
        else:
            self.noPlay.remove("ROLL_DICE")
            
    def playSound(self, soundname, async=True, delay=0):        
        if soundname not in self.noPlay:
            self.soundDict[soundname].Play(async)
            if delay: time.sleep(delay)

    def _buildSoundDict(self):
        if sys.platform in ['linux', 'linux2']:
            sndObj = DummyWxWave
        else:
            sndObj = wx.Sound

        resPath = os.path.join(JOWST_PATH, "resources")
        resPath = os.path.normpath(resPath)
                               
        self.soundDict = {"ROLL_DICE":
                          sndObj(os.path.join(resPath, "dice.wav")),
                          "PIN_COUNT":
                          sndObj(os.path.join(resPath, "count.wav")),
                          "BELL":
                          sndObj(os.path.join(resPath, "bell.wav")),
                          "FINISH_BELL":
                          sndObj(os.path.join(resPath, "finishbell.wav")),
                          "CAGE":
                          sndObj(os.path.join(resPath, "cage.wav")),
                          "ARGH":
                          sndObj(os.path.join(resPath, "argh.wav")),
                          1:
                          sndObj(os.path.join(resPath, "one.wav")),
                          2:
                          sndObj(os.path.join(resPath, "two.wav")),
                          3:
                          sndObj(os.path.join(resPath, "three.wav")),
                          4:
                          sndObj(os.path.join(resPath, "four.wav")),
                          5:
                          sndObj(os.path.join(resPath, "five.wav")),
                          6:
                          sndObj(os.path.join(resPath, "six.wav")),
                          7:
                          sndObj(os.path.join(resPath, "seven.wav")),
                          8:
                          sndObj(os.path.join(resPath, "eight.wav")),
                          9:
                          sndObj(os.path.join(resPath, "nine.wav")),
                          10:
                          sndObj(os.path.join(resPath, "ten.wav"))
                          }

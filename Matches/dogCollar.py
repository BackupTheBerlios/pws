from lib import spw
SpwSpecMatch = spw.SPW_SpecialtyMatch
from data.globalConstants import *
name = "Dog Collar"
dq   = 0

class DogCollarBonusContainer:
    def __init__(self, wrestler):
        self._wrestler = wrestler
        self._reverseOnNextDC = None

    def setReverseOnNextDC(self, val=1):
        self._reverseOnNextDC = val

    def getReverseOnNextDC(self):
        return self._reverseOnNextDC

    def clearReverseOnNextDC(self):
        self._reverseOnNextDC = None   

class SpecialtyMatch(SpwSpecMatch):
    def __init__(self, team1, team2, timeLimit=60, network=0, dqEnabled=0):
        SpwSpecMatch.__init__(self, team1, team2, dqEnabled=0,
                              timeLimit=timeLimit, network=network)
        self._setEventChart()
        self._matchType = name
        self._specSound = None
        self._imageFile = "dogCollarMatch.jpg"
        self._labelData = (("reverseOnDC", "Rev On DC", "WHITE",
                            "GREY", (60, -1)),)

        self._dcbDict = {}
        self._initContainers(team1)
        self._initContainers(team2)

    def _initContainers(self, team):
        pos = 0
        for man in team:
            name = man.getName()
            team = man.getTeamNum()
            man.dcbKey = "%s_TEAM%d_%d" % (name, team, pos)
            self._dcbDict[man.dcbKey] = DogCollarBonusContainer(man)
            pos += 1

    def _runDefense(self, w):
        if self._dcbDict[w.dcbKey].getReverseOnNextDC():
            move = self._setDefensiveMove("REVERSE", 0)
            move["WRESTLER"] = w.getName()
            move["INDEX"] = DC_START_ROW
            move["CARD"] = DC
            move["PIPS"] = []
            self._dcbDict[w.dcbKey].clearReverseOnNextDC()
            return move

        return SpwSpecMatch._runDefense(self, w)                            

    def _runOffense(self, wrestler):
        move = {}
        move.update(SpwSpecMatch._runOffense(self, wrestler))
        w = wrestler

        if move.get("REVERSE_ON_NEXT_DC"):
            self._addBonus(w, self._dcbDict[w.dcbKey].setReverseOnNextDC, 1,
                           "REVERSE_ON_NEXT_DC")
            
        return move
        
    def _endMatchCheck(self):
        SpwSpecMatch._endMatchCheck(self)
        if not self._endMatch:
            for man in self._getMenIn():
                if self._dcbDict[man.dcbKey].getReverseOnNextDC():
                    self._sendMessage("ENABLE_LABEL", man=man,
                                      label="reverseOnDC")
                else:
                    self._sendMessage("DISABLE_LABEL", man=man,
                                      label="reverseOnDC")

    def _setEventChart(self):    
        self._eventChart = [
            {"MOVE_NAME":"EYE RAKE WITH STUDS - DRAW BLOOD",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":20},
            {"MOVE_NAME":"CANINE CHOMP",
             "MOVE_TYPE":SUBMISSION,
             "MOVE_POINTS":16},
            {"MOVE_NAME":"STRANGLE FOR WITH CHOKER CHAIN",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":14},
            {"MOVE_NAME":"TIGHTEN COLLAR AROUND OPPONENT'S NECK",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":15},
            {"MOVE_NAME":"CHAIN OPPONENT TO TURNBUCKLE",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":16},
            {"MOVE_NAME":"SMASH FOE WITH FIRE EXTINGUISHER",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":19},
            {"MOVE_NAME":"STUN FOE WITH LEASH SNAP",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "FOE_DC_ROUNDS":2},
            {"MOVE_NAME":"REMOVE OWN COLLAR",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "REVERSE_ON_NEXT_DC":1},
            {"MOVE_NAME":"SPRINKLE FOE WITH FLEAS",
             "MOVE_TYPE":SUBMISSION,
             "MOVE_POINTS":23},
            {"MOVE_NAME":"LASSO FOE INTO CORNER",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":18},
            {"MOVE_NAME":"MAKE FOE WIMPER AND ROLL OVER",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":25,
             "PIN_MODIFIER":1}
            ]

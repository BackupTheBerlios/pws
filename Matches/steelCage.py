from lib import spw
Match = spw.SPW_SpecialtyMatch
from data.globalConstants import *
name = "Steel Cage"
dq   = 0

class SpecialtyMatch(Match):
    def __init__(self, team1, team2, timeLimit=60, network=0, dqEnabled=0):
        Match.__init__(self, team1, team2, dqEnabled=0,
                           timeLimit=timeLimit, network=network)
        self._setEventChart()
        self._matchType = name
        self._specSound = "CAGE"

    def _getPinEligibility(self, roundScore):
        pinAttemptMan, pinEligibleMan, pinModifier = \
                       Match._getPinEligibility(self, roundScore)

        if (pinAttemptMan and self._pinScored[pinAttemptMan.getTeamNum()]) or \
           (pinEligibleMan and self._pinScored[pinEligibleMan.getTeamNum()]) \
                     or self._refIncapRounds:
            pinAttemptMan = None
            pinEligibleMan = None

        return pinAttemptMan, pinEligibleMan, pinModifier

    def _checkForFinish(self, wrestler):
        # If there was a pin or submission, update _pinScored appropriately
        #  and then do the climb out of cage check.  
        if self._endMatch and not self._tagTeam and \
                     not wrestler.getFinishOnPin():
            self._pinScored[wrestler.getTeamNum()] = 1
            self._endMatch = False  # reset flag, match not over!
            self._finishList = []   # empty finish list, match not over!
            self._handleClimbOutOfCage(wrestler)
        elif self._endMatch and wrestler.getFinishOnPin():
            victim = self._getMenIn()[not wrestler.getTeamNum()]
            vicname = victim.getName()
            self._doFinish(wrestler, victim)
                

    def _handleClimbOutOfCage(self, wrestler): 
        aggressor = wrestler.getName()
        victim = self._getMenIn()[not wrestler.getTeamNum()]
        vicname = victim.getName()
        if self._pinScored[wrestler.getTeamNum()] and sum(self._pinScored) < 2:
            self._sendMessage("FINISH_EVENT_MSG",
                              message="%s is attempting to climb out of the "
                                      "cage!" % aggressor)

            self._sendMessage("GENERIC_PROMPT",
                              prompt="%s roll to stop %s from "
                              "escaping the cage >" % (vicname, aggressor),
                              man=victim, type=XX)

            roll1 = self._oneD6.roll()
            roll2 = self._oneD6.roll()

            if roll1 == roll2:
                self._pinRoundCounter = roll1 + roll2 + 3
                self._pinVictim = victim
                self._sendMessage("FINISH_EVENT_MSG",
                                  message="%s did not make it out of the "
                                          "cage!\n%s has %d rounds to "
                                          "score a pin or submission!" %
                                  (aggressor, vicname,
                                   self._pinRoundCounter - 1))
            else:
                self._doFinish(wrestler, victim)
        elif sum(self._pinScored) == 2:
            self._sendMessage("FINISH_EVENT_MSG",
                              message="%s and %s are attempting to climb "
                                      "out of the cage!" % (aggressor, vicname)
                              )
            self._doCageRace()
        else:
            self._doFinish(wrestler, victim)


    def _doCageRace(self):
        climbOutRolls = [0,0]
        while not self._endMatch:
            idx = 0
            for man in self._getMenIn():
                self._sendMessage("GENERIC_PROMPT",
                                  prompt="%s roll to escape from cage >" %
                                  man.getName(),
                                  man=man, type=XX)
                
                climbOutRolls[idx] = self._twoD6.roll() +\
                                     man.getSinglesPriority()
                idx += 1
            diffVals = cmp(climbOutRolls[0], climbOutRolls[1])
            if diffVals:
                team = climbOutRolls.index(max(climbOutRolls))
                aggressor = self._getMenIn()[team]
                victim = self._getMenIn()[not team]
                self._doFinish(aggressor, victim)
        
    def _doFinish(self, aggressor, victim):
        self._endMatch = True
        self._sendMessage("FINISH_EVENT_MSG",
                          message="%s climbs out of the cage!" %
                          aggressor.getName())

        self._finishList.append({"WINNER":aggressor,
                                 "MOVE":{"MOVE_NAME":"Climb out " +\
                                         "of steel cage",
                                         "MOVE_TYPE":OFFENSIVE},
                                 "LOSER":victim})
                              
                              
        
    def _goForDQ(self, w):
        vic = self._getMenIn()[not w.getTeamNum()]
        self._sendMessage("DQ_RESULT", victim=vic, finished=0, count=0,
                          aggressor=w, dqEnabled=0)

        return 0
    
    def _submissionCheck(self, w):
        """If a wrestler has successfully executed submission move, check
           to see if they have already scored a pin or a submission.  If so,
           don't allow the wrestler to go for another submission"""

        for move in self._roundResults[w.getTeamNum()]:
            if move["MOVE_TYPE"] == SUBMISSION and move["MOVE_POINTS"] > 0 \
                   and self._doubleTeamRoundCounter < 1 and \
                   not self._pinScored[w.getTeamNum()] and \
                   not  self._refIncapRounds:
                self._goForSubmission(w)

        self._checkForFinish(w)

    def _tagOutCheck(self, w, rndScore):
        Match._tagOutCheck(self, w, rndScore)
        if self._getMenIn()[w.getTeamNum()] != w:
            w.clearDCRounds()
            
    def _setEventChart(self):    
        self._eventChart = [
            {"MOVE_NAME":"FLYING DOUBLE-LOADED ELBOW TO GROIN",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":15,
             "PIN_MODIFIER":1},
            {"MOVE_NAME":"CRUSH FINGERS AGAINST CAGE",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":10,
             "SPECIALTY_ROLL":1},
            {"MOVE_NAME":"B-52 KNEEDROP OFF TOP OF CAGE",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":20,
             "PIN_MODIFIER":1},
            {"MOVE_NAME":"CHOKE BETWEEN ROPES AND CAGE",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":14},
            {"MOVE_NAME":"CATAPULT INTO CAGE",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":15,
             "FOE_OC_PENALTY":5},
            {"MOVE_NAME":"RUNNING POWER SLAM ONTO CAGE",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":12},
            {"MOVE_NAME":"GRIND FACE INTO STEEL CAGE -- BLIND",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "FOE_DC_ROUNDS":2},
            {"MOVE_NAME":"USE BRASS KNUCKLES -- DRAW BLOOD",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":15,
             "PIN_MODIFIER":1},
            {"MOVE_NAME":"KNOCK REF UNCONSCIOUS",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "REF_INCAP_ROUNDS":4},
            {"MOVE_NAME":"CHOKE WITH CHAIN THROWN INTO CAGE BY MASKED ALLY",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":20},
            {"MOVE_NAME":"SHOULDER SMASH INTO CAGE",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":10,
             "FINISH_ON_PIN":1}
            ]
        
        

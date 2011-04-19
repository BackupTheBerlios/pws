from lib import spw
Match = spw.SPW_SpecialtyMatch
from data.globalConstants import *
name = "Texas Death"
dq   = 0

class SpecialtyMatch(Match):
    def __init__(self, team1, team2, timeLimit=60, network=0, dqEnabled=0):
        Match.__init__(self, team1, team2, dqEnabled=0,
                           timeLimit=timeLimit, network=network)
        self._setEventChart()
        self._matchType = name
        self._specSound = None


    def _getPinEligibility(self, roundScore):
        pinAttemptMan, pinEligibleMan, pinModifier = \
                       Match._getPinEligibility(self, roundScore)

        if self._refIncapRounds:
            pinAttemptMan = None
            pinEligibleMan = None

        return pinAttemptMan, pinEligibleMan, pinModifier

    def _submissionCheck(self, w):
        """If a wrestler has successfully executed submission move, check
           to see if they have already scored a pin or a submission.  If so,
           don't allow the wrestler to go for another submission"""

        for move in self._roundResults[w.getTeamNum()]:
            if move["MOVE_TYPE"] == SUBMISSION and move["MOVE_POINTS"] > 0 \
                   and self._doubleTeamRoundCounter < 1 and \
                   not  self._refIncapRounds:
                self._goForSubmission(w)


    def _setEventChart(self):    
        self._eventChart = [
            {"MOVE_NAME":"SLASH FACE WITH CAN OPENER - DRAW BLOOD",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":15,
             "PIN_MODIFIER":1},
            {"MOVE_NAME":"KNOCK REF UNCONSCIOUS",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "REF_INCAP_ROUNDS":5},
            {"MOVE_NAME":"SMASH EMPTY CHAIR OVER HEAD - DRAW BLOOD",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":20,
             "PIN_MODIFIER":1},
            {"MOVE_NAME":"THROW SALT - BLIND",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "FOE_DC_ROUNDS":2},
            {"MOVE_NAME":"CHOKE WITH COWBOY LARIAT",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":12},
            {"MOVE_NAME":"RAM HEAD INTO RINGSIDE BELL-GONG!",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":14},
            {"MOVE_NAME":"SMASH WITH 2\"x4\"",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":15,
             "FOE_OC_PENALTY":5},
            {"MOVE_NAME":"CHOKE AGAINST BOTTOM ROPE",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":14,
             "SPECIALTY_ROLL":1},
            {"MOVE_NAME":"THROW OPPONENT INTO TV ANNOUNCER",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":15},
            {"MOVE_NAME":"INTERFERENCE FROM A NON-INVOLVED WRESTLER",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":20},
            {"MOVE_NAME":"OFFER FRIENDSHIP BUT KICK IN GROIN",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":10}
            ]

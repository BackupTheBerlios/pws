from lib import spw
SpwSpecMatch = spw.SPW_SpecialtyMatch
from data.globalConstants import *
name = "Boot Camp"
dq   = 0

class BootCampPenaltyContainer:
    def __init__(self, wrestler):
        self._wrestler = wrestler
        self._ocCancelRounds = 0
        
    def setCancelOCs(self, rounds):
        self._ocCancelRounds += rounds

    def getCancelOCs(self):
        return self._ocCancelRounds

    def decrementCancelOCs(self, decval=1):
        self._ocCancelRounds -= decval

    
class BootCampBonusContainer:
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
        self._imageFile = "bootCampMatch.jpg"
        self._labelData = (("reverseOnDC", "Rev On DC", "WHITE",
                            "FOREST GREEN", (60, -1)),
                           ("noOC", "No OC", "WHITE", "FOREST GREEN",
                            (40, -1)))

        # Flags and objects specific to the boot camp match
        self._doubleDqVictim = None
        self._doubleDqAggressor = None
        self._bootCampEndMatch = 0

        self._bcpDict = {}
        self._bcbDict = {}
        self._initContainers(team1)
        self._initContainers(team2)


    def _initContainers(self, team):
        pos = 0
        for man in team:
            name = man.getName()
            team = man.getTeamNum()
            man.bcpKey = "%s_TEAM%d_%d" % (name, team, pos)
            self._bcpDict[man.bcpKey] = BootCampPenaltyContainer(man)
            man.bcbKey = "%s_TEAM%d_%d" % (name, team, pos)
            self._bcbDict[man.bcbKey] = BootCampBonusContainer(man)
            pos += 1
        
    def _runDefense(self, w):
        if self._bcbDict[w.bcbKey].getReverseOnNextDC():
            move = self._setDefensiveMove("REVERSE", 0)
            move["WRESTLER"] = w.getName()
            move["INDEX"] = DC_START_ROW
            move["CARD"] = DC
            move["PIPS"] = []
            self._clearDoubleDqFlags(w)
            self._bcbDict[w.bcbKey].clearReverseOnNextDC()
            return move

        move = {}
        move.update(SpwSpecMatch._runDefense(self, w))
        if move.get("MOVE_NAME") in ("C", "REVERSE"):
            self._clearDoubleDqFlags(w)
                    
        return move
           
    def _clearDoubleDqFlags(self, wrestler):
        if wrestler == self._doubleDqVictim:
            self._doubleDqVictim = None
            self._doubleDqAggressor = None
            
    def _runOffense(self, wrestler):
        if self._bcpDict[wrestler.bcpKey].getCancelOCs():
            move = {'MOVE_POINTS': 0, 'MOVE_TYPE': NA, 'MOVE_NAME': 'NA',
                    'PIPS':[], 'WRESTLER':wrestler.getName()}
            self._bcpDict[wrestler.bcpKey].decrementCancelOCs()
            return move

        move = {}
        move.update(SpwSpecMatch._runOffense(self, wrestler))
        w = wrestler
        if move.get("DOUBLE_DQ") and self._doubleTeamRoundCounter < 1:
            if self._doubleDqVictim:
                ddqagg = self._doubleDqAggressor
                self._doubleDqAggressor = self._getHigherMan(ddqagg, w)
                victeam = not self._doubleDqAggressor.getTeamNum()
                self._doubleDqVictim = self._getMenIn()[victeam]
            else:
                self._doubleDqAggressor = w
                self._doubleDqVictim = self._getMenIn()[not w.getTeamNum()]
        elif move.get("ENABLE_DQ"):
            move["MOVE_POINTS"] = DQ
        elif move.get("FOE_OC_CANCEL_ROUNDS"):
            cancelRounds = move.get("FOE_OC_CANCEL_ROUNDS")
            otherMan = self._getMenIn()[not w.getTeamNum()]
            self._addPenalty(otherMan,
                             self._bcpDict[otherMan.bcpKey].setCancelOCs,
                             cancelRounds,
                             "FOE_OC_CANCEL_ROUNDS")
        elif move.get("REVERSE_ON_NEXT_DC"):
            self._addBonus(w, self._bcbDict[w.bcbKey].setReverseOnNextDC, 1,
                           "REVERSE_ON_NEXT_DC")
            
        return move

    def _resolveMoves(self):
        SpwSpecMatch._resolveMoves(self)
        # In the event where a Kamikaze Dive was rolled make the DQ roll
        # for the victim of the Kamikaze Dive.  
        if self._doubleDqVictim and self._doubleTeamRoundCounter < 1:
            name = self._doubleDqVictim.getName()
            w = self._getMenIn()[not self._doubleDqVictim.getTeamNum()]
            for move in self._roundResults[w.getTeamNum()]:
                if move.get('DOUBLE_DQ'):
                    move["MOVE_POINTS"] = DQ
                    # Temporarily enable DQs
                    self._dqEnabled = 1
                    alttext = "%s is down. " % name
                    alttext += "The referee begins the count..."
                    altresult = "%s answers the count!" % name
                    points = self._goForDQ(w, alttext, 1, altresult)
                    # Put Move points into another key-value pair so that
                    # the points can be applied later since the match engine
                    # needs the MATCH_POINTS value to be set to DQ
                    if points > 9:
                        move["TMP_MOVE_POINTS"] = 0
                        # Even though there was a countout here, there's still
                        # a chance that there may be a countout in another
                        # function...Ugh.  Set a boot camp specific flag
                        self._endMatch = 0
                        self._bootCampEndMatch = 1
                    else:
                        move["TMP_MOVE_POINTS"] = points
                        
                    self._doubleDqVictim = None
                    self._dqEnabled = 0    # Disable DQs
                    break
        
    def _dqCheck(self, w):
        # countOut flag is used to determine if a team ( w.getTeamNum() )  has
        #  scored a count out in the current round.
        countOut = False
        appendDqMove = 1
        for move in self._roundResults[w.getTeamNum()]:
            # If team already has already scored a countout, there is no need
            # to try and score another.  The following if block takes care of
            # this.
            if move["MOVE_TYPE"] == DQ and move["MOVE_POINTS"] == DQ and \
                   not countOut:
                alttext = None
                altresult = None
                printScore = 1
                # Temporarily enable DQs for certain move types
                if move.get("DOUBLE_DQ") or move.get("ENABLE_DQ"):
                    self._dqEnabled = 1
                    if move.get("ENABLE_DQ"):
                        otherMan = self._getMenIn()[not w.getTeamNum()]
                        name = otherMan.getName()
                        alttext = "%s is injured and on the mat." % name
                        alttext += "  The referee begins the count..."
                        altresult = "%s answers the count!" % name
                    else:
                        # This is the case where a Kamikaze Dive was rolled
                        # and now the wrestler who made the dive must
                        # check to see if he is counted out.  This block
                        # sets the victim as the "aggresor" for the dq roll.
                        # We also need to give the points to the wrestler
                        # who intiated the KAMIKAZE DIVE.  Those points
                        # were stored in the TMP_MOVE_POINTS dict member
                        #
                        # If double teaming is occuring, the dq roll will only
                        # be for points
                        # If both men in rolled a KAMIKAZE DIVE, then only
                        # make a dq for the wrestler with the higher
                        # priority (self._doubleDqAggressor)
                        if self._doubleTeamRoundCounter > 0:
                            self._dqEnabled = 0
                            appendDqMove = 0
                        elif w != self._doubleDqAggressor:
                            continue
                            
                        printScore = 0
                        alttext = "%s is down from the KAMIKAZE DIVE!" % \
                                  w.getName()
                        alttext += " The referee begins the count..."
                        dqMove = {}
                        dqMove.update(move)
                        dqMove["MOVE_NAME"] = "KAMIKAZE DIVE RECOVERY"
                        w = self._getMenIn()[not w.getTeamNum()]
                        if appendDqMove:
                            self._roundResults[w.getTeamNum()].append(dqMove)
                            appendDqMove = 0
                        move["MOVE_POINTS"] = move["TMP_MOVE_POINTS"]

                w.setPinStatus(0)
                points = self._goForDQ(w, alttext, printScore, altresult)
                if points > 9 and self._dqEnabled:
                    # There should be no points added to the team's total score
                    # if a countout occurs so set the DQ's move points to
                    # zero.
                    if printScore:
                        move["MOVE_POINTS"] = 0
                    countOut = True
                elif printScore:
                    move["MOVE_POINTS"] = points

                # Disable DQs
                if move.get("DOUBLE_DQ") or move.get("ENABLE_DQ"):
                    self._dqEnabled = 0

        # A dq may have been scored previously, if so set the end match
        # flag here
        if self._bootCampEndMatch:
            self._endMatch = 1
        
    def _endMatchCheck(self):
        SpwSpecMatch._endMatchCheck(self)
        if not self._endMatch:
            for man in self._getMenIn():
                cancelOCs = self._bcpDict[man.bcpKey].getCancelOCs()
                msg = None
                if cancelOCs > 0:
                    toolTip = "Next %d OCs will be cancelled" % cancelOCs
                    self._sendMessage("ENABLE_LABEL", man=man, label="noOC",
                                      tooltip=toolTip)
                else:
                    self._sendMessage("DISABLE_LABEL", man=man, label="noOC")

                if self._bcbDict[man.bcbKey].getReverseOnNextDC():
                    self._sendMessage("ENABLE_LABEL", man=man,
                                      label="reverseOnDC")
                else:
                    self._sendMessage("DISABLE_LABEL", man=man,
                                      label="reverseOnDC")
                    
                
                
        
    def _setEventChart(self):    
        self._eventChart = [
            {"MOVE_NAME":"KAMIKAZE DIVE",
             "MOVE_TYPE":DQ,
             "DOUBLE_DQ":1},
            {"MOVE_NAME":"INJURE FOE (Call MASH Unit)",
             "MOVE_TYPE":DQ,
             "ENABLE_DQ":1},
            {"MOVE_NAME":"SMASH FOE WITH GERMAN HELMET",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":14},
            {"MOVE_NAME":"TAKE OPPONENT P.O.W.",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "FOE_OC_CANCEL_ROUNDS":2},
            {"MOVE_NAME":"STOMP ON HEAD WITH MILITARY BOOT",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":16},
            {"MOVE_NAME":"AMBUSH BY GUERILLA ATTACK",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":22},
            {"MOVE_NAME":"DROP AND GIVE FOE 20 PUSHUPS",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":20},
            {"MOVE_NAME":"B-52 BACKBREAKER",
             "MOVE_TYPE":SUBMISSION,
             "MOVE_POINTS":19},
            {"MOVE_NAME":"MILITARY CRAWL TO SAFETY",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":0,
             "REVERSE_ON_NEXT_DC":1},
            {"MOVE_NAME":"DIG HEEL INTO ESOPHAGUS",
             "MOVE_TYPE":OFFENSIVE,
             "MOVE_POINTS":15},
            {"MOVE_NAME":"BLUDGEON FOE WITH RIFLE BUTT",
             "MOVE_TYPE":PA,
             "MOVE_POINTS":22,
             "PIN_MODIFIER":1}
            ]

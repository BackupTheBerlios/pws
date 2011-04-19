"""
Copyright 2003 John LeGrande

    This file is part of Pro Wrestling Superstar.

    Pro Wrestling Superstar is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Pro Wrestling Superstar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Pro Wrestling Superstar; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    A copy of the GNU GPL is included with Pro Wrestling Superstar in the file
    license.txt. 
"""

import random, copy, string, os.path
import asyncore
from data.globalConstants import *
import util

# _PcTable contains all of the pin coefficients to determine a Pin score
# when a pin attempt is made.  This table is used by the getPinScore
# method in the match class.  These coefficients were determined by
# plotting points that provided terms to be used in a polynomial function.
# The "dice roll" will determine which set of coefficients will be used
# when trying to determine a pin score.
_PcTable=( (1.979, -0.1955 , 0.2325, -.04057, .003794, -.0001268),
           (1.835, 0.7553,-.1941, .03166, -.001259),
           (1.8507,0.407043,0.136349,-0.0368212,0.00401624,-0.000138823),
           (2.12036,0.159969,0.429073,-0.121858,0.0127314,-0.000426193),
           (2.8942,0.233225,0.255282,-0.0714956,0.00779086,-0.000266631),
           (2.81664,0.486365,0.12849,-0.0446613,0.0054668,-0.000196376),
           (2.99063,1.31414,-0.257259,0.0270636,-0.000557041),
           (3.9324, 0.829254,-0.969406,0.588141,-0.120921,0.00801282),
           (4,0.416667,1.70833,-1.41667,0.291667),
           (5,-6,6),
           (17,)
         )


class Dice:
    def __init__(self, valArg, numDice=1):
        self._maxVal = valArg
        self._numDice = numDice
        
    def roll(self):
        dieRoll = 0
        self.pips = []
        for die in range(self._numDice):
            roll = random.randint(0, self._maxVal)
            dieRoll += roll
            self.pips.append(roll)
        return dieRoll

class Wrestler:
    def __init__(self, wrestler, network=1):
        wrestler = util.getWrestlerModule(wrestler.path)
        if network:
            from Networking import CopyDice
            diceobj = CopyDice
        else: diceobj = Dice
        
        self._twoD6 = diceobj(5, 2)
        self._oneD6 = diceobj(5)
        self._name = wrestler.name
        self._GenCardList = wrestler.GeneralCard
        self._OCardList = wrestler.OffensiveCard
        self._DCardList = wrestler.DefensiveCard
        self._SpecialtyList = []

        # Build MoveDict from Specialty Card
        for specElem in wrestler.Specialty[wrestler.Specialty.keys()[0]]:
            specElem["MOVE_NAME"] = wrestler.Specialty.keys()[0]
            self._SpecialtyList.append(specElem)
            
        self._RopesList = wrestler.Ropes
        self._submissionRange = self._expandRange(wrestler.Sub)
        self._tagTeamRange = self._expandRange(wrestler.TagTeam)
        self._singlesPriority = wrestler.Priority[0]
        self._tagTeamPriority = wrestler.Priority[1]
        self._nameSet = ""
        if hasattr(wrestler, "nameSet"):
            self._nameSet = wrestler.nameSet

        # Ensure that we are using the .py extension
        filename = os.path.splitext(os.path.abspath(wrestler.__file__))[0]
        self._filename = os.path.normpath("%s.py" % filename)
        
        self._injured = False
        self._pinStatus = 1

        self._pinModifier = 0
        self._ocPenalties = []
        self._dcRounds = []
        self._finishOnPin = False

    def getName(self): return self._name

    # Get Cards
    def getGeneralCard(self): return self._GenCardList
    def getDefensiveCard(self): return self._DCardList
    def getSpecialtyCard(self): return self._SpecialtyList
    def getOffensiveCard(self): return self._OCardList
    def getRopesCard(self): return self._RopesList
    def getSubmissionRange(self): return self._submissionRange
    def getTagTeamRange(self): return self._tagTeamRange
    def getSinglesPriority(self): return self._singlesPriority
    def getTagTeamPriority(self): return self._tagTeamPriority
    def getNameSet(self): return self._nameSet

    # Get/Set methods
    def setCPU(self, isCPU): self._cpu = isCPU
    def isCPU(self): return self._cpu
    def setStatus(self, statusVal): self._status = statusVal
    def getStatus(self): return self._status
    def setTeamPos(self, pos): self._teamPos = pos
    def getTeamPos(self): return self._teamPos
    def setTeamNum(self, tnum): self._teamNum = tnum
    def getTeamNum(self): return self._teamNum
    def getFileName(self): return self._filename
    def setInjured(self, val): self._injured = val
    def getInjuryRounds(self): return self._injured
    def getOneD6Pips(self): return self._oneD6.pips
    def getTwoD6Pips(self): return self._twoD6.pips
    def setPinStatus(self, val): self._pinStatus = val
    def pinStatus(self): return self._pinStatus
    
    # These methods are used during a grudge match
    def setPinModifier(self, pinmod): self._pinModifier = pinmod
    def getPinModifier(self): return self._pinModifier
    def setOCPenalty(self, penalty): self._ocPenalties.append(penalty)
    def getOCPenalty(self):
        if len(self._ocPenalties): penalty = self._ocPenalties.pop(0)
        else: penalty = 0
        return penalty
    def popOCPenalty(self): self._ocPenalties.pop()
    def hasOCPenalty(self): return len(self._ocPenalties)
    def addDCRounds(self, rounds): self._dcRounds += [DC] * rounds
    def popDCRound(self): self._dcRounds.pop()
    def clearDCRounds(self): self._dcRounds = []            
    def getDCRounds(self): return len(self._dcRounds)
    def setFinishOnPin(self, val): self._finishOnPin = val
    def getFinishOnPin(self): return self._finishOnPin    
            
    # roll dice Methods
    def rollGenCard(self):
        roll = self._twoD6.roll()
        return {"RESULT":self._GenCardList[roll], "INDEX":roll, "CARD":GC,
                "PIPS":self._twoD6.pips}

    def rollOffCard(self):
        roll = self._twoD6.roll()
        move = self._OCardList[roll]
        move["INDEX"] = roll
        move["CARD"] = OC
        move["PIPS"] = self._twoD6.pips
        return move

    def rollDefCard(self):
        roll = self._twoD6.roll()
        return {"RESULT":self._DCardList[roll], "INDEX":roll,
                "PIPS":self._twoD6.pips}

    def rollSpecialty(self):
        roll = self._oneD6.roll()
        move = self._SpecialtyList[roll]
        move["INDEX"] = roll
        move["CARD"] = SPECIALTY
        move["PIPS"] = self._oneD6.pips
        return move

    def rollRopes(self):
        roll = self._twoD6.roll()
        move = self._RopesList[roll]
        move["INDEX"] = roll
        move["CARD"] = ROPES
        move["PIPS"] = self._twoD6.pips        
        return move

    def roll2D6(self): return self._twoD6.roll()
    def roll1D6(self): return self._oneD6.roll()    

    # Checks
    def submits(self):
        submits = False
        rollVal = self._twoD6.roll() + 2
        if (rollVal in self._submissionRange):
            submits = True
        return submits

    def makeSave(self):
        makeSave = False
        rollVal = self._twoD6.roll() + 2
        if (rollVal in self._tagTeamRange):
            makeSave = True
        return makeSave

    # Utility methods
    def _expandRange(self, rt):
        if len(rt) < 2:
           return tuple(rt)
           
        return tuple(range(rt[0], rt[1] + 1))
        

class Match:
    def __init__(self, team1, team2, dqEnabled=1, timeLimit=30, network=0):
        self._teams = [team1, team2]
        self._manIn = [team1[0], team2[0]]
        self._sendMessage = None
        self._network = network
        self._currentTeam = 0
        self._twoD6 = Dice(5, 2)
        self._oneD6 = Dice(5, 1)
        self._setRef()
        self._genCardResults = [0,0]
        self._dtGenCardResults = []
        self._roundResults = [[],[]]
        self._totalScore = [0,0]
        self._finishList = []
        self._percentageDie = Dice(99)
        self._doubleTeamRoundCounter = 0
        self._doubleTeamList = []
        self._dqEnabled = dqEnabled
        self._timeLimit = timeLimit
        self._endMatch = False
        self._matchRunning = True
        self._tagTeam = False
        self._allInRing = False
        self._round = 1
        self._matchType = "Regular"
        self._imageFile = None
        self._labelData = []
        
        if len(team1) > 1 or len(team2) > 1:
            self._tagTeam = True
        
        if self._tagTeam:
           from data import tagChart
           self._tagChart = tagChart.TagChart(len(team1))

        self._specMoveRolls = 0
        self._specMoveCheckNeeded = True
        self._state = UNRESOLVED_GC_ROLL
        self._strategyPinChart =  None
        self._onlyPinOnPA = None
        
    def setDQ(self, dqEnabled=1): self._dqEnabled = dqEnabled
    def setTimeLimit(self, timeLimit): self._timeLimit = timeLimit

    def setInterfaces(self, resultQ, msgQ, signalQ):
        self._resultController = ResultController(resultQ, msgQ)
        self._sendMessage = self._resultController.getResult
        self._signalQueue = signalQ

    def useStrategyPinChart(self, usechart=0):
        from data import strategyPinChart
        if usechart:
            self._strategyPinChart = strategyPinChart.PinChart()
        else:
            self._strategyPinChart = 0
        
    def pinOnlyOnPA(self, pinonpa=0):
        self._onlyPinOnPA = pinonpa
            
    def getResultHandler(self): return self._resultController.getResultHandler()
    
    def _matchIsStopped(self):
        return self._endMatch
            
    def _setRef(self):
        rollVal = self._twoD6.roll()
        self._ref = 0
        if (rollVal == 1):
            self._ref = 1
        elif (rollVal == 9):
            self._ref = -1

    def getRef(self):
        if (self._ref == 0): refString = "'Honest' Abe (+0)"
        elif (self._ref == 1): refString = "'Fast Count' Frank (+1)"
        else: refString = "'Slow-Count' Sam (-1)"
        return refString

    def getTeams(self): return self._teams
    def getTimeLimit(self): return self._timeLimit
    def getMatchType(self): return self._matchType
    def getImageFile(self): return self._imageFile
    def getLabelData(self): return self._labelData
    
    def _dummyInterfaceCB(self, msg, **kw): return 0
    
    def stopMatch(self):
        self._endMatch = True
        self._sendMessage = self._dummyInterfaceCB
        self._resultController.waitForResult = False
        self._resultController.resultQueue.put(0)
        self._manIn[0].setCPU(1)
        self._manIn[1].setCPU(1)
        
    def isRunning(self):
        return self._matchRunning
    
    def isTagMatch(self): return self._tagTeam

    def isDraw(self):
        return len(self._finishList) < 1
            
    def isDoubleCountout(self):
        return len(self._finishList) > 1
            
    def getWinners(self):
        winners = []
        if len(self._finshList) == 1:
            return self.getTeams()[finish["WINNER"].getTeamNum()]
        elif self.isDraw():
            return []
        else:
            return None
        
    def getTeamStrings(self):
        return [self.getTeamString(t) for t in (0, 1)]

    def getTeamString(self, teamnum):
        team = self.getTeams()[teamnum]
        teamStr = ""
        idx = 1
        for member in team:
            delimiter = ", "            
            if idx == len(team) - 1:
                delimiter = ", "
                if len(team) == 2:
                    delimiter = " "                
                delimiter += "and "
            teamStr += "%s%s" % (member.getName(), delimiter)
            idx += 1
            
        return teamStr[:-2]

    def getMatchResultData(self):
        teams = self.getTeams()
        matchtime = self._round - 1
        finish = self._finishList
        teamStrs = self.getTeamStrings()
        if self.isDraw():
            t1, t2 = teamStrs
            winteam, loseteam = (0, 1)
            resultStr = "%s wrestled to a %d minute\n" % (t1, matchtime)
            resultStr += "time limit draw with %s." % t2
            resultOrder = (0, 1)
        elif self.isDoubleCountout():
            dq1, dq2 = [finish[idx]["WINNER"].getName() for idx in (0, 1)]
            dqees = "%s and %s" % (dq1, dq2)
            winteam, loseteam = (0, 1)
            resultStr = "At the %d minute mark \n%s were " % (matchtime,
                                                              dqees) 
            resultStr += "both counted out, resulting in a draw."
            resultOrder = (0, 1)
        else:
            winner = finish[0]["WINNER"].getName()
            winteam = finish[0]["WINNER"].getTeamNum()
            winmove = finish[0]["MOVE"]["MOVE_NAME"]
            loser = finish[0]["LOSER"].getName()
            loseteam = finish[0]["LOSER"].getTeamNum()

            resultStr = "At the %d minute mark " % matchtime
            if finish[0].get("COUNTOUT", None):
                resultStr += "%s was counted out " % loser
            elif finish[0].get("SUBMISSION", None):
                resultStr += "%s submits " % loser
            else:
                resultStr += "%s was pinned " % loser
            resultStr += "\nafter %s executed a %s.\n\n" % (winner, winmove)
            isplural = "s" * int(len(teams[winteam]) < 2)
            resultStr += "%s win%s the match.\n" % (teamStrs[winteam],
                                                    isplural)
            resultOrder = (winteam, loseteam)
               
        winkey, losekey = [util.formatTeamKey(teams[t]) for t in resultOrder]

        return {"WINNER_KEY":winkey,
                "LOSER_KEY":losekey,
                "WINNER_NAME":teamStrs[winteam],
                "LOSER_NAME":teamStrs[loseteam],
                "RESULT_STRING":resultStr}
                
        
    def _prompt(self, promptVal, skipFlag):
        inputVal = None
        if not skipFlag:
            inputVal = raw_input(promptVal)
        return inputVal

    def _runOffense(self, w):
        self._sendMessage("GENERIC_PROMPT", prompt="%s Roll Offensive Card > " \
                          % w.getName(), man=w, type=OC)
        action = copy.deepcopy(w.rollOffCard())

        if (action["MOVE_TYPE"] == ROPES):
            self._sendMessage("GENERIC_PROMPT", prompt="%s Roll Ropes Card > " % \
                              w.getName(), man=w, type=ROPES)
            action = copy.deepcopy(w.rollRopes())

        if (action["MOVE_TYPE"] == SPECIALTY):
            self._sendMessage("GENERIC_PROMPT", prompt="%s Roll Specialty Card > " % \
                              w.getName(), man=w, type=SPECIALTY)
            action = copy.deepcopy(w.rollSpecialty())

        if (action["MOVE_TYPE"] == DQ):
            action["MOVE_POINTS"] = DQ

        action["WRESTLER"] = w.getName()
        
        #print "%s executes %s for %d points" % (action["WRESTLER"],
        #                                        action["MOVE_NAME"],
        #                                        action["MOVE_POINTS"])
        return action

    def _runDefense(self, w):
       self._sendMessage("GENERIC_PROMPT", prompt="%s Roll Defensive Card > " % \
                         w.getName(), man=w, type=DC)

       defenseValue = w.rollDefCard()
       if (defenseValue["RESULT"] == A): action = self._setDefensiveMove("A", A)
       elif (defenseValue["RESULT"] == B): action = self._setDefensiveMove("B", B)
       elif (defenseValue["RESULT"] == C): action = self._setDefensiveMove("C", C)
       else: action = self._setDefensiveMove("REVERSE", 0)

       action["WRESTLER"] = w.getName()
       action["INDEX"] = defenseValue["INDEX"]
       action["CARD"] = DC
       action["PIPS"] = defenseValue["PIPS"]
       ##print "%s executes %s for %d points" % (action["WRESTLER"],
##                                               action["MOVE_NAME"],
##                                               action["MOVE_POINTS"])

       return action

    def _setDefensiveMove(self, mType, dVal):
        action = {"MOVE_NAME":mType,
                  "MOVE_POINTS":dVal,
                  "MOVE_TYPE":DEFENSIVE}

        return action

    def _getManIn(self, team=-1):
        if team < 0: team = self._currentTeam
        return self._manIn[team]

    def _getMenIn(self):
       w1 = self._getManIn(0)
       w2 = self._getManIn(1)
       return w1, w2


    def _getMenOut(self, team):
        menOut = []
        for i in self._teams[team]:
            if self._manIn[team].getName() != i.getName():
               menOut.append(i)
        return menOut
        
    def _getOtherTeam(self):
        if (self._currentTeam == 0): otherTeam = self._currentTeam + 1
        else: otherTeam = self._currentTeam - 1

        return otherTeam

    def _rollDice(self):
        if self._matchIsStopped(): return
        self._state = UNRESOLVED_GC_ROLL
        unresolvedGenRoll = True
        self._sendMessage("ROUND_BORDER", start=1, time=self._round)
        
        while (unresolvedGenRoll and self._doubleTeamRoundCounter < 1):
            for i in (0,1):
                self._currentTeam = i
                self._genCardResults[i] = self._promptGenRoll(self._getManIn())
                
            if self._genCardResults[0] == DC and self._genCardResults[1] == DC:
                self._sendMessage("GENERIC_MESSAGE",\
                                  message="Both Men in rolled DC\n\n")
            else: unresolvedGenRoll = False

        # if double team round counter > 0 roll general cards for all
        #   doubleteamers and roll General Card for shorthanded team man in
        while(self._doubleTeamRoundCounter > 0 and unresolvedGenRoll):
            self._dtGenCardResults = []
            dtGenCardResults = self._dtGenCardResults
            for man in self._doubleTeamList:
                dtGenCardResults.append(self._promptGenRoll(man))

            self._currentTeam = self._shortHandedTeamNum
            manIn = self._getManIn()
            self._genCardResults[self._currentTeam] = self._promptGenRoll(manIn)
            self._genCardResults[self._getOtherTeam()] = OCTT

            doubleTeamersAllDC = not cmp(DC * len(dtGenCardResults),
                                     self._getListTotal(dtGenCardResults))
                          
            if self._genCardResults[self._currentTeam] == DC and \
               doubleTeamersAllDC:
                self._sendMessage("GENERIC_MESSAGE",\
                                  message="Everyone rolled DC\n")
            else: unresolvedGenRoll = False

        # If not double teaming and OC/TT is rolled, call doubleTeamSetup
        #  function.
        if self._doubleTeamRoundCounter < 1 and OCTT in self._genCardResults and \
               self._tagTeam:
            self._dtGenCardResults = []
            # Get the double teaming action started
            if self._genCardResults[0] == OCTT and \
               self._genCardResults[1] == OCTT:
                # Everyone is in the ring for one round, set flag
                self._allInRing = True
                self._doubleTeamRoundCounter = 1
                self._sendMessage("GENERIC_MESSAGE", message="\nEveryone in the"+\
                                  " ring for one round!!!")
            elif OCTT in self._genCardResults:
                self._getTagChartResults(self._genCardResults.index(OCTT))
                if len(self._doubleTeamList):
                    for man in self._doubleTeamList:
                        if man.getInjuryRounds() < 1:
                            self._dtGenCardResults.append(OC)
                        else: self._dtGenCardResults.append(INJURED)

            self._state = UNRESOLVED_MOVES

    def _promptGenRoll(self, w):
        tmpCurrTeam = self._currentTeam
        self._currentTeam = w.getTeamNum()
        index = 0
        # If other man-in is not injured, and current man-in is not injured
        #  roll on General Card
        if self._manIn[self._getOtherTeam()].getInjuryRounds() < 1 and \
           w.getInjuryRounds() < 1:
            self._sendMessage("GENERIC_PROMPT",\
                              prompt="%s Roll General Card > " % w.getName(),\
                              man=w, type=GC)
            gcRoll = w.rollGenCard()
            retGCRoll = gcRoll["RESULT"]
            index = gcRoll["INDEX"]
            pips = gcRoll["PIPS"]
        # If current man-in is injured, set General Card roll to INJURED
        elif w.getInjuryRounds() > 0:
            retGCRoll = INJURED
            index = INJURED
            pips = []
        # The other man-in is injured (which would mean all team members
        #  are injured on the other team) and current
        #   man-in isn't injured.  Set current man-in General Card to OC.
        else:
            retGCRoll = OC
            index = OC
            pips = []
            
        self._currentTeam = tmpCurrTeam
        self._sendMessage("GENERAL_CARD_RESULT", man=w, result=retGCRoll,
                          index=index, die_pips=pips)

        return retGCRoll

    def _getListTotal(self, theList):
        y = 0
        for x in theList:
           y += x
        return y

    def _getTagChartResults(self, teamNum):
        self._currentTeam = teamNum
        offManIn = self._getManIn()
        offTTR = self._selectHighManOut()
        if offTTR < 1:
            self._doubleTeamRoundCounter = 0
            return
            
        self._currentTeam = self._getOtherTeam()
        defManIn = self._getManIn()
        defTTR = self._selectHighManOut()
        if defTTR < 1:
            dtr = self._doubleTeamRoundCounter = 1
            for man in self._teams[offManIn.getTeamNum()]:
                if man.getInjuryRounds() < 1:
                    self._doubleTeamList.append(man)

            self._shortHandedTeamNum = defManIn.getTeamNum()
            self._sendMessage("DOUBLE_TEAM_START",\
                               doubleTeamList=self._doubleTeamList,\
                               doubleTeamRounds=dtr)
            return
            
        tagRollModifier = offTTR - defTTR
        tagRoll = offManIn.roll2D6() + int(round(tagRollModifier))
        if tagRoll > 10: tagRoll = 10
        elif tagRoll < 0: tagRoll = 0
        
        results = self._tagChart.getTagChartResults(tagRoll)
        dtr = self._doubleTeamRoundCounter = results["ROUND_COUNT"]
        self._shortHandedTeamNum = defManIn.getTeamNum()
        if results["MAX_DT"] == ALL:
            self._allInRing = True
            self._sendMessage("GENERIC_MESSAGE", message="\nEveryone in the"+\
                              " ring for one round!!!")
        elif results["MAX_DT"] < len(self._teams[offManIn.getTeamNum()]):
            menOut = self._getMenOut(offManIn.getTeamNum())
            if not offManIn.isCPU():
               manCount = 0
               possibleDoubleTeamers = []
               for man in menOut:
                   if man.getInjuryRounds() < 1:
                       possibleDoubleTeamers.append(man)
                       manCount += 1
               pdters = map(lambda x: "%s" % x.getName(), possibleDoubleTeamers)

               accompliceIdx = self._sendMessage("CHOICE_LIST",\
                                                 prompt="Select double teamer:",\
                                                 choicelist=pdters,man=offManIn,
                                                 caption="Double Team Selction")

               accomplice = possibleDoubleTeamers[accompliceIdx]
               self._doubleTeamList = [offManIn, accomplice]
            else:
               randNum = random.randint(0, len(menOut) - 1)
               self._doubleTeamList = [offManIn, menOut[randNum]]
        elif results["MAX_DT"] == INJURED:
            injResults = self._tagChart.getInjuryResults(offManIn.roll1D6())
            if "MAN-OUT" in injResults["INJURED"]:
                menOut = self._getMenOut(defManIn.getTeamNum())
                man = menOut[random.randint(0, len(menOut) - 1)]
                man.setInjured(injResults["ROUND_COUNT"])
                m = man
                self._sendMessage("INJURY_STATUS", start=1,man=m,
                                   injuryRound=injResults["ROUND_COUNT"])

            if "MAN-IN" in injResults["INJURED"]:
                defManIn.setInjured(injResults["ROUND_COUNT"])
                m = defManIn
                self._sendMessage("INJURY_STATUS", start=1,man=m,
                                   injuryRound=injResults["ROUND_COUNT"])
                
                availableMenOut = []
                for man in self._getMenOut(defManIn.getTeamNum()):
                    if man.getInjuryRounds() < 1:
                        availableMenOut.append(man)

                team = defManIn.getTeamNum()
                dMan = defManIn

                if len(availableMenOut) == 1:
                    dMan = self._manIn[team] = availableMenOut[0]
                    self._sendMessage("NEW_MAN_IN", new_man_in=dMan)
                elif len(availableMenOut) > 1 and not defManIn.isCPU():
                    manCount = 0
                    aMenOut = map(lambda x: "%s" % x.getName(), availableMenOut)
                    newManIdx = self._sendMessage("CHOICE_LIST",\
                                                  prompt= "Select new man-in:",\
                                                  choicelist=aMenOut,man=defManIn,
                                                  caption="Man Injured!!")

                    dMan = self._manIn[team] = availableMenOut[newManIdx]
                    self._sendMessage("NEW_MAN_IN", new_man_in=dMan)
                elif len(availableMenOut) > 1 and defManIn.isCPU():
                    dMan = self._manIn[team] = \
                           availableMenOut[random.randint(0, len(availableMenOut) - 1)]                    
                    self._sendMessage("NEW_MAN_IN", new_man_in=dMan)

                # Roll on General Card for defensive man in
                # If man in is injured the promptGenRoll method will return
                #  an INJURED General Card result
                self._genCardResults[team] = self._promptGenRoll(dMan)

                
            self._doubleTeamRoundCounter = 0
        else:
            self._doubleTeamRoundCounter = results["ROUND_COUNT"]
            
            for man in self._teams[offManIn.getTeamNum()]:
                if man.getInjuryRounds() < 1:
                    self._doubleTeamList.append(man)

        if len(self._doubleTeamList):
            dtl = self._doubleTeamList
            self._sendMessage("DOUBLE_TEAM_START", doubleTeamList=dtl,\
                               doubleTeamRounds=dtr)

    def _selectHighManOut(self):
        maxTagPri = 0
        menOut = self._getMenOut(self._currentTeam)
        maxList = []
        manOut = None
        pri = 0
        
        for man in menOut:
           if man.getInjuryRounds() < 1:
               if man.getTagTeamPriority() >= maxTagPri: maxList.append(man)
               
        if not self._getManIn().isCPU() and len(maxList) > 1:
            l=map(lambda x: "%s (%s)" % (x.getName(), x.getTagTeamPriority()), maxList)
            i=self._sendMessage("CHOICE_LIST", prompt='Select man out:',\
                                choicelist=l,man=self._getManIn(),
                                caption="Man out selection")
            manOut = maxList[i]
        elif self._getManIn().isCPU() and len(maxList) > 1:
            manOut = maxList[random.randint(0, len(maxList) - 1)]
        elif len(maxList) == 1:
            manOut = maxList[0]

        if manOut: pri = manOut.getTagTeamPriority()
        return pri

    
    def _resolveMoves(self):
        if self._matchIsStopped(): return
        roundAction = [[], []]
        roundMoveStatus = []
        self._currentTeam = 0
        reversalFlag = None

        while(len(roundMoveStatus) < 2):
            # Handle double teamers offense or defense if double teaming
            # set cardVal to None if all men are in the ring for the round
            #  and all moves have been resolved
            if self._doubleTeamRoundCounter > 0:
                doubleTeamMoveResults = self._handleDoubleTeamMoves(\
                                        roundAction,\
                                        roundMoveStatus)
                roundAction = doubleTeamMoveResults["ROUND_ACTION"]
                roundMoveStatus = doubleTeamMoveResults["ROUND_MOVE_STATUS"]

                self._currentTeam = self._getOtherTeam()
            
            if len(roundMoveStatus) < 2:
                manInMoveResults = self._handleManInMove(roundAction,
                                                         roundMoveStatus)
                roundAction = manInMoveResults["ROUND_ACTION"]
                reversalFlag = manInMoveResults["REVERSAL_FLAG"]
                roundMoveStatus = manInMoveResults["ROUND_MOVE_STATUS"]

            if reversalFlag: reversalFlag = False
            elif not reversalFlag: self._currentTeam = self._getOtherTeam()
                
        self._specMoveRolls = 0
        self._specMoveCheckNeeded = True

        # Reset currentTeam to handle any additional wrestlers
        self._currentTeam = 0

        # Assign round results
        self._roundResults[0] = roundAction[0]
        self._roundResults[1] = roundAction[1]

        self._state = END_MATCH_CHECK

    def _endMatchCheck(self):
        if self._matchIsStopped(): return
        roundScore = [0,0]
        self._currentTeam = 0
        teamCount = 0
        points = 0
        submissionFinish = False
        
        w1, w2 = self._getMenIn()
        wrestler = self._getHigherMan(w1, w2)
        self._currentTeam = wrestler.getTeamNum()
        while(not submissionFinish and teamCount < 2):
            if not self._endMatch:
                self._submissionCheck(wrestler)
                if self._endMatch: submissionFinish = True

            if not submissionFinish:
                self._dqCheck(wrestler)

            self._currentTeam = self._getOtherTeam()
            teamCount += 1
            wrestler = self._getManIn()

        for team in (0,1):
            for move in self._roundResults[team]:
                roundScore[team] += move["MOVE_POINTS"]
                self._totalScore[team] += move["MOVE_POINTS"]

        self._sendMessage("SCORE", teams=self._teams, scores=roundScore, \
                          scoretype="ROUND")
        

        pinAttemptMan, pinEligibleMan, pinModifier = \
                       self._getPinEligibility(roundScore)
        
        if pinAttemptMan and not self._endMatch:
            points = self._goForPin(pinAttemptMan, pinModifier)
            self._totalScore[pinAttemptMan.getTeamNum()] += points
        elif pinEligibleMan and not self._endMatch:
            if self._tagTeam:
                # Normalize the tag team priority values
                #  to the singles priority (5.0 / 3)
                priVal =  pinEligibleMan.getTagTeamPriority() * 5.0 / 3
            else:
                priVal =  pinEligibleMan.getSinglesPriority()

            # Pin bonus = priority * 5
            pinBonus = priVal * 5
            if pinEligibleMan.isCPU():
                if self._strategyPinChart:
                    pri1 = priVal
                    man2 = self._getMenIn()[not pinEligibleMan.getTeamNum()]
                    if self._tagTeam:
                        pri2 = man2.getTagTeamPriority() *  5.0 / 3
                    else:
                        pri2 = man2.getTagTeamPriority()
                    score1, score2 = self._totalScore
                    pMod = pinModifier + self._ref
                    prob = \
                         self._strategyPinChart.getPositiveProbability(score1,
                                                                       pMod)
                    pinPercentage = getPinPercentage(pri1, score1, pri2,
                                                     score2, prob)
                else:
                    # Pin group * 7 = base toPin percentage
                    #  pinBonus is added to base toPin percentage to get the
                    #  total pin percentage
                    pinPercentage = self._getPinGroup(pinEligibleMan) * 7 + \
                                    pinBonus
                if self._percentageDie.roll() <= pinPercentage:
                    points = self._goForPin(pinEligibleMan, pinModifier)
                    self._totalScore[pinEligibleMan.getTeamNum()] += points
            else:
                probs = None
                tScore = self._totalScore[pinEligibleMan.getTeamNum()]
                if self._strategyPinChart:
                    pMod = move.get("PIN_MODIFIER", 0)
                    probs = \
                            self._strategyPinChart.getProbabilities(tScore,
                                                                    self._ref,
                                                                    pMod)
                else:
                    move =  self._roundResults[pinEligibleMan.getTeamNum()][-1]
                    pMod = move.get("PIN_MODIFIER", 0)
                    pGroup = self._getPinGroup(pinEligibleMan)
                    probs = getPinProbability(pGroup, self._ref, pMod)

                probs["ELIGIBLE_MAN_SCORE"] = int(tScore)
                otherScore = self._totalScore[not pinEligibleMan.getTeamNum()]
                probs["VICTIM_SCORE"] = int(otherScore)
                peMan = pinEligibleMan.getName()
                layoutPrompt = "Should %s attempt a pin?" % peMan
                tblLayout = util.layoutPinAttemptDialog(layoutPrompt, probs,
                                                        peMan)

                pinResult = self._sendMessage("YES_OR_NO_PROMPT",\
                                              man=pinEligibleMan,
                                              layout=tblLayout,
                                              caption="Pin Attempt")
                if pinResult:
                    points = self._goForPin(pinEligibleMan, pinModifier)
                    self._totalScore[pinEligibleMan.getTeamNum()] += points

        self._sendMessage("TIME", minutes=self._round)
        
        if not self._endMatch:
            self._sendMessage("SCORE", teams=self._teams,
                              scores=self._totalScore, scoretype="TOTAL")
               
        self._round += 1
        # Draw
        if self._round > self._timeLimit and not self._endMatch:
            self._endMatch = True

        if self._endMatch:
            self._sendMessage("FINISH", finishlist=self._finishList, time=
                              self._round - 1)
        self._sendMessage("ROUND_BORDER", start=0)
        
        # If match is not over and it's a tag match, check for tag out
        #  opportunity
        if not self._endMatch and self._tagTeam and \
           self._doubleTeamRoundCounter < 1:
            w1, w2 = self._getMenIn()
            self._tagOutCheck(w1, roundScore)
            self._tagOutCheck(w2, roundScore)

        # Decrement double team round counter
        if not self._endMatch and self._doubleTeamRoundCounter > 0:
            self._doubleTeamRoundCounter -= 1
            if self._doubleTeamRoundCounter:
                dters = string.join(map(lambda x: "%s,"%x.getName(),
                                        self._doubleTeamList))[:-1]
                
                self._sendMessage("GENERIC_MESSAGE", message= dters + \
                              " are double teaming for %d more rounds." %\
                              (self._doubleTeamRoundCounter))
            else:
                self._sendMessage("DOUBLE_TEAM_STATUS", man=None, status=None,
                                  doubleTeamRound=0)
                self._doubleTeamList = []
                              
        # Decrement injury counters and reset base pin status
        if not self._endMatch:
            for team in self._teams:
               for m in team:
                   m.setPinStatus(1)  # Pin Status
                   injRounds = m.getInjuryRounds()
                   if injRounds > 0:
                       m.setInjured(injRounds - 1)                      
                       self._sendMessage("INJURY_STATUS", man=m,
                                         injuryRound=injRounds-1,
                                         start=0)
            
        self._state = UNRESOLVED_GC_ROLL
            

    def _getPinEligibility(self, roundScore):
        self._currentTeam = 0
        teamCount = 0
        pinAttemptMan = None
        pinEligibleMan = None
        pinModifier = 0
        
        if self._doubleTeamRoundCounter < 1 and not self._endMatch:
            while(not pinAttemptMan and not pinEligibleMan and teamCount < 2):

                team = self._currentTeam

                move =  self._roundResults[team][-1]
                if move["MOVE_POINTS"] > 0 and move["MOVE_TYPE"] == PA:
                    pinModifier = 0
                    pinAttemptMan = self._getManIn()
                    # If using strategy pin chart flag man as eligible
                    # for a pin if a P/A was rolled
                    if self._strategyPinChart:
                        pinAttemptMan = None
                        pinEligibleMan = self._getManIn()
                        
                    if move.has_key("PIN_MODIFIER"):
                       pinModifier = move["PIN_MODIFIER"]

                if self._totalScore[team] - \
                   self._totalScore[self._getOtherTeam()] > 9 and \
                   roundScore[team] - roundScore[self._getOtherTeam()] > 4 and \
                   self._totalScore[team] > 30 and \
                   self._getManIn().pinStatus():

                    if self._onlyPinOnPA:
                        pinEligibleMan = None
                    else:
                        pinEligibleMan = self._getManIn()

                self._currentTeam = self._getOtherTeam()
                teamCount += 1

        return pinAttemptMan, pinEligibleMan, pinModifier
                
    def _goForPin(self, wrestler, modifier=0, num_reversals=0,
                  reverse_score=0):
        finishMade = False
        self._currentTeam = wrestler.getTeamNum()
        saveMade = saverName = False
        strategyChart = 0
        numReversals = num_reversals
        pinIsReversed = 0
        pManTotalScore = 0

        self._sendMessage("PIN_ATTEMPT", man=wrestler)
        modifierTotal = modifier + self._ref
        if not self._strategyPinChart:
            pGroup = self._getPinGroup(wrestler)
            pRoll = self._getPinRoll(wrestler, modifierTotal)
            pScore = self._getPinScore(pRoll, pGroup)
        else:
            if reverse_score > 0:
                pManTotalScore = reverse_score
            else:
                pManTotalScore = self._totalScore[wrestler.getTeamNum()]
            pGroup, pRoll, pScore, pinIsReversed = \
                    self._doStrategyPinRoll(wrestler, pManTotalScore, modifier,
                                            numReversals)
            if pinIsReversed:
                numReversals += 1
                    
        self._currentTeam = self._getOtherTeam()
        pinVictim = self._getManIn()
        if pScore >= 17:
            if self._tagTeam:
               saveMade,saverName = self._saveAttempt(pinVictim.getTeamNum())

            if not saveMade:
                loser = pinVictim
                move = self._roundResults[wrestler.getTeamNum()][-1]
                finishMade = True

            pScore = 0

        self._sendMessage("PIN_RESULT", aggressor=wrestler,
                          victim=pinVictim, finished=finishMade, save=saveMade,
                          saveman=saverName, points=pScore, roll=pRoll,
                          group=pGroup, strat_chart=strategyChart,
                          pin_reversal=pinIsReversed)

        points = pScore

        if finishMade:
            self._endMatch = True
            self._finishList.append({"WINNER":wrestler,
                                     "MOVE": move,
                                     "LOSER": loser})
        if pinIsReversed:
            self._reversalMan = pinVictim
            revPoints = self._goForPin(pinVictim, 0, numReversals,
                                       reverse_score=pManTotalScore)
            team = self._reversalMan.getTeamNum()
            self._totalScore[team] += revPoints
            points = 0
        
        return points
    
    def _doStrategyPinRoll(self, wrestler, score, modifier, num_reversals):
        pGroup = self._strategyPinChart.getPinGroup(score)
        pRoll = self._getPinRoll(wrestler, modifier + self._ref)
        pScore = self._strategyPinChart.getPinChartResult(score, pRoll)

        pinIsReversed = 0
        if pScore in [RSTAR, R]:
            if pScore == R and num_reversals > 1:
                pScore = 10
            else:
                pinIsReversed = 1

        return pGroup, pRoll, pScore, pinIsReversed
        
    def _goForSubmission(self, wrestler):
        finishMade = False
        self._currentTeam = wrestler.getTeamNum()
        saveMade = saverName = False
        origCurrentTeam = self._currentTeam
        mv = move = self._roundResults[wrestler.getTeamNum()][-1]
        self._sendMessage("SUBMISSION", man=wrestler, move=mv)
        self._currentTeam = self._getOtherTeam()
        submitVictim = self._getManIn()

        if submitVictim.submits():
            if self._tagTeam:
               saveMade,saverName=self._saveAttempt(submitVictim.getTeamNum())

            if not saveMade:
                finishMade = True
                loser = submitVictim

        self._sendMessage("SUBMISSION_RESULT",victim=submitVictim,
                          finished=finishMade,save=saveMade,
                          saveman=saverName)

        self._currentTeam = origCurrentTeam

        if finishMade:
            self._endMatch = True
            self._finishList.append({"WINNER":wrestler,
                                     "MOVE": move,
                                     "LOSER": loser,
                                     "SUBMISSION":1})
        
    def _goForDQ(self, wrestler, alttext=None, print_score=1, altresult=None):
        finishMade = False
        self._currentTeam = wrestler.getTeamNum()
        
        tmpCurrTeam = self._currentTeam
        self._currentTeam = self._getOtherTeam()
        countOutVictim = self._getManIn()
        if self._dqEnabled: self._sendMessage("DQ", victim=countOutVictim,
                                              text=alttext)
        points = countOutVictim.roll2D6() + 2
            
        if points > 9 and self._dqEnabled:
            finishMade = True
            for move in self._roundResults[wrestler.getTeamNum()]:
                if  move['MOVE_TYPE'] == DQ and move['MOVE_POINTS'] == DQ:
                    move["MOVE_NAME"] += " - Count Out"
                    loser = countOutVictim
                    points = 10
        else:
            finishMade = False

        self._sendMessage("DQ_RESULT", victim=countOutVictim,
                          finished=finishMade,count=points,aggressor=wrestler,
                          dqEnabled=self._dqEnabled, print_score=print_score,
                          text=altresult)

        self._currentTeam = tmpCurrTeam

        if finishMade:
            self._endMatch = True
            self._finishList.append({"WINNER":wrestler,
                                     "MOVE": move,
                                     "LOSER": loser,
                                     "COUNTOUT":1})

        return points
        

    def _getPinGroup(self, wrestler):
        pinGroup = 0
        if self._totalScore[wrestler.getTeamNum()] % 10 == 0:
            pinGroup = -1

        pinGroup += int(self._totalScore[wrestler.getTeamNum()] / 10)

        if pinGroup > 14: pinGroup = 14
       
        return pinGroup

    def _getPinRoll(self, wrestler, modifier=0):
        self._sendMessage("GENERIC_PROMPT", prompt="%s Roll for pin > " % \
                          wrestler.getName(), man=wrestler, type=PA)

        return wrestler.roll2D6() + modifier

    def _getPinScore(self, pinRoll, pinGroup):
        pinScore = 0
        if pinRoll < 0: pinRoll = 0
        elif pinRoll > 10: pinRoll = 10
        for term in range(0, len(_PcTable[pinRoll])):
            pinScore += _PcTable[pinRoll][term] * pow(pinGroup, term)

        return round(pinScore)
       
    def _getHigherMan(self, w1, w2):
        if self._tagTeam:
            w1Pri = w1.getTagTeamPriority()
            w2Pri = w2.getTagTeamPriority()
        else:
            w1Pri = w1.getSinglesPriority()
            w2Pri = w2.getSinglesPriority()

        cVal = cmp(w1Pri, w2Pri)
        if cVal > 0: highMan = w1
        elif cVal < 0: highMan = w2
        else:
            cVal = cmp(self._totalScore[w1.getTeamNum()] + w1Pri,
                       self._totalScore[w2.getTeamNum()] + w2Pri)
            if cVal > 0: highMan = w1
            elif cVal < 0: highMan = w2
            else:
                teamNum = self._oneD6.roll() % 2
                if teamNum == 0: highMan = w1
                else: highMan = w2

        return highMan

    def _submissionCheck(self, w):
        for move in self._roundResults[w.getTeamNum()]:
            if move["MOVE_TYPE"] == SUBMISSION and move["MOVE_POINTS"] > 0 and \
               self._doubleTeamRoundCounter < 1:
                w.setPinStatus(0)
                self._goForSubmission(w)


    def _dqCheck(self, w):
        # countOut flag is used to determine if a team ( w.getTeamNum() )  has
        #  scored a count out in the current round.
        countOut = False
        for move in self._roundResults[w.getTeamNum()]:
            # If team already has already scored a countout, there is no need
            # to try and score another.  The following if block takes care of
            # this.
            if move["MOVE_TYPE"] == DQ and move["MOVE_POINTS"] == DQ and \
               not countOut:
                w.setPinStatus(0)
                points = self._goForDQ(w)
                if points > 9 and self._dqEnabled:
                    # There should be no points added to the team's total score
                    # if a countout occurs so set the DQ's move points to
                    # zero.
                    move["MOVE_POINTS"] = 0
                    countOut = True
                else: move["MOVE_POINTS"] = points

    
    def _saveAttempt(self, team):
        menOut = self._getMenOut(team)
        maxTagRange = 0
        saver = None
        saverName = None
        eligibleMenOut = []
        
        if self._getManIn().isCPU():
            for man in menOut:
                tagRange = len(man.getTagTeamRange())
                if tagRange >= maxTagRange and man.getInjuryRounds() < 1:
                    maxTagRange = tagRange
                    saver = man
        else:
            tmpMenOut = []
            for man in menOut:
                if man.getInjuryRounds() < 1:
                   eligibleMenOut.append(man)
            if len(eligibleMenOut) > 1:
                for man in eligibleMenOut:
                    tr = man.getTagTeamRange()
                    tmpMenOut.append("%s (%d-%d)" % (man.getName(),
                                                     tr[0], tr[-1]))
                idx = self._sendMessage("CHOICE_LIST",
                                        prompt="Select man out to make save:",
                                        choicelist=tmpMenOut,man=self._getManIn(),
                                        caption="Save Attempt")
                saver = eligibleMenOut[idx]
            else:
                saver = eligibleMenOut[0]
                
        if saver:
            saveMan = saver
            saverName = saveMan.getName()
            saver = saver.makeSave()
            self._sendMessage("MAKE_SAVE", saveman=saveMan)
        
        return saver, saverName

    def _tagOutCheck(self, w, rndScore):
        manCount = 1
        tagOutList = []
        tagEligible = False
        self._currentTeam = w.getTeamNum()
        tagEligible = self._getTagEligibility(w, rndScore)

        if tagEligible and not w.isCPU():
            tmpTagList = ["No tag"]
            for man in self._getMenOut(w.getTeamNum()):
               if man.getInjuryRounds() < 1:
                   tagOutList.append(man)
                   tmpTagList.append(man.getName())
                   manCount += 1
            if len(tagOutList) > 0:
                tagOutManIdx = self._sendMessage("CHOICE_LIST",
                                                 prompt="Tag out to:",
                                                 choicelist=tmpTagList,man=w,
                                                 caption="Tag Out", tagout=1)
                tagOutManIdx -= 1

                if tagOutManIdx > -1:
                    tagOutMan = tagOutList[tagOutManIdx]
                    self._manIn[w.getTeamNum()] = tagOutMan
                    msg = "%s tags out to %s\n"%(w.getName(), tagOutMan.getName())
                    self._sendMessage("NEW_MAN_IN", message=msg, new_man_in=tagOutMan)
                    
        elif tagEligible and w.isCPU():
            tagModifier = (rndScore[self._getOtherTeam()] - \
                           rndScore[w.getTeamNum()]) * 1.5
            tagOutRoll = self._percentageDie.roll() + tagModifier

            if tagOutRoll > 50:
                for man in self._getMenOut(w.getTeamNum()):
                    if man.getInjuryRounds() < 1:
                        tagOutList.append(man)
                        manCount += 1
                if len(tagOutList) > 0:
                    tagOutMan = tagOutList[random.randint(0, len(tagOutList)-1)]
                    self._manIn[w.getTeamNum()] = tagOutMan
                    msg = "%s tags out to %s\n" % (w.getName(),tagOutMan.getName())
                    self._sendMessage("NEW_MAN_IN", message=msg, new_man_in=tagOutMan)


    def _getTagEligibility(self, w, rndScore):
        tagPri = w.getTagTeamPriority()
        otherTeamRndScore = rndScore[not w.getTeamNum()]
        tagEligible = False
        if tagPri >= 3:
            tagEligible = True
        elif tagPri == 2 and rndScore[w.getTeamNum()] >= otherTeamRndScore:
            tagEligible = True
        elif tagPri == 1 and rndScore[w.getTeamNum()] > otherTeamRndScore:
            tagEligible = True

        return tagEligible
    
    def _handleManInMove(self, ra, rms):
        roundAction = ra
        roundMoveStatus = rms
        reversalFlag = False
        manIn = self._getManIn()
        offOnlyFlag = False
        
        # The following if block sets the offenseOnly flag which is passed
        #  to the interface object.
        if DC not in self._genCardResults:
           offOnlyFlag = True
           
        cardVal = self._genCardResults[self._currentTeam]

        if (cardVal in (OC, OCTT)):
            roundMoveStatus.append(OC)
            roundAction[self._currentTeam].append(self._runOffense(manIn))

            # After reversing a double-team, the doubleTeamers will be on
            #  defense.  However we'll set the offense only flag, since
            #  the double-teamers moves have already been executed.
            if self._doubleTeamRoundCounter > 0:
                if OC not in self._dtGenCardResults: offOnlyFlag = True
            
        elif (cardVal == DC and (OC in roundMoveStatus or self._doubleTeamRoundCounter > 0)):
            roundMoveStatus.append(DC)
            roundAction[self._currentTeam].append(self._runDefense(manIn))
            if (roundAction[self._currentTeam][-1]["MOVE_NAME"]=="REVERSE"):
                self._genCardResults[self._currentTeam] = OC

                if self._doubleTeamRoundCounter > 0:
                    dtGCResults = self._dtGenCardResults
                    for x in range(len(dtGCResults)): dtGCResults[x] = DC

                self._genCardResults[self._getOtherTeam()] = DC

                for x in range(len(roundAction[self._getOtherTeam()])):
                    roundAction[self._getOtherTeam()][x]["MOVE_POINTS"] = 0

                reversalFlag = True
                roundMoveStatus = []
            elif (roundAction[self._currentTeam][-1]["MOVE_NAME"] == "C"):
                for x in range(len(roundAction[self._getOtherTeam()])):
                    roundAction[self._getOtherTeam()][x]["MOVE_POINTS"] = 0

        elif cardVal == INJURED:
            roundMoveStatus.append(DC)
            roundAction[self._currentTeam].append({"MOVE_NAME":"INJURED",
                                                   "MOVE_POINTS": 0,
                                                   "MOVE_TYPE": DEFENSIVE,
                                                   "WRESTLER": manIn.getName(),
                                                   "PIPS":[]})
##        /* DEBUG CODE */
##        elif (cardVal == DC and OC not in roundMoveStatus and \
##              self._doubleTeamRoundCounter > 0):
##            print "SOMETHING HAS GONE AWRY!!!"
##            print manIn.getName()
##            print "cardVal:", cardVal
##            print "roundMoveStatus", roundMoveStatus
##            print "roundAction", roundAction
##            print "Running Defense"

        
        if len(roundAction[self._currentTeam]):
            m = roundAction[self._currentTeam][-1]
            otherTmMoves = roundAction[self._getOtherTeam()]
            if self._doubleTeamRoundCounter > 0 and len(otherTmMoves):
                otherTmMoves = otherTmMoves[-len(self._doubleTeamList):]
            elif len(otherTmMoves):
                otherTmMoves = roundAction[self._getOtherTeam()][-1:]
            else:
                otherTmMoves = []

            # This if-then block will handle the case where both men in roll
            #  OC or OC/TT.  
            specMoveCheck = False
            if (self._genCardResults[0] in (OC, OCTT) and self._genCardResults[1] in (OC, OCTT)) \
                and self._doubleTeamRoundCounter < 1 and self._specMoveCheckNeeded:
                moveType = roundAction[self._currentTeam][-1]["MOVE_TYPE"]

                # If both men in rolled a P/A, *, or (S) see which man's move
                #  takes precedence
                if moveType in (PA, SUBMISSION, SPECIALTY):
                    currManIn = self._getManIn()
                    self._currentTeam = self._getOtherTeam()
                    otherManIn = self._getManIn()
                    specMoveCheck = True
                    self._specMoveRolls += 1
                    self._specMoveCheckNeeded = True
                    
                    # Return current team to currManIn's team
                    self._currentTeam = self._getOtherTeam()

                    if (self._tagTeam):
                        currPri = currManIn.getTagTeamPriority()
                        otherPri = otherManIn.getTagTeamPriority()
                    else:
                        currPri = currManIn.getSinglesPriority()
                        otherPri = otherManIn.getSinglesPriority()
                    
                    if currPri < otherPri and len(otherTmMoves):
                        m["MOVE_POINTS"] = 0
                    elif currPri == otherPri and len(otherTmMoves):
                        m["MOVE_POINTS"] = 0
                        otherTmMoves[0]["MOVE_POINTS"] = 0
                    elif len(otherTmMoves):
                        otherTmMoves[0]["MOVE_POINTS"] = 0

                # If it's not a special move and a special move has already been rolled,
                #  set the specMoveCheck flag so that the output can be displayed
                #  properly by the interface.
                elif self._specMoveRolls:
                    specMoveCheck = True
                else:
                    self._specMoveCheckNeeded = False
                    specMoveCheck = False
               
            self._sendMessage("MOVE_ATTEMPT", move=m, offenseOnly=offOnlyFlag,
                              otherTeamMoves=otherTmMoves, team=self._currentTeam,
                              specmove_check=specMoveCheck)

        return {"ROUND_ACTION": roundAction,
                "REVERSAL_FLAG": reversalFlag,
                "ROUND_MOVE_STATUS": roundMoveStatus}
        
    def _handleDoubleTeamMoves(self, ra, rms):
        # This function should run offense and defense for the double teamers.
        # If allInRing is set then run offense for both teams
        roundAction = ra
        roundMoveStatus = rms
        
        if self._allInRing:
            roundMoveStatus = [OC, OC]
            for t in (0,1):
                for m in self._teams[t]:
                    if m.getInjuryRounds() < 1:
                        lastForTeam = m == self._teams[t][-1]
                        self._sendMessage("DOUBLE_TEAM_STATUS", man=m, status=OC, \
                                          doubleTeamRound=1, lastman=lastForTeam)
                        roundAction[t].append(self._runOffense(m))
                        self._sendMessage("MOVE_ATTEMPT", move=roundAction[t][-1],\
                                          offenseOnly=True, team=t)
        else:
            manCount = 0
            offOnly = False
            if OC not in self._dtGenCardResults: roundMoveStatus.append(DC)
            else: roundMoveStatus.append(OC)

            if DC not in self._genCardResults:
                offOnly = True
                
            self._currentTeam = self._doubleTeamList[0].getTeamNum()
            #print "double team number:", self._currentTeam
            #print self._dtGenCardResults
            for man in self._doubleTeamList:
                team = man.getTeamNum()
                m = man
                dtResult = self._dtGenCardResults[manCount]
                self._sendMessage("DOUBLE_TEAM_STATUS", man=m, status=dtResult, \
                                  doubleTeamRound=self._doubleTeamRoundCounter)
                if dtResult in (OC, OCTT):
                    roundAction[team].append(self._runOffense(man))
                elif dtResult == DC:
                    roundAction[team].append({"MOVE_NAME":"ON DEFENSE",
                                              "MOVE_POINTS":0,
                                              "MOVE_TYPE":DEFENSIVE,
                                              "WRESTLER":man.getName(),
                                              "PIPS":[]})
                manCount += 1
                self._sendMessage("MOVE_ATTEMPT",move=roundAction[team][-1], \
                                  offenseOnly=offOnly, team=team) 
        self._allInRing = False
        
        return {"ROUND_ACTION": roundAction,
                "ROUND_MOVE_STATUS": roundMoveStatus}
                        
                   

    def runMatch(self):
        retVal = 0
        refStr = "Referee is %s" % self.getRef()
        self._sendMessage("GENERIC_MESSAGE", message=refStr+"\n\n")
        while (not self._endMatch):
            self._rollDice()
            self._resolveMoves()
            self._endMatchCheck()
            if not self._endMatch:
                self._sendMessage("ROUND_START_PROMPT")

        # DEBUG - DQ count
        for finish in self._finishList:
            if finish["MOVE"]["MOVE_TYPE"] == DQ:
               retVal = 1

        self._sendMessage = None
        self._matchRunning = False
        self._resultController = None
        self._signalQueue.put(MATCH_STOPPED)
        

class SPW_SpecialtyMatch(Match):
    def __init__(self, team1, team2, timeLimit=60, network=0, dqEnabled=0):
        Match.__init__(self, team1, team2, dqEnabled=0,
                           timeLimit=timeLimit, network=network)
        self._setEventChart()
        self._pinScored = [0,0]
        self._pinRoundCounter = 0
        self._refIncapRounds = 0
        self._oneD6 = Dice(5)
        self._bonuses = [[],[]]
        self._penalties = [[],[]]

    def _runOffense(self, wrestler):
        move = {}
        move.update(Match._runOffense(self, wrestler))
        if move["MOVE_TYPE"] == XX:
            w = wrestler
            self._sendMessage("HIGHLIGHT_CELL", team=w.getTeamNum(),
                              row=move["INDEX"] + OFFENSIVE_CARD_START_ROW + 1,
                              col=2, man=w)
            # roll on specialty chart
            msg = "%s Make %s Roll > " % (w.getName(), self._matchType)
            self._sendMessage("GENERIC_PROMPT",
                              prompt=msg, man=w, type=XX,
                              sound=self._specSound)

            move.update(self._eventChart[self._twoD6.roll()])
            msg = None
            if move.has_key("PIN_MODIFIER"):
                self._addBonus(w, w.setPinModifier, move["PIN_MODIFIER"],
                               "PIN_BONUS")
            elif move.has_key("SPECIALTY_ROLL"):
                specMove = {}
                self._sendMessage("GENERIC_PROMPT",
                                  prompt="%s Roll Specialty Card > " % \
                                  w.getName(), man=w, type=SPECIALTY)
                specMove.update(w.rollSpecialty())
                move["MOVE_NAME"] += " AND\n%s" % specMove["MOVE_NAME"]
                move["MOVE_TYPE"] = specMove["MOVE_TYPE"]
                move["MOVE_POINTS"] += specMove["MOVE_POINTS"]
            elif move.has_key("FOE_OC_PENALTY"):
                otherManIn = self._getMenIn()[not w.getTeamNum()]
                self._addPenalty(otherManIn, otherManIn.setOCPenalty,
                                 move["FOE_OC_PENALTY"], "OC_PENALTY")
            elif move.has_key("FOE_DC_ROUNDS"):
                otherManIn = self._getMenIn()[not w.getTeamNum()]
                if otherManIn.getDCRounds(): modifier = 0
                else: modifier = 1
                self._addPenalty(otherManIn, otherManIn.addDCRounds,
                                 move["FOE_DC_ROUNDS"] + modifier,
                                 "DC_ROUNDS")
            elif move.has_key("REF_INCAP_ROUNDS"):
                if not self._refIncapRounds:
                    self._refIncapRounds = move["REF_INCAP_ROUNDS"] + 1
            elif move.has_key("FINISH_ON_PIN"):
                self._addBonus(w, w.setFinishOnPin, True, "AUTO_PIN_BONUS")
            
        if wrestler.hasOCPenalty():
            move["MOVE_POINTS"] -= wrestler.getOCPenalty()

        return move
                                 
    def _promptGenRoll(self, w):
        dcRounds = w.getDCRounds()
        otherManIn = self._getMenIn()[not w.getTeamNum()]
        
        if dcRounds:
            self._sendMessage("HIGHLIGHT_CELL", col=0, row=DC_START_ROW,
                              man=w, team=w.getTeamNum())
            self._sendMessage("GENERAL_CARD_RESULT", man=w, result=DC,
                              index=INJURED, die_pips=[])

            return DC
        elif otherManIn.getDCRounds():
            self._sendMessage("HIGHLIGHT_CELL", col=2,
                              row=OFFENSIVE_CARD_START_ROW,
                              man=w, team=w.getTeamNum())
            self._sendMessage("GENERAL_CARD_RESULT", man=w, result=OC,
                              index=OC, die_pips=[])
            return OC        
        else:
            return Match._promptGenRoll(self, w)

    def _endMatchCheck(self):
        self._applyPenaltiesAndBonuses()
        self._clearPenaltiesAndBonuses()
        Match._endMatchCheck(self)

        if not self._endMatch:
            if self._pinRoundCounter:
                self._pinRoundCounter -= 1
                self._sendMessage("GENERIC_MESSAGE",
                                  message=self._pinVictim.getName() + \
                                  " has %d more rounds to score a pin or submission." %\
                                  (self._pinRoundCounter))
                if not self._pinRoundCounter:
                    winner = self._getMenIn()[not self._pinVictim.getTeamNum()]
                    self._doFinish(winner, self._pinVictim)
                    self._sendMessage("FINISH", finishlist=self._finishList,
                                      time=self._round - 1)
                    return
                    
            if self._refIncapRounds:
                self._refIncapRounds -= 1
                if self._refIncapRounds:
                    self._sendMessage("GENERIC_MESSAGE", message="Referee is " + \
                                      "incapacitated for %d more rounds." %\
                                      (self._refIncapRounds))
                else:
                    self._sendMessage("GENERIC_MESSAGE", message="Referee is " + \
                                      "no longer incapacitated.")
                    

            for man in self._getMenIn():
                if man.getDCRounds():
                    man.popDCRound()  # Decrement dc rounds
                    if man.getDCRounds():
                        self._sendMessage("GENERIC_MESSAGE",
                                          message=man.getName() + \
                                          " is on defense for %d more rounds." %\
                                          man.getDCRounds())
                    else:
                        self._sendMessage("GENERIC_MESSAGE",
                                          message=man.getName() + \
                                          " is no longer on defense.")
                        


    def _goForPin(self, wrestler, modifier=0, num_reversals=0,
                  reverse_score=0):
        points = Match._goForPin(self, wrestler, wrestler.getPinModifier(),
                                 num_reversals, reverse_score)
        wrestler.setPinModifier(0)
        wrestler.setFinishOnPin(False)
        self._checkForFinish(wrestler)
        return points

    def _checkForFinish(self, wrestler): pass            
    def _doFinish(self, agressor, victim): pass

    def _tagOutCheck(self, w, rndScore):
        Match._tagOutCheck(self, w, rndScore)
        if self._getMenIn()[w.getTeamNum()] != w:
            w.clearDCRounds()
            
    def _getTagEligibility(self, w, rndScore):
        tagPri = w.getTagTeamPriority()
        otherTeamRndScore = rndScore[not w.getTeamNum()]
        tagEligible = False
        if tagPri >= 3 and w.getDCRounds() < 2:
            tagEligible = True
        elif tagPri == 2 and \
                 rndScore[w.getTeamNum()] >= otherTeamRndScore and \
                 w.getDCRounds() < 2:
            tagEligible = True
        elif tagPri == 1 and \
                 rndScore[w.getTeamNum()] > otherTeamRndScore and \
                 w.getDCRounds() < 2:
            tagEligible = True

        return tagEligible

    def _handleManInMove(self, ra, rms):
        manIn = self._getManIn()
        manInMove = {}
        move = None
        moveName = None
        manInMove.update(Match._handleManInMove(self, ra, rms))
        manInRoundAction = manInMove["ROUND_ACTION"][self._currentTeam]
        otherManIn = self._getMenIn()[not manIn.getTeamNum()]

        if len(manInRoundAction):
            move = manInRoundAction[-1]
            moveName = move["MOVE_NAME"]

        if moveName in ("REVERSE", "C") and \
           (OC in rms or self._doubleTeamRoundCounter > 0):
                self._clearPenalties(manIn.getTeamNum())
                self._clearBonuses(not manIn.getTeamNum())


        return manInMove

    def _setEventChart(self): raise NotImplementedError
        
    def _addBonus(self, w, modifierfunc, funcarg, bonustype):
        team = w.getTeamNum()
        self._bonuses[team].append((w, modifierfunc, funcarg, bonustype))

    def _addPenalty(self, w, modifierfunc, funcarg, pentype):
        team = w.getTeamNum()
        self._penalties[team].append((w, modifierfunc, funcarg, pentype))

    # The following method should only be called when an
    #  Offensive move has been reversed or neutralized
    def _clearBonuses(self, team):
        self._bonuses[team] = []

    # The following method should only be called when an
    #  Offensive move has been reversed or neutralized
    def _clearPenalties(self, team):
        self._penalties[team] = []

    def _removePenalties(self, team, indices):
        newPenalties = []
        idx = 0
        for penalty in self._penalties[team]:
            if idx not in indices:
                newPenalties.append(penalty)
            idx += 1
            
        self._penalties[team] = newPenalties
        
    def _applyPenaltiesAndBonuses(self):
        w1, w2 = self._getMenIn()
        dc1 = self._checkForDCPenaltyRemoval(w1)
        dc2 = self._checkForDCPenaltyRemoval(w2)
        self._removePenalties(w1.getTeamNum(), dc1)
        self._removePenalties(w2.getTeamNum(), dc2)
        
        for modlist in self._penalties: self._applyModifierFunc(modlist)

        for modlist in self._bonuses: self._applyModifierFunc(modlist)

    def _applyModifierFunc(self, modlist):
        for w, func, funcarg, mtype in modlist:
            func(funcarg)            

    def _clearPenaltiesAndBonuses(self):
        self._penalties = [[],[]]
        self._bonuses = [[],[]]
        
    def _checkForDCPenaltyRemoval(self, w):
        """Remove any DC Penalties if the wrestler executed a move
           which resulted in a DC Penalty for the other team"""
        otherTeam = not w.getTeamNum()
        penIndices = []
        idx = 0
        for wrestler, func, parg, ptype in self._penalties[otherTeam]:
            if ptype == "DC_ROUNDS":
                if w.getDCRounds() > 1:
                    w.clearDCRounds()
                    w.addDCRounds(1)    # Needed for endMatchCheck()
                for w, func, parg, ptype in self._penalties[w.getTeamNum()]:
                    if ptype == "DC_ROUNDS":
                        penIndices.append(idx)
                    idx += 1
                
                break
        return penIndices
        
        


UNRESOLVED_GC_ROLL = 250
UNRESOLVED_MOVES = 251
END_MATCH_CHECK = 252

FREE = 0
BUSY = 1
#from twisted.flow import flow
#from twisted.flow.threads import Threaded
import Queue
class ResultController:
    def __init__(self, resultQ, messageQ):
        self.resultQueue = resultQ
        self.messageQueue = messageQ
        self.waitForResult = True
        
    def getResult(self, msg, **kw):
        if not self.waitForResult: return 0
        self.messageQueue.put((msg, kw))
        return self.resultQueue.get()

def getPinPercentage(pri1, score1, pri2, score2, goodprobs):
    scoreDiff = score1 - score2    
    priDiff = pri1 - pri2
    isLosing = 0
    if scoreDiff < 0:
        isLosing = 1
        scoreDiff = abs(scoreDiff)
    
    # Desperation Calculation
    desperation = 0
    despBase = abs(scoreDiff / 10)
    lpd = LP_DESPERATION
    lhpd = LHP_DESPERATION
    whpd = WHP_DESPERATION
    if despBase > 3: despBase = 3
    
    if isLosing and scoreDiff > 9 and goodprobs > 0:
        lastTerm = -8.743E-15 * pow(despBase, 2)
        if priDiff < 0:
            # Wrestler's with a lower priority are more "desperate"        
            scaler = abs(priDiff) * lpd
        else:
            scaler = lhpd * pri1 - lhpd * (priDiff)
        desperation = (despBase - 1 + lastTerm) * scaler
    elif scoreDiff > 9 and goodprobs > 0:
        lastTerm = -8.743E-15 * pow(despBase, 2)
        if priDiff < 0:
            scaler = abs(priDiff) * lpd
        else:
            scaler = whpd * pri1 - whpd * (priDiff)
        desperation = (despBase - 1 + lastTerm) * scaler
    # End Desperation Calculation

    if scoreDiff > 30: scoreDiff = 30
    pinAttemptChance = 0
    if scoreDiff > 9 and goodprobs > 0:
        pinAttemptChance = -30 + 3.5 * scoreDiff - .05 * \
                           pow(scoreDiff, 2)
    return goodprobs + pinAttemptChance + desperation
    
def getPinProbability(pGroup, refmodifier, pinmodifier):
    """Get the probability of a pin when *NOT* using the Strategy Pin Chart"""
    
    threshold = PIN_GROUP_POINT_RANGES[pGroup] + 1
    twoD6Probs = TWOD6_PROBABILITIES
    probDict = {"PIN_PROBABILITY":0, "REF_MODIFIER":refmodifier,
                "PIN_MODIFIER":pinmodifier}

    modifierTotal = refmodifier + pinmodifier
    threshold -= modifierTotal
    if threshold > len(twoD6Probs):
        probDict["PIN_PROBABILITY"] = 0.0
    elif threshold < 0:
        probDict["PIN_PROBABILITY"] = 100.0
    else:
        for prob in twoD6Probs[threshold:]:
            probDict["PIN_PROBABILITY"] += prob

    return probDict
    
    
def setupMatch(arg, wrestler=None):
        dqs = 0
        for matchCount in range(0,10000):
            team1 = []
            team2 = []
            from Wrestlers import AndreTheGiant
            andre = Wrestler(AndreTheGiant)
            andre.setTeamNum(1)
            andre.setCPU(True)
            team2.append(andre)

            from Wrestlers import RickMartel
            rick = Wrestler(RickMartel)
            rick.setTeamNum(1)
            rick.setCPU(True)
            team2.append(rick)

            from Wrestlers import RoadWarrior_Animal
            anim = Wrestler(RoadWarrior_Animal)
            anim.setTeamNum(0)
            anim.setCPU(True)
            team1.append(anim)
            
            from Wrestlers import RoadWarrior_Hawk
            hawk = Wrestler(RoadWarrior_Hawk)
            hawk.setTeamNum(0)
            hawk.setCPU(True)
            team1.append(hawk)

            from Wrestlers import RoadWarrior_Animal
            anim1 = Wrestler(RoadWarrior_Animal)
            anim1.setTeamNum(1)
            anim1.setCPU(True)
            #team2.append(anim1)

            from Wrestlers import RoadWarrior_Hawk
            hawk1 = Wrestler(RoadWarrior_Hawk)
            hawk1.setTeamNum(1)
            hawk1.setCPU(True)
            #team2.append(hawk1)

            #from lib import Networking
            from lib import Interface
            
            if arg == "server":
               srv = Networking.JowstServer('localhost', 400)
            elif arg == "client":

                interFace = Interface.BaseInterface(noSleep=1)
                if wrestler == "hawk": w = hawk
                else: w = rick
                c = Networking.JowstClient(('localhost', 50400),
                                           interFace.sendMessage,
                                           w)
            
            if arg == "server":
               import msvcrt
               print "Hit any key to Start Match"
               while(not msvcrt.kbhit()):
                  asyncore.poll()
                  
               match = Match([rick], [hawk], srv.handle_message,)
               dqs += match.runMatch()
               print dqs
            elif arg == "client":
               asyncore.loop()
            else:
                import sys, time
                interFace = Interface.BaseInterface(noSleep=1, testing=1)
                match = Match(team1, team2, dqEnabled=0, timeLimit=120)
                match.setInterfaces(interFace._resultQueue,
                                    interFace._messageQueue,
                                    interFace._signalQueue)
                interFace._checkMessageQueue()
                try:
                    match.runMatch()
                    interFace._stopMatch = True
                except:
                    interFace._stopMatch = True
                    sys.exit()

def test_match(t1, t2):
    team1 = getTeamList(t1)
    team2 = getTeamList(t2)
    from lib import Interface
    import sys, time
    interFace = Interface.BaseInterface(noSleep=1, testing=1)
    match = Match(team1, team2, dqEnabled=1, timeLimit=120)
    match.setInterfaces(interFace._resultQueue,
                        interFace._messageQueue,
                        interFace._signalQueue)
    interFace._checkMessageQueue()
    try:
        match.runMatch()
        interFace._stopMatch = True
    except:
        interFace._stopMatch = True
        sys.exit()

def getTeamList(t1, t):
    tlist = []
    for mod in t1:
        w = Wrestler(mod)
        w.setTeamNum(t)
        w.setCPU(True)
        tlist.append(w)
    return tlist
        
#if __name__ == '__main__':
#    setupMatch(sys.argv[1], sys.argv[2])

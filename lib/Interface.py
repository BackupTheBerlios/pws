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

from data.globalConstants import *
from util import JOWST_PATH, getModules
from lib import spw
import string, time, sys, os, glob, Queue, threading

class BaseInterface:
    def __init__(self, enableDrama=0, testing=0):
        if enableDrama:
            self._drama = DramaQueen(1, 1, 1, 1)
        else:
            self._drama = DramaQueen(0, 0, 0, 0)
            
        self._testing = testing
        self._stopMatch = None
        self._resultQueue = ResultQueue()
        self._messageQueue = Queue.Queue()
        self._signalQueue = Queue.Queue()
        self._messageDict = {"GENERIC_MESSAGE":(self._printMessage, True),
                             "GENERIC_PROMPT":(self._genericPrompt, False),
                             "ROUND_BORDER":(self._printRoundBorder, True), 
                             "MOVE_ATTEMPT":(self._moveAttempt, True),
                             "GENERAL_CARD_RESULT":(self._generalCardResult, True),
                             "CHOICE_LIST":(self._choiceList, False),
                             "NEW_MAN_IN":(self._newManIn, True),
                             "DOUBLE_TEAM_START":(self._dtStart, True),
                             "DOUBLE_TEAM_STATUS":(self._dtStatus, True),
                             "YES_OR_NO_PROMPT":(self._yesOrNo, False),
                             "TIME":(self._printTime, True),
                             "SCORE":(self._printScore, True),
                             "FINISH":(self._finish, False),
                             "INJURY_STATUS":(self._injuryStatus, True),
                             "PIN_ATTEMPT":(self._pinAttempt, True),
                             "PIN_RESULT":(self._pinResult, True),
                             "SUBMISSION":(self._submission, True),
                             "SUBMISSION_RESULT":(self._submissionResult, True),
                             "FINISH_EVENT_MSG":(self._printFinishEventMsg, True),
                             "DQ":(self._dq, True), 
                             "DQ_RESULT":(self._dqResult, True),
                             "MAKE_SAVE":(self._makeSave, True),
                             "START_MATCH":(self._takeTeams, False),
                             "ROUND_START_PROMPT":(self._roundStartPrompt, False),
                             "CLEANUP_UI":(self._cleanupUI, False),
                             "DISCONNECT_MSG":(self._disconnectMsg, False),
                             "CHAT_MSG":(self._receiveChatMsg, False),
                             "TOO_MANY_CONNECTIONS":(self._tooManyConns, False),
                             "ENABLE_MENUS":(self._doEnableMenus, False),
                             "SHOW_POPUP_WIN":(self._showPopupWin, False),
                             "CLOSE_POPUP_WIN":(self._closePopupWin, False),
                             "HIGHLIGHT_CELL":(self._highlightCell, True),
                             "ENABLE_LABEL":(self._enableTextLabel, True),
                             "DISABLE_LABEL":(self._disableTextLabel, True),
                             }
        
        self._stringDict = {OC: "### %s rolled OC. ###",
                            OCTT: "### %s rolled OC/TT ###",
                            DC: "### %s rolled DC ###",
                            INJURED: "### %s is injured. ###",
                            "DT_MSG": "\n>>> %s double teaming for %d rounds. <<<",
                            "DT_STATUS":">>> %s is a %s double teamer. <<<",
                            "DT_END":">>> Double teaming ends. <<<",
                            "FINISH":"+++ %s wins with a %s over %s!!! +++",
                            "DRAW":"+++ After %s minutes, the match is declared a draw. +++",
                            "INJURY_START":"~~~| %s injured for %s rounds!!! |~~~",
                            "INJURY_STATUS":"~~~| %s is injured for %s more rounds. |~~~",
                            "INJURY_END":"~~~| %s is no longer injured. |~~~",
                            "PIN":"+++ %s was pinned by %s!!! +++",
                            "SUBMISSION":"+++ %s submits!!! +++",
                            "COUNTOUT":"+++ %s is counted out!!! +++"}


    def sendMessage(self, msg, **kw):
        func, putInQueue = self._messageDict[msg]
        if kw.has_key("callback"):
            self._resultQueue.cb = kw["callback"]
        apply(func, [], kw)
        if putInQueue: self._resultQueue.put(0)

    def setResultCB(self, resultCB):
        self._resultCB = resultCB
            
    def _checkMessageQueue(self):
        qChecker = threading.Thread(target=self._msgQueueChecker)
        qChecker.start()
        
    def _msgQueueChecker(self):
        while not self._stopMatch:
            if not self._messageQueue.empty():
                msg, kw = self._messageQueue.get()
                self.sendMessage(msg, **kw)
        
    def _sleeper(self, secs):
        if not self._noSleep:
            time.sleep(secs)
            
    def _printMessage(self, **kw):
        self._printText(kw['message'])
        
    # This method should be overridden if you want to change the behavior
    # EXTENDING THIS METHOD IS NOT RECOMMENDED!!!!!
    def _genericPrompt(self, **kw):
        if not kw['man'].isCPU():
            self._printText("%s " % kw['prompt'])
            self._getInput(kw)
        else:
            self._resultQueue.put(0)
            
    def _printRoundBorder(self, **kw):
        self._printText("=" * 79)
        self._printText()

    # This is poorly written and exposes some bad design in the match engine
    #  When the match engine is refactored this method should clean up significantly.
    def _moveAttempt(self, **kw):
        move = kw['move']
        man = kw['move']['WRESTLER']
        reversalFlag = False
        offenseOnly = kw['offenseOnly']
        specMoveCheck = False
        if kw.has_key('specmove_check'):
            specMoveCheck = kw['specmove_check']
        
        if kw.has_key("scorecard"):
            teamnum = kw['team']
            scorecard = kw['scorecard']
        else:
            scorecard = None

        # Handle offensive move
        if move['MOVE_TYPE'] != DEFENSIVE and not specMoveCheck:
            self._drama.dramaPause(.35)
            self._printText("%s executes a %s...." % (man, move['MOVE_NAME']))
            if offenseOnly and not move["MOVE_TYPE"] == DQ:
                self._printText("%s scores %d points.\n\n" % (man,
                                                            move['MOVE_POINTS']))
                if scorecard: scorecard.updateScore(teamnum, move['MOVE_POINTS'])
            else:
                self._printText()
        # Handle case where both men in potentially roll P/A, *, or (S)
        elif specMoveCheck:
            self._drama.dramaPause(.35)
            self._printText("%s executes a %s....\n\n" % (man, move['MOVE_NAME']))

            # Resolve scoring once both teams have executed moves.
            if len(kw["otherTeamMoves"]):
                offensiveMove = kw["otherTeamMoves"][-1]
                self._printText("%s scores %d points.\n\n" % (offensiveMove["WRESTLER"],
                                                              offensiveMove["MOVE_POINTS"]))
                # Update the scorecard for the team who executed the first offensive move
                if scorecard:
                    scorecard.updateScore(not teamnum, offensiveMove['MOVE_POINTS'])
                if move["MOVE_TYPE"] != DQ:
                    self._printText("%s scores %d points.\n\n" % (man,
                                                                  move["MOVE_POINTS"]))
                    # Update the scorecard for the team who executed the second offensive move                    
                    if scorecard: scorecard.updateScore(teamnum, move['MOVE_POINTS'])

        # Handle defensive move and offensive wrestler's move.                        
        else:
            # Handle offensive moves
            if kw.has_key("otherTeamMoves"):
                if len(kw["otherTeamMoves"]) > 1:
                    offensiveMoves = "Double Teaming."
                elif len(kw["otherTeamMoves"]) == 1:
                    offensiveMoves = kw["otherTeamMoves"][-1]["MOVE_NAME"]
            else:
                kw["otherTeamMoves"] = []

            # Handle defensive move
            if move['MOVE_NAME'] == 'A':
                dMove = "%s attempts to defend against %s but is unsuccessful."\
                      % (man, offensiveMoves)
            elif move['MOVE_NAME'] == 'B':
                dMove = "%s absorbs the punishment." % man
            elif move['MOVE_NAME'] == 'C':
                dMove = "%s neutralizes %s." % (man, offensiveMoves)
            elif move['MOVE_NAME'] == 'REVERSE':
                self._drama.dramaPause(1)
                self._printText("%s reverses %s!" % (man, offensiveMoves))
                reversalFlag = True
            elif move['MOVE_NAME'] == 'INJURED':
                dMove = "%s is injured and unable to defend himself." % man
            elif move['MOVE_NAME'] == 'ON DEFENSE':
                dMove = "%s does nothing for the round." % man

            # If there is no reversal print out the scores and update the
            #  scorecard
            if not reversalFlag:
                self._drama.dramaPause(.35)
                moveCount = 1
                for offensiveMove in kw["otherTeamMoves"]:
                    newlines = '\n'
                    offensiveMan = offensiveMove["WRESTLER"]
                    if moveCount == len(kw["otherTeamMoves"]):
                        newlines = '\n\n'
                    # The offenseOnly flag is set if the defensive wrestler
                    #  is injured.  If it is set make sure we don't give the
                    #  offensive wrestler double points for their offensive move.
                    if not offensiveMove["MOVE_TYPE"] == DQ and \
                           not offenseOnly:
                        self._printText("%s scores %d points.%s" % (offensiveMan, \
                                                       offensiveMove['MOVE_POINTS'],
                                                                    newlines))
                        if scorecard:
                            oTeam = not teamnum
                            scorecard.updateScore(oTeam,
                                                  offensiveMove['MOVE_POINTS'])
                    # If a DQ move was neutralized, give 0 points to the offensive move.
                    elif offensiveMove["MOVE_TYPE"] == DQ and \
                             move["MOVE_NAME"] == 'C':
                        self._printText("%s scores %d points.%s" % (offensiveMan, \
                                                                    0,
                                                                    newlines))
                        if scorecard:
                            oTeam = not teamnum
                            scorecard.updateScore(oTeam, 0)

                self._drama.dramaPause(.35)
                self._printText(dMove)
                self._printText("%s scores %d points.\n\n" % (man,
                                                              move['MOVE_POINTS']))
                if scorecard: scorecard.updateScore(teamnum,
                                                    move['MOVE_POINTS'])
          
    def _generalCardResult(self, **kw):
        man = kw['man'].getName()
        gcResult = kw['result']
        self._drama.dramaPause(.35)
        strResult = self._stringDict[gcResult] % (man)
        self._printText("%s\n" % strResult)

    # This method should be overridden if you want to change the behavior
    # EXTENDING THIS METHOD IS NOT RECOMMENDED!!!!!
    def _choiceList(self, **kw):
        prompt = kw['prompt']
        inputValue = False
        
        while (not inputValue):
            print prompt
            print "-" * len(prompt)
            print
            manCount = 1

            for choice in kw['choicelist']:
                print "%d) %s." % (manCount, choice)
                manCount += 1
                
            inputValue = raw_input("\n> ")
            if inputValue.isdigit() and string.atoi(inputValue) < manCount:
                inputValue = int(inputValue)
            else:
                print "Invalid entry.  Please re-enter a valid choice.\n"
                inputValue = 0
                
        self._resultQueue.put(inputValue - 1)
       
    def _newManIn(self, **kw):
        """Lets the interface know that there is a new man in for a team"""
        if kw.has_key('message'):
            self._printText(kw['message'])
        
    def _dtStart(self, **kw):
        dtList = kw["doubleTeamList"]
        dtRounds = kw["doubleTeamRounds"]

        self._drama.dramaPause(.5)
        men = string.join(map(lambda x: "%s, " % (x.getName()), dtList))[:-2]
        self._printText(self._stringDict["DT_MSG"] % (men, dtRounds))
        
    def _dtStatus(self, **kw):
        if kw['man']:
            man = kw['man'].getName()
        dtRound = kw['doubleTeamRound']
        dtStatus = kw['status']

        self._drama.dramaPause(.5)
        if dtRound > 0:
            if dtStatus in (OC, OCTT): strStatus = "offensive (OC)"
            else: strStatus = "defensive (DC)"
            self._printText(self._stringDict["DT_STATUS"] % (man, strStatus))
        else: self._printText(self._stringDict["DT_END"])

    # This method should be overridden if you want to change the behavior
    # EXTENDING THIS METHOD IS NOT RECOMMENDED!!!!!
    def _yesOrNo(self, **kw):
        prompt = kw['prompt']
        result = -999
        while (result == -999):
            result = raw_input(prompt)

            if string.upper(result) in ('Y', 'YES'):
                result = True
            elif string.upper(result) in ('N', 'NO'):
                result = False
            else:
               print "Invalid entry.  Please re-enter a vailid choice"
               result = -999
        
        self._resultQueue.put(result)

    def _printTime(self, **kw):
        self._printText("-" * 79)
        self._printText("\nAfter %s minutes." % (kw['minutes']))
        
    def _printScore(self, **kw):
        teams = kw['teams']
        scores = kw['scores']
        scoreType = kw['scoretype']
        skipFlag = True

        self._drama.dramaPause(.35)
        
        if scoreType == "ROUND":
            #skipFlag = False
            for t in (0,1):
                for man in teams[t]:
                    if not man.isCPU(): skipFlag=False
            
            if not skipFlag and not kw.has_key('noprompt'):
                self._printText("Hit any key to continue...")
                self._getInput(kw)
            
            
            self._printText("\nRound Scores:\n" + "-" * 13)
        else:
            self._printText("\nTotal Scores:\n" + "-" * 13)

        for t in (0,1):
            self._drama.dramaPause(.35)
            men = string.join(map(lambda x: "%s," % (x.getName()), \
                                                      teams[t]))[:-1]
            self._printText("%s: %d" % (men, scores[t]))
        self._printText()
        
    def _finish(self, **kw):
        finish = kw['finishlist']

        self._drama.dramaPause(1)
        self._printText()
        if len(finish) > 1:
            name1 = finish[0]["WINNER"].getName()
            name2 = finish[0]["LOSER"].getName()
            strFinish = "%s and %s were both counted out." % (name1, name2)
            self._printText(strFinish)
                
        elif len(finish) == 1:
            finish = finish[0]
            # Defensive player may have reversed a pin when using the
            # strategy pin chart
            if finish['MOVE']['MOVE_NAME'] in ['A', 'B', 'C', 'REVERSE']:
                finish['MOVE']['MOVE_NAME'] = "Pin Reversal"
                
            self._printText(self._stringDict["FINISH"]  %\
                  (finish['WINNER'].getName(), finish['MOVE']['MOVE_NAME'],\
                   finish['LOSER'].getName()))
        else:
            self._printText(self._stringDict["DRAW"] % \
                  (kw['time']))

        self._printText()
        if self._testing:
            self._resultQueue.put(0)
        
    def _injuryStatus(self, **kw):
        man = kw['man'].getName()
        rounds = kw['injuryRound']
        injuryStart = kw['start']

        self._drama.dramaPause(.5)
        self._printText()
        if injuryStart: self._printText(self._stringDict["INJURY_START"] % (man, \
                                                                            rounds))
        elif rounds > 0:
            self._printText(self._stringDict["INJURY_STATUS"] % (man, rounds))
        else:
            self._printText(self._stringDict["INJURY_END"] % man)

    def _pinAttempt(self, **kw):
        man = kw['man'].getName()
        self._printText("%s is attempting a pin!!!\n\n" % man)
        if kw['man'].isCPU(): self._drama.pinPause(1)

    def _pinResult(self, **kw):
        aggressor = kw['aggressor'].getName()
        victim = kw['victim'].getName()
        finished = kw['finished']
        saveMade = kw['save']
        pinRoll = kw['roll']
        pinGroup = kw['group']
        points = kw['points']
        stratChart = kw['strat_chart']
        pinIsReversed = kw['pin_reversal']

        if pinIsReversed:
            self._printText("%s Reverses the pin!!!" % victim)            
        else:
            if not finished:
                count = self._getPinCount(pinRoll, pinGroup, stratChart)
                self._doCount(count, "PIN_COUNT")

            if finished:
                self._doCount(3, "PIN_COUNT")
                self._printText(self._stringDict["PIN"] % (victim, aggressor))
            elif not finished and not saveMade:
                count = self._getPinCount(pinRoll, pinGroup, stratChart)
                self._printText("%s kicks out of the pin!" % victim)
                self._printText("%s gets %d points for the pin attempt."\
                      % (aggressor, points))
                if kw.has_key("scorecard"):
                    kw["scorecard"].updateScore(kw['aggressor'].getTeamNum(),
                                                points)
            else:
                self._printText("%s makes the save!!!!!" % kw['saveman'])
        self._printText()

    def _getPinCount(self, pinRoll, pinGroup, strategy_chart):
        count = 1
        if strategy_chart:
            if pinRoll > STRAT_PIN_GROUP_POINT_RANGES[pinGroup]: count = 2
        else:
            if pinRoll > PIN_GROUP_POINT_RANGES[pinGroup] / 2: count = 2
        return count
    
    def _submission(self, **kw):
        aggressor = kw['man'].getName()
        self._drama.submissionPause(1)
        self._printText("%s straps in the %s." % (aggressor,
                                                  kw['move']["MOVE_NAME"]))
        
    def _submissionResult(self, **kw):
        victim = kw['victim'].getName()
        finished = kw['finished']
        saveMade = kw['save']

        self._drama.submissionPause(2)
        if finished:
            self._printText(self._stringDict["SUBMISSION"] % (victim))
        elif not finished and not saveMade:
            self._printText("%s does not submit!" % victim)
        else:
            self._printText("%s makes the save!!!!!" % kw['saveman'])
        self._printText()
        
    def _printFinishEventMsg(self, **kw):
        self._printText(kw['message'])
        
    def _dq(self, **kw):
        victim = kw['victim'].getName()
        text = kw.get('text')
        if not text:
            text = "%s is on the outside.  The ref begins the count." % victim
                
        self._drama.countoutPause(1)        
        self._printText(text)

    def _dqResult(self, **kw):
        victim = kw['victim'].getName()
        finished = kw['finished']
        aggressor = kw['aggressor'].getName()
        dqEnabled = kw['dqEnabled']
        text = kw.get('text')
        
        if not text:
            text = "%s makes it back into the ring at the %d count."\
                      % (victim, kw['count'])

        if dqEnabled: self._doCount(kw['count'], "COUNTOUT")
        
        if finished:
            self._printText(self._stringDict["COUNTOUT"] % (victim))
        else:
            if dqEnabled:
                self._printText(text)

            points = 0
            if kw.get('print_score'):
                points = kw['count']
                self._printText("%s scores %d points.\n" % (aggressor,
                                                            points))
                
            if kw.has_key("scorecard"):
                kw["scorecard"].updateScore(kw['aggressor'].getTeamNum(),
                                            points)

        self._printText()
        
    def _flushEvents(self): pass
    
    def _doCount(self, count, counttype=None, soundfunc=None, sndargs=None):
        max = 3
        pauseFunc = self._drama.pinPause
        if counttype == "COUNTOUT":
            max = 10
            pauseFunc = self._drama.countoutPause
            
        for c in range(1, count + 1):
            ellipsis = "..."
            if c == max:
                ellipsis = ""
                
            self._flushEvents()
            if soundfunc:
                if counttype == "COUNTOUT": sndargs = [c]
                soundfunc(*sndargs)
            self._printText(str(c) + ellipsis, 0)
            self._flushEvents()
            pauseFunc(1)
            self._flushEvents()

        self._printText()
        
    def _makeSave(self, **kw):
        saveMan = kw['saveman'].getName()

        self._drama.pinPause(1)
        self._printText("%s attempts to make a save." % saveMan)
        self._drama.pinPause(1)

    def _printText(self, msg='\n', appendNewLine=1):
        if msg[-1] != '\n' and appendNewLine:
            msg +='\n'
        sys.stdout.write(msg)

    def cleanupQueues(self):
        for q in (self._resultQueue, self._messageQueue, self._signalQueue):
            while not q.empty():
                q.get()
        # Re-init the result queue
        self._resultQueue = ResultQueue()
        
    def _getInput(self, kw):
        getKey()
        self._resultQueue.put(0)

    # These methods should be overridden by any sub classes
    def _takeTeams(self, **kw):
        raise NotImplementedError, "Interface._takeTeams()"
    
    def _roundStartPrompt(self, **kw):
        self._resultQueue.put(0)
    def _cleanupUI(self, **kw): pass
    def _cleanupScorecards(self, **kw): pass
    def _disconnectMsg(self, **kw): pass
    def _receiveChatMsg(self, **kw): pass
    def _tooManyConns(self, **kw): pass
    def _doEnableMenus(self, **kw): pass
    def _showPopupWin(self, **kw): pass
    def _closePopupWin(self, **kw): pass
    def _highlightCell(self, **kw): pass
    def _enableTextLabel(self, **kw): pass
    def _disableTextLabel(self, **kw): pass
    
from lib.dblib import getWrestlerData
class MatchSetup:
    def __init__(self, network=0):
        self.teams     = [[], []]
        self.matchType = "Regular"
        self.timeLimit = 30
        self.dqEnabled = True

        if network:
            from lib.Networking import CopyDramaQueen
            self.drama = CopyDramaQueen(1, 1, 1, 1)
        else:
            self.drama = DramaQueen(1, 1, 1, 1)
            
        self.stratChart = False
        self.pinOnlyOnPA = False
        self.cpus = [[],[]]
        self.network = network
        
        self._getWrestlerFiles()
        
    def _getWrestlerFiles(self):
        self.wrestlers = getWrestlerData()
        
    def _wrestlersOnTeam(self, team):
        wrestlerTeam = []
        for wrestler in self.teams[team]:
            wrestlerTeam.append(wrestler.name)
        return wrestlerTeam
    
    def getWrestlerObject(self, wrestler): return self.wrestlers[wrestler]
    def getWrestlerName(self, wrestlerFileName, cb=None):
        name = self.wrestlers[wrestlerFileName].name
        if cb: cb(name)
        else: return name
        
    def getWrestlerInstance(self, wfilename, getInstanceCB):
        wrestler = self.wrestlers[wfilename]
        if self.network:
            from lib.Networking import CopyWrestler
            wrestlerobj = CopyWrestler
        else:
            wrestlerobj = spw.Wrestler

        getInstanceCB(wrestlerobj(wrestler, self.network))
        
        
    def getMatchObject(self, getMatchObjectCB):
        t = 0
        wrestlers = [[], []]
        if self.network:
            from lib.Networking import CopyWrestler
            wrestlerobj = CopyWrestler
        else:
            wrestlerobj = spw.Wrestler

        for team in self.teams:
            for member in team:
                wrestler = wrestlerobj(member, self.network)
                wrestler.setTeamNum(t)
                wrestler.setCPU(wrestler.getName() in self.cpus[t])
                wrestlers[t].append(wrestler)
            t += 1

        if self.matchType == "Regular":
            matchObj = spw.Match
        else:
            matchMods = getModules("Matches")
            for mod in matchMods:
                if matchMods[mod].name == self.matchType:
                    matchObj = matchMods[mod].SpecialtyMatch

        matchInst = matchObj(wrestlers[0], wrestlers[1],
                             timeLimit=self.timeLimit,
                             network=self.network,
                             dqEnabled=self.dqEnabled)
        matchInst.useStrategyPinChart(self.stratChart)
        matchInst.pinOnlyOnPA(self.pinOnlyOnPA)
        getMatchObjectCB(matchInst)
        
    def setTimeLimit(self, timeLimit): self.timeLimit = timeLimit
    def setDQ(self, dqEnabled): self.dqEnabled = dqEnabled

    # Setting drama values
    def setDramaticPause(self, enable): self.drama.setDramaPause(enable)
    def setRealtimePins(self, enable): self.drama.setRealtimePins(enable)
    def setRealtimeCountouts(self, enable):
        self.drama.setRealtimeCountouts(enable)
    def setSubmissionDrama(self, enable):
        self.drama.setSubmissionDrama(enable)
    # No more drama
    
    def setStrategyChart(self, stratChart): self.stratChart = stratChart
    def setPinOnlyOnPA(self, pinonpa): self.pinOnlyOnPA = pinonpa
    def setMatchType(self, matchType): self.matchType = matchType

    def getWrestlers(self, getWrestlerCB):
        self._getWrestlerFiles()
        wrestlers = self.wrestlers.keys()

        choices = []
        for wrestler in wrestlers:
            wmod = self.wrestlers[wrestler]
            if not hasattr(wmod, "nameSet"):
                nameSet = ""
            else: nameSet = wmod.nameSet
            choices.append((wmod.name, nameSet, wrestler))

        getWrestlerCB(choices)

    def getCurrentSetupValues(self, getCurrSetupCB=None):
        teams = [[], []]
        t = 0
        for team in self.teams:
            for member in team:
                teams[t].append(member.name)
            t += 1
            
        setupValDict = {"MATCH_TYPE":self.matchType,
                        "TIME_LIMIT":self.timeLimit,
                        "DQ_ENABLED":self.dqEnabled,
                        "DRAMA":self.drama,
                        "TEAMS":teams,
                        "CPUS":self.cpus,
                        "STRATEGY_CHART":self.stratChart,
                        "PIN_ONLY_ON_PA":self.pinOnlyOnPA}
        if getCurrSetupCB: getCurrSetupCB(setupValDict)
        else: return setupValDict
        
    def getTeams(self, getTeamsCB, data): getTeamsCB(self.teams, data)
    def getCPUs(self, getCPUsCB): getCPUsCB(self.cpus)
    def getMatchType(self, getMatchTypeCB): getMatchTypeCB(self.matchType)
    def getTimeLimit(self, getTimeLimitCB): getTimeLimitCB(self.timeLimit)
    def getDQ(self, getDqCB): getDqCB(self.dqEnabled)
    def getDrama(self, getDramaCB): getDramaCB(self.drama)
    
    def addWrestler(self, teamNum, wrestler, addWrestlerCB):
        wrestlerName = self.wrestlers[wrestler].name
        if len(self.teams[teamNum]) > 2:
            wrestler = (TOO_MANY_WRESTLERS_ERROR, wrestlerName)
        elif wrestlerName in self._wrestlersOnTeam(teamNum):
            wrestler = (WRESTLER_ALREADY_ON_TEAM_ERROR, wrestlerName)
        else:
            self.teams[teamNum].append(self.wrestlers[wrestler])
            wrestler = wrestlerName
        addWrestlerCB(wrestler, teamNum)
        
    def removeWrestler(self, teamNum, wrestler, rmWrestlerCB):
        idx = -1
        teamList = self.teams[teamNum]
        for wrestlerObj in teamList:
            if wrestlerObj.name == wrestler:
                idx = teamList.index(wrestlerObj)
                wrestlerToDelete = wrestlerObj
                break
        if idx > -1: self.teams[teamNum].remove(wrestlerToDelete)
            
        rmWrestlerCB(idx, teamNum)
        
    def addCPU(self, wrestler, team): self.cpus[team].append(wrestler)
    def removeCPU(self, wrestler, team): self.cpus[team].remove(wrestler)
    
    def validateTeams(self, validationCB):
        team1Len = len(self.teams[0])
        team2Len = len(self.teams[1])
        players = team1Len + team2Len
        
        validationCB(not cmp(team1Len, team2Len) and players)
        

class HostMatchSetup:
    def __init__(self, netclientCB):
        self.netClientCB = netclientCB
        
    def setTimeLimit(self, val): self.netClientCB("setTimeLimit", val)
    def setDQ(self, val): self.netClientCB("setDQ", val)
    def setDramaticPause(self, val): self.netClientCB("setDramaticPause", val)
    def setRealtimePins(self, val): self.netClientCB("setRealtimePins", val)
    def setRealtimeCountouts(self, val):
        self.netClientCB("setRealtimeCountouts", val)
    def setSubmissionDrama(self, val):
        self.netClientCB("setSubmissionDrama", val)
    def setStrategyChart(self, val): self.netClientCB("setStrategyChart", val)
    def setPinOnlyOnPA(self, val): self.netClientCB("setPinOnlyOnPA", val)
    def setMatchType(self, val): self.netClientCB("setMatchType", val)

    def getWrestlerInstance(self, wfilename, getInstCB):
        self.netClientCB("getWrestlerInstance",
                         wfilename).addCallback(getInstCB)
        
    def getWrestlers(self, getWrestlerCB):
        self.netClientCB("getWrestlers").addCallback(getWrestlerCB)
        
    def getTeams(self, getTeamsCB, dlg):
        self.netClientCB("getTeams").addCallback(getTeamsCB, dlg)
        
    def getCPUs(self, getCPUsCB):
        self.netClientCB("getCPUs").addCallback(getCPUsCB)
        
    def getMatchType(self, getMatchTypeCB):
        self.netClientCB("getMatchTypeCB").addCallback(getMatchTypeCB)
        
    def getTimeLimit(self, getTimeLimitCB):
        self.netClientCB("getTimeLimitCB").addCallback(getTimeLimitCB)
        
    def getDQ(self, getDqCB): self.netClientCB("getDqCB").addCallback(getDqCB)

    def getDrama(self, getDramaCB):
        self.netClientCB("getDramaCB").addCallback(getDramaCB)
        
    def addWrestler(self, team, wrestler, addWrestlerCB):
        self.netClientCB("addWrestler", team,
                         wrestler).addCallback(addWrestlerCB, team)
        
    def removeWrestler(self, team, wrestler, rmWrestlerCB):
        self.netClientCB("removeWrestler", team,
                         wrestler).addCallback(rmWrestlerCB, team)
        
    def addCPU(self, wrestler, team):
        self.netClientCB("addCPU", wrestler, team)
        
    def removeCPU(self, wrestler, team):
        self.netClientCB("removeCPU", wrestler, team)

    def validateTeams(self, validationCB):
        self.netClientCB("validateTeams").addCallback(validationCB)
    
class ClientMatchSetup:
    def __init__(self, netclientCB):
        self.netClientCB = netclientCB
    # This will get fired if the timelimit changes on the client, but we don't need
    #  to do anything since the client should not be setting the timelimit.
    def setTimeLimit(self, *args): pass

    def getWrestlerInstance(self, wfilename, getInstCB):
        self.netClientCB("getWrestlerInstance",
                         wfilename).addCallback(getInstCB)

    def getWrestlers(self, getWrestlerCB):
        self.netClientCB("getWrestlers").addCallback(getWrestlerCB)
        
    def addWrestler(self, team, wrestler, addWrestlerCB):
        self.netClientCB("addWrestler", team,
                         wrestler).addCallback(addWrestlerCB, team)
        
    def removeWrestler(self, team, wrestler, rmWrestlerCB):
        self.netClientCB("removeWrestler", team,
                         wrestler).addCallback(rmWrestlerCB, team)

    def addCPU(self, wrestler, team):
        self.netClientCB("addCPU", wrestler, team)
    
    def removeCPU(self, wrestler, team):
        self.netClientCB("removeCPU", wrestler, team)
        
    # Client doesn't do any validation, that's all handled by the server
    def validateTeams(self, validationCB): validationCB(ok2go=1)
        
class DummyScorecard:
    def __init__(self):
        self.teams = [0,0]

    def updateScore(t, val):
        self.teams[t] += val

class ResultQueue(Queue.Queue):
    def __init__(self):
        Queue.Queue.__init__(self)
        self.cb = None
        
    def put(self, value):
        if self.cb: self.cb(value)
        else: Queue.Queue.put(self, value)
            
class MessageQueue(Queue.Queue):
    def __init__(self, wakeupIdleFunc):
        Queue.Queue.__init__(self)
        self.wakeupIdleFunc = wakeupIdleFunc

    def put(self, value):
        Queue.Queue.put(self, value)
        self.wakeupIdleFunc()

class DramaQueen:
    def __init__(self, dramapause, rtpins, rtcountout, subdrama):
        self._dramaticPause = dramapause
        self._realtimePins = rtpins
        self._realtimeCountout = rtcountout
        self._submissionDrama = subdrama

    def hasDrama(self):
        return 1 in (self._dramaticPause, self._realtimePins,
                     self._realtimeCountout, self._submissionDrama)
    
    def setDramaPause(self, dramapause):
        self._dramaticPause = dramapause
        
    def setRealtimePins(self, rtpins):
        self._realtimePins = rtpins

    def setRealtimeCountouts(self, rtcountout):
        self._realtimeCountout = rtcountout

    def setSubmissionDrama(self, subdrama):
        self._submissionDrama = subdrama
        
    def getDramaPause(self):
        return self._dramaticPause
        
    def getRealtimePins(self):
        return self._realtimePins

    def getRealtimeCountouts(self):
        return self._realtimeCountout

    def getSubmissionDrama(self):
        return self._submissionDrama

    def dramaPause(self, secs):
        if self._dramaticPause:
            self._sleeper(secs)

    def pinPause(self, secs):
        if self._realtimePins:
            self._sleeper(secs)

    def countoutPause(self, secs):
        if self._realtimeCountout:
            self._sleeper(secs)

    def submissionPause(self, secs):
        if self._submissionDrama:
            self._sleeper(secs)
        
    def _sleeper(self, secs):
        time.sleep(secs)
    
        
def getKey():
    import msvcrt
    if msvcrt.kbhit():
        msvcrt.getch()
    while (1):
        if msvcrt.kbhit():
            msvcrt.getch()
            break

def printout(msg):
    print msg

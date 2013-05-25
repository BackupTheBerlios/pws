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

import sys, string, re, threading, thread, time, copy, Queue

from lib.util import *
from lib import Interface, spw, soundManager, tournamentLib, dblib
from data.globalConstants import *
from gui import matchSetup, wrestlerCreator, tourngui, datagui 
from gui.dialogs import NetworkingStartDialog, SelectDialog, MessageDialog
from gui.dialogs import YesOrNoDialog, ScrolledDialog
from lib import Networking

from wxPython.wx import *
from wxPython.lib.intctrl import *
from wxPython.grid import *
from wxPython.gizmos import *

class MainJowstWindow(wxPanel, Interface.BaseInterface):
    def __init__(self, parent):
        self.parent = parent
        self.soundMngr = soundManager.SoundManager()
        wxPanel.__init__(self, parent, -1)
        Interface.BaseInterface.__init__(self, 0)
        self._stringDict = {OC: "%s rolled OC.\n",
                            OCTT: "%s rolled OC/TT\n",
                            DC: "%s rolled DC\n",
                            INJURED: "%s is injured.",
                            "DT_MSG": "%s double teaming for %d rounds.",
                            "DT_STATUS":"%s is a %s double teamer.",
                            "DT_END":"Double teaming ends.",
                            "FINISH":"%s wins with a %s over %s!!!",
                            "DRAW":"After %s minutes, the match is declared a draw.",
                            "INJURY_START":" %s injured for %s rounds!!!",
                            "INJURY_STATUS":"%s is injured for %s more rounds.",
                            "INJURY_END":"%s is no longer injured.",
                            "PIN":"%s was pinned by %s!!!",
                            "SUBMISSION":"%s submits!!!",
                            "COUNTOUT":"%s is counted out!!!"}

        self._matchStarted = 0
        self.defaultBG_Color = None
        self._allCPUs = 1
        self._doNextRoundPrompt = False
        self._tagOutOccurred = False
        self._testing = False
        self.currHighlight = [None, None]
        self.teamFrSizer = [None,None]
        self._chatPanel = None
        self.notebookPages = {}
        self.msgQueue = Queue.Queue()  # Used for internal class messages 
        self.state = 0
        self._tagChoiceListTeam = -1
        self.client = None
        self._tourney = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        # Status Window and sizer
        self.topFrameSizer = wxBoxSizer(wxHORIZONTAL)

        self.notebookWin = wxNotebook(self, -1, style=wxNB_TOP)
        
        self.msgWin = wxTextCtrl(self, -1,
                                 style=wxTE_READONLY|wxTE_MULTILINE|wxTE_RICH2)
        self.topFrameSizer.Add(self.msgWin, 2, wxEXPAND)
        self.topFrameSizer.Add(self.notebookWin, 1, wxEXPAND)

        EVT_UPDATE_HIGHLIGHTER(self, self._onUpdate)
        EVT_MSG_ARRIVED(self, self._processMessage)
        self.teamFrSizer[0] = JowstTeamFrame(self, 0)
        self.teamFrSizer[1] = JowstTeamFrame(self, 1)
        self.buttonCol = ButtonColumn(self)
        EVT_BUTTON(self, ROLL_DICE_BUTTON, self.rollDice)
        self._diceRollButton = self.buttonCol.rollDiceButt
        self._diceRollButton.Enable(False)

        self._dieOne = self.buttonCol.dieOne
        self._dieTwo = self.buttonCol.dieTwo
        
        # This sizer will contain both team frames and the
        # middle button column
        self.midFrameSizer = wxBoxSizer(wxHORIZONTAL)
        self.midFrameSizer.Add(self.teamFrSizer[0], 2,
                               wxEXPAND|wxLEFT,border=5)
        self.midFrameSizer.Add((20,0))
        self.midFrameSizer.Add(self.buttonCol, 0, wxALIGN_CENTER|wxEXPAND)
        self.midFrameSizer.Add((20,0))
        self.midFrameSizer.Add(self.teamFrSizer[1], 2,
                               wxEXPAND|wxRIGHT,border=5)
        
        self.mainWinSizer = wxBoxSizer(wxVERTICAL)
        self.mainWinSizer.Add(self.topFrameSizer, 1, wxEXPAND|wxALL, border=5)
        self.mainWinSizer.Add(self.midFrameSizer, 2, wxEXPAND)

        self.SetAutoLayout(1)
        self.SetSizer(self.mainWinSizer)
        self.mainWinSizer.Fit(self)

        self.Show(1)

    def setMatchSounds(self, evt):
        id = evt.GetId()
        item = evt.GetEventObject().SoundMenu
        self.soundMngr.enableMatchSounds(item.IsChecked(id))

    def setDiceRollSounds(self, evt):
        id = evt.GetId()
        item = evt.GetEventObject().SoundMenu
        self.soundMngr.enableDiceSound(item.IsChecked(id))
        
    def rollDice(self, event):
        if self._matchStarted:
            self._diceRollButton.Enable(False)
            self.handlePromptResult(0)

    def _drawDice(self, pips):
        currDie = self._dieOne
        if len(pips) == 1: self._dieTwo.disable()
        elif self._dieTwo.isDisabled(): self._dieTwo.enable()
        for pip in pips:
            currDie.drawPips(pip + 1)
            currDie = self._dieTwo
            
    def handlePromptResult(self, result, data=None):
        if self.state in (AWAITING_DICE_ROLL_CLICK, ROUND_START, CHOICE_LIST):
            self._resultQueue.put(result)
            # Turn on round start prompt flag
            self._doNextRoundPrompt = True
            if self.state == ROUND_START:
                wxBeginBusyCursor()
        elif self.state == TAG_OUT_CHOICELIST:
            self._doNextRoundPrompt = False
            self._resultQueue.put(result)              
            self.teamFrSizer[self._tagChoiceListTeam].tagOutEligible = False
            self.teamFrSizer[self._tagChoiceListTeam].tagButton.Enable(False)

            # data is the message that states that a tag
            #  out has ocurred
            if data and data == TAG_OUT_OCCURRED:
                self._tagOutOccurred = True
            self._tagChoiceListTeam = -1 # Make invalid
            self.msgQueue.get()  # Remove the args from the queue
            
    def _onUpdate(self, evt):
        gridWin = self.teamFrSizer[evt.team].acWin
        renderer = gridWin.GetCellRenderer(evt.row, evt.col)
        renderer.setHighlightFlag(evt.isHighlighted)
        gridWin.SetCellValue(evt.row, evt.col, evt.text)
        

    def _scrollTo(self, r):
        sppuX, sppuY = r.grid.GetScrollPixelsPerUnit()
        vsX, vsY = r.grid.GetViewStart()
        vsW, vsH = r.grid.GetClientSizeTuple()
        
        if r.x/sppuX < vsX or \
           r.x + r.width > vsX + vsW or \
           r.y/sppuY < vsY or \
           r.y + r.height > vsY + vsH:
            r.grid.Scroll(r.x / sppuX, r.y / sppuY)
            r.grid.Refresh()
        #wxYieldIfNeeded()
        
    def _flushEvents(self):
        self.parent.app.makeReactorCurrent()
        while self.parent.app.Pending():
            self.parent.app.Dispatch()

    def sendMessage(self, msg, **kw):
        func, putInQueue = self._messageDict[msg]
        if kw.has_key("callback"):
            self._resultQueue.cb = kw["callback"]
        apply(func, [], kw)
        wxYieldIfNeeded()
        if putInQueue: self._resultQueue.put(0)
        
    def _msgQueueChecker(self):
        while not self._stopMatch:
            msg, kw = self._messageQueue.get()
            if msg:
                evt = MsgArrivedEvent(self.GetId(), msg, **kw)
                wxPostEvent( self, evt )
                
    def _processMessage(self, evt):
        self.sendMessage(evt.msg, **evt.kw)
        
    def _doCount(self, count, counttype=None, soundfunc=None, sndargs=None):
        timer = self.parent.app.timer
        soundfunc = None
        soundfunc = self.soundMngr.playSound
        soundargs = [counttype]
        if not timer.IsRunning():
            Interface.BaseInterface._doCount(self, count, counttype, soundfunc,
                                             soundargs)
        else:
            timer.Stop()
            Interface.BaseInterface._doCount(self, count, counttype,
                                             soundfunc, soundargs)
            timer.Start(NETWORK_LATENCY, False)
                
    def _printMessage(self, **kw):
        self._setText()
        apply(Interface.BaseInterface._printMessage, [self], kw)
        
    def _genericPrompt(self, **kw):
        man = kw['man']
        self._setText(wxBOLD)

        soundEffect = kw.get("sound")
        if soundEffect:
            if kw['man'].isCPU():
                d = .5
            else:
                d = 0
            self.soundMngr.playSound(soundEffect, delay=d)
        
        if not kw['man'].isCPU():
            self._printText("%s " % kw['prompt'])
            self._getInput(kw)
        else:
            self._resultQueue.put(self._getInput(kw))

    def _getInput(self, kw):
        if self._stopMatch: return
        t = kw['man'].getTeamNum()
        #manIn = self.teamFrSizer[t].getManIn()
        currWrestler = self.teamFrSizer[t].acWin.currWrestler
        manDiff = False
        
        #if manIn:
        
        # During double teaming, we may need to switch ActionCards so we
        #  make the check to see if we need to switch
        if kw['man'].getName() != currWrestler:
            manDiff = True
        if kw['type'] == GC:
            #self.teamFrSizer[t].setManIn(kw['man'])
            if self.currHighlight[t]:
                self.currHighlight[t].stopHighlightMode()
            if manDiff:
                self.teamFrSizer[t].acWin.populateActionCard(kw['man'])
            self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(GC_START_ROW, 0)
        elif kw['type'] == DC:
            self.currHighlight[t].stopHighlightMode()
        elif kw['type'] == OC:
            self.currHighlight[t].stopHighlightMode()
            if manDiff:
                self.teamFrSizer[t].acWin.populateActionCard(kw['man'])
            row, col = (self.currHighlight[t].row, self.currHighlight[t].col)
            self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(row, col)
        elif kw['type'] == ROPES:
            self.currHighlight[t].stopHighlightMode()
            self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(ROPES_START_ROW, 2)
        elif kw['type'] == SPECIALTY:
            self.currHighlight[t].stopHighlightMode()
            self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(SPECIALTY_START_ROW, 0)
        elif kw['type'] == XX:
            if self.currHighlight[t]:
                self.currHighlight[t].stopHighlightMode()
           
        if not kw['man'].isCPU():
            #wxYieldIfNeeded()
            self.currHighlight[t].startHighlightMode(1)
            
        self._scrollTo(self.currHighlight[t])

        if not kw['man'].isCPU():
            self.state = AWAITING_DICE_ROLL_CLICK       
            self._diceRollButton.Enable(True)
        
    def _printRoundBorder(self, **kw):
        if self._startEvent.isSet():
            self.soundMngr.playSound("BELL", delay=1)
            self._startEvent.clear()
            
        if self._tagOutOccurred:
            self._printText()
            self._tagOutOccurred = False
            
        if wxIsBusy(): wxEndBusyCursor()
        # Only print a round border at the start of a round
        if kw['start']:
            self._setText(wxBOLD, fontColor=wxNamedColour(ROUND_COLOR))
            self._printText()
            self._printText("===== In the %s minute of the match: ====="
                            % minuteString(kw['time']))
            self._printText()

    def _moveAttempt(self, **kw):
        t = kw['team']
        move = kw['move']
        kw['scorecard'] = self.scoreCardWin
        if move.has_key('INDEX'):
            moveIdx = move["INDEX"]
            if move["CARD"] == OC:
                row, col = (OFFENSIVE_CARD_START_ROW + 1 + moveIdx, 2)
            elif move["CARD"] == DC:
                row, col = self.teamFrSizer[t].acWin.dcList[moveIdx]
            elif move["CARD"] == ROPES:
                row, col = (ROPES_START_ROW + 1 + moveIdx, 2)
            elif move["CARD"] == SPECIALTY:
                row, col = (SPECIALTY_START_ROW + 2 + moveIdx, 0)
        else:
            row, col = (DC_START_ROW, 0)

        self.currHighlight[t].stopHighlightMode()
        self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(row, col)
        self.currHighlight[t].startHighlightMode(None)

        self.soundMngr.playSound("ROLL_DICE", delay=.1)
        self._drawDice(move["PIPS"])
        self._scrollTo(self.currHighlight[t])

        self._setText(fontColor=wxNamedColour(MOVE_COLOR))
        apply(Interface.BaseInterface._moveAttempt, (self,), kw)
        
    def _generalCardResult(self, **kw):
        t = kw['man'].getTeamNum()
        self._setText()

        if self.currHighlight[t]:
            self.currHighlight[t].stopHighlightMode()
        if not kw['index'] in (INJURED, OC):
            row, col = self.teamFrSizer[t].acWin.gcList[kw['index']]
            self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(row, col)
            self.currHighlight[t].startHighlightMode(None)

        self.soundMngr.playSound("ROLL_DICE", delay=.1)
        self._drawDice(kw['die_pips'])
        self._scrollTo(self.currHighlight[t])

        apply(Interface.BaseInterface._generalCardResult, (self,), kw)

    def _choiceList(self, **kw):
        t = kw['man'].getTeamNum()

        # Put these args in the queue so they are available to the
        #  _doChoiceListPrompt()
        self.msgQueue.put(kw)

        # Tagging out is a special case of the choice list.  Handling here.
        if kw.has_key('tagout'):
            self.teamFrSizer[t].tagOutEligible = True
            self.teamFrSizer[t].tagButton.Enable(True)
            self._setText(wxBOLD)
            self._printText("< %s can tag out or " %(kw['man'].getName())+ \
                            "click 'Roll Dice' button to start next round. >")
            
            self.teamFrSizer[t].updateChoices(kw['choicelist'], kw['prompt'],
                                              kw['caption'])

            self.state = TAG_OUT_CHOICELIST
            self._tagChoiceListTeam = t
            if not kw['man'].isCPU(): self._diceRollButton.Enable(True)
        else:
            self.state = CHOICE_LIST
            self._doChoiceListPrompt()
            
    def _doChoiceListPrompt(self):
        kw = self.msgQueue.get()
        prompt = kw['prompt']
        prompt += " " * 50
        dlg = wxSingleChoiceDialog(self, prompt, kw['caption'],
                                   kw['choicelist'], wxOK)
        if dlg.ShowModal() == wxID_OK:
            retVal = dlg.GetSelection()
        dlg.Destroy()
        
        self.handlePromptResult(retVal)

    def _newManIn(self, **kw):
        if kw.has_key("message"):
            self._setText()
            Interface.BaseInterface._newManIn(self, **kw)
        man = kw['new_man_in']
        team = man.getTeamNum()
        self.teamFrSizer[team].setManIn(man)
        self.teamFrSizer[team].acWin.populateActionCard(man)
        
    def _dtStart(self, **kw):
        self._setText()
        dtList = kw['doubleTeamList']
        dtRounds = kw["doubleTeamRounds"]
        t = dtList[0].getTeamNum()
        self.teamFrSizer[t].dtRoundCounter.SetValue(str(dtRounds))
        apply(Interface.BaseInterface._dtStart, (self,), kw)

    def _dtStatus(self, **kw):
        if kw['man']:
            t = kw['man'].getTeamNum()
        dtRound = kw['doubleTeamRound']
        
        self._setText()
        if dtRound < 1:
            for t in (0,1):
                acWin = self.teamFrSizer[t].acWin
                acWin.populateActionCard(self.teamFrSizer[t].getManIn())
                self.teamFrSizer[t].dtRoundCounter.SetValue(str(dtRound))
                wxYieldIfNeeded()
        else:
            acWin = self.teamFrSizer[t].acWin
            acWin.populateActionCard(kw['man'])
            self.teamFrSizer[t].dtRoundCounter.SetValue(str(dtRound))
            wxYieldIfNeeded()

        # The lastman key only exists when everyone is in the ring for one round.
        #  "lastman" refers to the last man on the team who will execute a move
        # When the lastman is true we need to set the double team round counter
        #  to 0
        if kw.has_key("lastman") and kw['lastman']:
            self.teamFrSizer[t].dtRoundCounter.SetValue("0")
            
        apply(Interface.BaseInterface._dtStatus, (self,), kw)

    def _yesOrNo(self, **kw):
        prompt = kw.get('prompt', kw['caption'])
        layout = kw['layout']
        caption = kw.get('caption', "Pro Wrestling Superstar")
        
        if not layout:
            dlg = wxMessageDialog(self, prompt, caption,
                                  wxYES_NO)
        else:
            dlg = YesOrNoDialog(self, caption)
            for item in layout:
                if type(item) in [type([]), type(())]:
                    itemStr, itemType, param = item
                    if itemType == HEADING:
                        dlg.addHeading(itemStr, param)
                    elif itemType == LINE:
                        dlg.addLine(itemStr)
                elif type(item) == type({}):
                    dlg.setTableHeaders(item["COLUMNS"])
                    for row in item["ROWS"]:
                        dlg.addTableRow(row)
                    dlg.insertTable()

        if dlg.ShowModal() == wxID_YES:
            result = 1
        else:
            result = None
        dlg.Destroy()

        self._resultQueue.put(result)
        
    def _printTime(self, **kw):
        self.buttonCol.matchTime.SetValue("%s-00" % kw['minutes'])

    def _printScore(self, **kw):
        self._setText(fontColor=wxNamedColour(ROUND_COLOR))
        kw['noprompt'] = 1
        if kw['scoretype'] == "TOTAL":
            self.scoreCardWin.nextRound()

    def _finish(self, **kw):
        self.soundMngr.playSound("FINISH_BELL")
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._finish, (self,), kw)

        # Result Queue pump
        # Tell engine/server we received the "FINISH" msg
        self._resultQueue.put(0)  
        # Tell engine/server we received the "ROUND_BORDER" msg
        self._resultQueue.put(0)

        finish = kw['finishlist']
        if (self._matchIsLocal() or kw.has_key('resultdata')) and \
            not self._testing:
            self._showResultsDialog(kw)
                
        if self._tourney:
            if len(finish) == 1:
                self._tourney.setWinner(finish[0]['WINNER'].getTeamNum())
            else:
                self._tourney.setWinner(-1)

            filename = None
            if hasattr(self._tourney, "filename"):
                filename = self._tourney.filename

            tourngui.showTournamentControlPanel(self._tourney,
                                                self._doMatchStartup,
                                                self._stopTourney,
                                                filename)

        endMatchID = self.parent.RunMenu.FindItem("End Match")

        # If we're running the match locally then call endMatch()
        if self.parent.RunMenu.FindItemById(endMatchID).IsEnabled():
            EVT_FINISHED(self, self.endMatch)
            event = FinishedEvent( self.GetId() ) 
            self.GetEventHandler().AddPendingEvent( event )

    def _injuryStatus(self, **kw):
        self._setText(fontColor=wxNamedColour(INJURY_COLOR))
        t = kw['man'].getTeamNum()
        name = kw['man'].getName()
        if kw['start']:
            self.teamFrSizer[t].lblDict[kw['man'].getName()].SetBackgroundColour(wxRED)
            wxYieldIfNeeded()
            self.teamFrSizer[t].lblDict[kw['man'].getName()].SetLabel(name + " INJ = %sR" % kw['injuryRound'])
            wxYieldIfNeeded()
        elif kw['injuryRound'] > 0 and not kw['start']:
            self.teamFrSizer[t].lblDict[kw['man'].getName()].SetLabel(name + " INJ = %sR" % kw['injuryRound'])
            wxYieldIfNeeded()
        else:
            self.teamFrSizer[t].lblDict[kw['man'].getName()].SetLabel(name)
            wxYieldIfNeeded()
            self.teamFrSizer[t].lblDict[kw['man'].getName()].SetBackgroundColour(self.defaultBG_Color)
            wxYieldIfNeeded()
        self.teamFrSizer[t].lblDict[kw['man'].getName()].Layout()
        wxYieldIfNeeded()
        apply(Interface.BaseInterface._injuryStatus, (self,), kw)
        wxYieldIfNeeded()
        
    def _pinAttempt(self, **kw):
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._pinAttempt, (self,), kw)

    def _pinResult(self, **kw):
        kw['scorecard'] = self.scoreCardWin
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._pinResult, (self,), kw)

    def _submission(self, **kw):
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._submission, (self,), kw)
        self.soundMngr.playSound("ARGH")

    def _submissionResult(self, **kw):
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._submissionResult, (self,), kw)

    def _printFinishEventMsg(self, **kw):
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._printFinishEventMsg, (self,), kw)
        self._drama.dramaPause(2)
        
    def _dq(self, **kw):
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._dq, (self,), kw)
        
    def _dqResult(self, **kw):
        kw['scorecard'] = self.scoreCardWin
        self._setText(wxBOLD, fontColor=wxNamedColour(FINISH_COLOR))
        apply(Interface.BaseInterface._dqResult, (self,), kw)

    def _makeSave(self, **kw):
        # We don't want to display any save attempts
        pass

    def _roundStartPrompt(self, **kw):
        self.state = ROUND_START
        # If there is a non-cpu wrestler, prompt to start next round
        if not self._allCPUs and self._doNextRoundPrompt:
            self._setText(wxBOLD)
            self._printText("< Click 'Roll Dice' button to start next round. >")
            self._diceRollButton.Enable(True)
        else:  # Tell the match engine we're ready to start the round
            self.handlePromptResult(0)
            
    def _tooManyConns(self, **kw):
        dlg = wxMessageDialog(self, "Too many connections",
                              "Uanble to Connect to server", wxOK)
        dlg.ShowModal()
        dlg.Destroy()
        
    def _setText(self, fontOptions=0, fontColor=wxBLACK):      
        f = self.msgWin.GetFont()

        if wxBOLD&fontOptions:
            f.SetWeight(wxBOLD)

        self.msgWinFont = f
        self.msgWinFG_Colour = fontColor
        wxYieldIfNeeded()

    def _printText(self, strText='\n', appendNewLine=1):
        if self._stopMatch: return
        self.msgWin.SetDefaultStyle(wxTextAttr(self.msgWinFG_Colour,
                                               font=self.msgWinFont))
        if strText[-1] != '\n' and appendNewLine:
            strText += '\n'
        self.msgWin.SetInsertionPointEnd()
        self.msgWin.WriteText(strText)
        self.msgWin.ScrollPages(1)
        wxYieldIfNeeded()

    def _matchIsLocal(self):
        return hasattr(self, "_matchObj") and self._matchObj
    
    def _showResultsDialog(self, kw):
        promptStr = "Select the database to add the match results to.\n" \
                    "Clicking Cancel will not add the results to a" \
                    " database."
        resultData = kw.get('resultdata')
        if not resultData:
            resultData = self._matchObj.getMatchResultData()
        hdr = resultData["RESULT_STRING"]
        dlg = datagui.ResultDBSelector(self, "Update Results")
        dlg.addLabel(hdr, bold=1)
        dlg.addSpacer(5)
        dlg.addDateEntry("Match Date", "matchDate")
        evt = "House Show"
        if self._tourney:
            evt = self._tourney.getTourneyName()
        dlg.addTextEntry("Event", "event", default=evt,
                         entrysize=200)
        dlg.addTextEntry("Location", "location", entrysize=250)
        dlg.addSpacer(5)
        dlg.addLine()
        dlg.addSpacer(2)
        dlg.addLabel(promptStr, center=1)
        dlg.addDbSelector()
        time.sleep(2)

        if dlg.ShowModal() == wxID_OK:
            if kw.has_key('resultdata'):
                matchType = resultData['MATCH_TYPE']
                noWinner = resultData['NO_WINNER']
            else:
                matchType = self._matchObj.getMatchType()
                noWinner = self._matchObj.isDraw() or \
                           self._matchObj.isDoubleCountout()

            db = dlg.getResultDb()
            matchData = {"MATCH_TIME": "%d:00" % kw['time'],
                         "DATE": dlg.matchDate.GetValue(),
                         "EVENT": dlg.event.GetValue(),
                         "LOCATION": dlg.location.GetValue(),
                         "MATCH_TYPE": matchType}

            if db:
                db.updateResults(resultData["WINNER_KEY"],
                                 resultData["WINNER_NAME"],
                                 resultData["LOSER_KEY"],
                                 resultData["LOSER_NAME"],
                                 data=matchData,
                                 isdraw=noWinner)               
                dlg.Destroy()
                d = wxMessageDialog(self, "%s database" % db.name +\
                                    " has been updated.",
                                    "Database Updated", style=wxOK)
                d.ShowModal()
                d.Destroy()
            else:
                dlg.Destroy()
        else:
            dlg.Destroy()
        
    def setupMatch(self, evt):
        setupObj = Interface.MatchSetup()
        setupGUI = matchSetup.MatchSetupDialog(setupObj)
        setupGUI.buildMatchControlGUI()
        setupGUI.enableWidgetEvents()
        setupGUI.enableWidgets()
        setupGUI.addButtons()

        if setupGUI.ShowModal() == wxID_OK:
            self._doMatchStartup(setupGUI)
        else:
            setupGUI.Destroy()
            
    def _doMatchStartup(self, setupGUI, falseItems=("Run Match", ),
                        trueItems=("End Match", )):
        self._stopMatch = False
        self._cleanupScorecards()
        self.msgWin.Clear()
        setupGUI.getMatchObject(self._setMatchObject)
        setupGUI.getDrama(self._setDrama)
        timeLimit = self._matchObj.getTimeLimit()
        teams = self._matchObj.getTeams()
        matchType = self._matchObj.getMatchType()
        imageFile = self._matchObj.getImageFile()
        labelData = self._matchObj.getLabelData()
        self._setupUI(teams, timeLimit, matchtype=matchType,
                      imagefile=imageFile, labeldata=labelData)

        self.enableMenus(self.parent.RunMenu, trueItems, falseItems)
        setupGUI.Destroy()

        if hasattr(self, "_matchObj") and self._matchObj:
            timer = self.parent.app.timer
            if timer.IsRunning(): timer.Stop()

            self._matchObj.setInterfaces(self._resultQueue,
                                         self._messageQueue, self._signalQueue)
            self._matchStarted = 1
            self._checkMessageQueue()
            matchRun = threading.Thread(target=self._matchObj.runMatch)
            matchRun.start()

    def _setMatchObject(self, matchObj): self._matchObj = matchObj
    def _setDrama(self, drama): self._drama = drama
    
    def _takeTeams(self, **kw):
        self._stopMatch = False # Unset the stop match flag
        self._cleanupScorecards()
        self.msgWin.Clear()
        self._drama = kw['drama']
        self._setupUI(kw['teams'], kw['timelimit'], kw['network'],
                      kw['player_wrestlers'], matchtype=kw['matchtype'],
                      imagefile=kw['matchimage'], labeldata=kw['labeldata'])

    def _cleanupScorecards(self, **kw):
        # Blow away any existing scorecard windows
        for page in self.notebookPages.keys():
            if page != "Chat":
                self.notebookWin.DeletePage(self.notebookPages[page])


    def _cleanupUI(self, **kw):
        self.cleanup(doshutdown=kw.get("shutdown"))

    def _disconnectMsg(self, **kw):
        # Re-enable the Network menu
        self._networkCleanup()
        # Re-enable the Run Menu
        trueItems = ("Run Match",)
        falseItems = []
        self.enableMenus(self.parent.RunMenu, trueItems, falseItems)
        imgpath = os.path.join(JOWST_PATH, "resources", "rj45.jpg")
        dlg = MessageDialog(self, kw['message'], kw['caption'],
                            image=os.path.normpath(imgpath))
        dlg.Show(1)
        
    def _showMsgBox(self, evt):
        dlg = evt.data
        dlg.ShowModal()
        dlg.Destroy()
        
    def _receiveChatMsg(self, **kw):
        msg = kw["message"]
        player = kw["playername"]
        try:
            self._chatPanel.receiveMsg(player, msg)
        except:
            pass
        
    def _setupUI(self, teams, timelimit, network=0, player_wrestlers=[],
                 matchtype="Regular", imagefile=None, labeldata=[]):
        t = 0
        totalWidgets = []
        teamStrs = []
        for team in teams:
            teamStr = ""
            self.teamFrSizer[t].cleanup()
            for member in team:
                if len(player_wrestlers):
                    if member.getName() in player_wrestlers:
                        if not member.isCPU(): self._allCPUs = 0
                elif not member.isCPU(): self._allCPUs = 0
                self.teamFrSizer[t].addWrestler(member)
                teamStr += member.getName() + ", "
            self.teamFrSizer[t].acWin.populateActionCard(teams[t][0])
            self.teamFrSizer[t].setManIn(teams[t][0])

            for label in labeldata:
                name, text, fgcolor, bgcolor, size = label
                self.teamFrSizer[t].addTextLabel(name, text, fgcolor, bgcolor,
                                                 size)
                                             
            totalWidgets.append(self.teamFrSizer[t].totalScore)
            teamStrs.append(teamStr[:-2])
            t += 1
        if not self.defaultBG_Color:
            self.defaultBG_Color = self.teamFrSizer[0].lblDict[teams[0][0].getName()].GetBackgroundColour()
        self.scoreCardWin = ScoreCard(self.notebookWin, timelimit, teamStrs, totalWidgets)
        self.notebookWin.InsertPage(0, self.scoreCardWin, "Scorecard",
                                    select=True)
        
        self.notebookPages["Scorecard"] = 0
        if network and not self._chatPanel:
            self._chatPanel = ChatPanel(self.notebookWin,
                                        self.client.sendChatMsg)
            
            self.notebookWin.AddPage(self._chatPanel, "Chat")
            self.notebookPages["Chat"] = 1
        elif network and self._chatPanel:
            self._chatPanel.setChatCB(self.client.sendChatMsg)

        self._matchStarted = 1
        try:
            self.buttonCol.setMatchImage(matchtype, imagefile=imagefile)
        except:
            pass
        # Disable sound if all cpus and no dramatic pause
        if self._allCPUs and not self._drama.hasDrama():
            self.soundMngr.enableSound(0)
            self.enableMenus(self.parent.SoundMenu, (), ("Match Sounds",
                                                         "Dice Roll Sounds"))
        self._startEvent = threading.Event()
        self._startEvent.set()
        wxYieldIfNeeded()


    def setupNetworkMatch(self, evt):        
        timer = self.parent.app.timer
        #self._checkMessageQueue()
        if not timer.IsRunning(): timer.Start(NETWORK_LATENCY, False)
        os.environ["JOWST_CLIENT_TOKEN"] = generateRandomPassword()
        serverPath = os.path.normpath(os.path.join(JOWST_PATH, "server"))
        # Start Server
        os.spawnle(os.P_NOWAIT, serverPath, "server", os.environ)
        self.client = Networking.JowstClient("host", self.sendMessage,
                                             "no_name_required", host=1,
                                             clientToken=os.environ["JOWST_CLIENT_TOKEN"])
        self.setResultCB(self.client.sendResult)
        self.client.startClient()

    def stopNetworkGame(self, evt):
        self.client.stopNetGame()
                
    def connectToNetworkMatch(self, evt):
        startclient = None
        timer = self.parent.app.timer
        #self._checkMessageQueue()
        if not timer.IsRunning(): timer.Start(NETWORK_LATENCY, False)
        dlg = NetworkingStartDialog("Connect to Server", "Connect to Server")
        dlg.addConnectToServerField()
        dlg.addPortField()
        dlg.addServerPasswordField()
        dlg.addPlayerNameField()
        dlg.addButtons()
        if dlg.ShowModal() == wxID_OK:
            trueItems = ("Disconnect From Server", )
            falseItems = ("Start Network Game", "Connect To Server")
            self.enableMenus(self.parent.NetworkMenu, trueItems, falseItems)
            trueItems = []
            falseItems = ("Run Match",)
            self.enableMenus(self.parent.RunMenu, trueItems, falseItems)
            server = dlg.getServerName()
            port = dlg.getPort()
            passwd = dlg.getServerPassword()
            playername = dlg.getPlayerName()
            startclient = 1
        else:
            self._networkCleanup()
            
        dlg.Destroy()
        if startclient:
            self.client = Networking.JowstClient("player", self.sendMessage,
                                                 playername,
                                                 passwd=passwd, port=port,
                                                 hostname=server)
            self.setResultCB(self.client.sendResult)
            self.client.startClient()

    def disconnFromServer(self, evt):
        self.client.disconnectFromServer()
        self._networkCleanup()
        
    def stopServer(self, evt):
        self.client.stopServer()
        self._networkCleanup()
        
    def _networkCleanup(self):
        falseItems = ("Stop Network Game", "Stop Server")
        trueItems = ("Start Network Game", "Connect To Server")
        self.enableMenus(self.parent.NetworkMenu, trueItems, falseItems)
        self.cleanup()

    def reenableSound(self):
        # Turn sound back on
        msID = self.parent.SoundMenu.FindItem("Match Sounds")
        dsID = self.parent.SoundMenu.FindItem("Dice Roll Sounds")
        msItem = self.parent.SoundMenu.FindItemById(msID)
        dsItem = self.parent.SoundMenu.FindItemById(dsID)

        for menuItem, func, name in ((msItem, self.soundMngr.enableMatchSounds,
                                      "Match Sounds"),
                                     (dsItem, self.soundMngr.enableDiceSound,
                                      "Dice Roll Sounds")):
            if not menuItem.IsEnabled():
                if menuItem.IsChecked(): func(1)
                self.enableMenus(self.parent.SoundMenu, (name, ), ())

        
    def endMatch(self, evt):
        # Match finished 
        if evt and hasattr(evt, "eventType") and evt.eventType == FINISHED:
            self._signalQueue.get()

        # Match interrupted
        if self._matchIsLocal():
            if self._matchObj.isRunning():
                self._matchObj.stopMatch()
                self._signalQueue.get()
                time.sleep(1)
                if self._tourney:
                    filename = None
                    if hasattr(self._tourney, "filename"):
                        filename = self._tourney.filename
                    tourngui.showTournamentControlPanel(self._tourney,
                                                        self._doMatchStartup,
                                                        self._stopTourney,
                                                        filename)

            self._matchObj = None
        self.cleanup()
        if self._testing: return
        
        trueItems = ("Run Match", )
        falseItems = ("End Match", )
        
        self.enableMenus(self.parent.RunMenu, trueItems, falseItems)

    def cleanup(self, doshutdown=1):
        self._matchStarted = 0
        self.state = 0
        self._doNextRoundPrompt = False
        self._tagOutOccurred = False
        if doshutdown: self._stopMatch = True
        self._allCPUs = True

        self._messageQueue.put((None, None))
        self._diceRollButton.Enable(False)
        for t in (0, 1):            
            try:
                if self.currHighlight[t]:
                    self.currHighlight[t].stopHighlightMode()
                    time.sleep(.25)
                    self.currHighlight[t] = None
            except:
                pass

        self.buttonCol.matchTime.SetValue("0-00")          
        for t in (0,1): self.teamFrSizer[t].cleanup()
        self.cleanupQueues()
        if wxIsBusy(): wxEndBusyCursor()
        self.reenableSound()

        if self._testing:
            if self._testObj.hasMoreTests():
                self._testObj.next()
            else:
                self.enableMenus(self.parent.HelpMenu, ("Start Test", ),
                                 ("Stop Test", )) 
                self.enableMenus(self.parent.RunMenu, ("Run Match", ),
                                 ("End Match", ))
        

    def startTest(self, evt):
        from lib.testlib import GuiTester
        self.enableMenus(self.parent.HelpMenu, ("Stop Test", ),
                         ("Start Test", )) 
        self._testing = True
        self._testObj = GuiTester(self.run_test)
        self._testObj.run()

    def stopTest(self, evt):
        self._testing = False
        self.endMatch(None)
        self.enableMenus(self.parent.HelpMenu, ("Start Test", ),
                         ("Stop Test", )) 
        
        
    def run_test(self, matchObj, drama):
        self._stopMatch = False
        self._cleanupScorecards()
        self.msgWin.Clear()
        self._setMatchObject(matchObj)
        self._setDrama(drama)
        timeLimit = self._matchObj.getTimeLimit()
        teams = self._matchObj.getTeams()
        matchType = self._matchObj.getMatchType()
        imageFile = self._matchObj.getImageFile()
        labelData = self._matchObj.getLabelData()
        self._setupUI(teams, timeLimit, matchtype=matchType,
                      imagefile=imageFile, labeldata=labelData)

        falseItems = ("Run Match", )
        trueItems = ("End Match", )
        self.enableMenus(self.parent.RunMenu, trueItems, falseItems)

        timer = self.parent.app.timer
        if timer.IsRunning(): timer.Stop()

        self._matchObj.setInterfaces(self._resultQueue, self._messageQueue, self._signalQueue)
        self._matchStarted = 1
        self._checkMessageQueue()
        matchRun = threading.Thread(target=self._matchObj.runMatch)
        matchRun.start()
        
    def _doEnableMenus(self, **kw):
        menu = getattr(self.parent, kw['menuname'])
        self.enableMenus(menu, kw['trueitems'], kw['falseitems'])
        
    def enableMenus(self, menu, trueItems, falseItems):
        enable = 1
        for menuitems in (trueItems, falseItems):
            for item in menuitems:
                menu.Enable(menu.FindItem(item), enable)
            enable -= 1

    def _showPopupWin(self, **kw):
        setattr(self, kw['win_name']+"Win", PopupWin(self, kw['win_text']))
        getattr(self, kw['win_name']+"Win").Show(1)

    def _closePopupWin(self, **kw):
        if hasattr(self, kw['win_name']+"Win") and \
               getattr(self, kw['win_name']+"Win"):
            getattr(self, kw['win_name']+"Win").Destroy()
            setattr(self, kw['win_name']+"Win", None)

    def _highlightCell(self, **kw):
        row, col, t = kw['row'], kw['col'], kw['team']
        flash = kw.get("flash")
        if not flash:
            if kw['man'].isCPU(): flash = 0
            else: flash = 1
        if self.currHighlight[t]:
            self.currHighlight[t].stopHighlightMode()
        self.currHighlight[t] = self.teamFrSizer[t].acWin.GetCellRenderer(row,
                                                                          col)
        self.currHighlight[t].startHighlightMode(flash)
        
    def _enableTextLabel(self, **kw):
        man = kw['man']
        win = self.teamFrSizer[man.getTeamNum()]
        win.enableTextLabel(kw['label'], kw.get('tooltip'))

    def _disableTextLabel(self, **kw):
        man = kw['man']
        win = self.teamFrSizer[man.getTeamNum()]
        win.disableTextLabel(kw['label'])
        
    def viewWrestler(self, evt):
        wrestlerDict = dblib.getWrestlerData()
        dictvals = wrestlerDict.values()
        dictvals.sort(cmpNames)
        choices = []

        for wrestler in dictvals:
            choices.append(spw.Wrestler(wrestler))
            
        WrestlerViewer(self, choices, name_and_set=1)
    
    def showAboutWin(self, evt):
        dlg = AboutWin(self)
        dlg.ShowModal()
        dlg.Destroy()

    def startWrestlerBuilder(self, evt):
        wrestlerCreator.startBuilder(self)

    def startTourney(self, evt):
        tourngui.showTournamentGUI(self._runTourney)

    def _runTourney(self, teams, name):
        falses = ["Run New Tournament", "Run Match"]
        self.enableMenus(self.parent.RunMenu, (), falses)
        falses = ["Open Tournament"]
        self.enableMenus(self.parent.FileMenu, (), falses)
        wrestlerDict = dblib.getWrestlerData()
        tourneyTeams = []
        seed = 1
        for team in teams:
            teamMods = []
            for wrestlerName, setName in team:
                for wrestlerMod in wrestlerDict.values():                    
                    if wrestlerName == wrestlerMod.name and \
                       setName == getattr(wrestlerMod, "nameSet", ""):
                        teamMods.append(wrestlerMod)
                        break
            tourneyTeams.append(tournamentLib.Team(teamMods, seed))
            seed += 1
        self._tourney = tournamentLib.TournamentManager(tourneyTeams, name)
        tourngui.showTournamentControlPanel(self._tourney,
                                            self._doMatchStartup,
                                            self._stopTourney)

    def _tourneyMatchStart(self):
        setupObj = Interface.MatchSetup()
        setupGUI = matchSetup.MatchSetupDialog(setupObj)
        setupGUI.buildMatchControlGUI()
        setupGUI.setTeams(m[0][0].team.getData(), m[0][1].team.getData(), 0)
        setupGUI.enableWidgetEvents()
        setupGUI.enableWidgets()
        setupGUI.addButtons()
        
        self._stopMatch = False        
        if setupGUI.ShowModal() == wxID_OK:
            self._doMatchStartup(setupGUI)

    def _stopTourney(self):
        self._tourney = None
        trues = ["Run New Tournament", "Run Match"]
        self.enableMenus(self.parent.RunMenu, trues, ())
        trues = ["Open Tournament"]
        self.enableMenus(self.parent.FileMenu, trues, ())
        
        
    def openTournament(self, evt):
        dbDir = os.path.join(JOWST_PATH, "db")
        dlg = wxFileDialog(self, "Open Saved Tournament", dbDir, "",
                           "Tournament Files (*.trn)|*.trn", style=wxOPEN)

        if dlg.ShowModal() == wxID_OK:
            falses = ["Run New Tournament", "Run Match"]
            self.enableMenus(self.parent.RunMenu, (), falses)
            falses = ["Open Tournament"]
            self.enableMenus(self.parent.FileMenu, (), falses)
            try:
                db = dblib.BaseDB(dlg.GetPath())
                self._tourney = db.getRecord("TOURNEY_DATA")
            except:
                self._tourney = None
                
            if not self._tourney:
                msg = "No tournament data in %s" % dlg.GetPath()
                edlg = wxMessageDialog(self, msg, "Error Opening File",
                                       style=wxOK|wxICON_ERROR)
                edlg.ShowModal()
                edlg.Destroy()
                trues = ["Run New Tournament", "Run Match"]
                self.enableMenus(self.parent.RunMenu, trues, ())
                trues = ["Open Tournament"]
                self.enableMenus(self.parent.FileMenu, trues, ())
                dlg.Destroy()
                return
                
            tourngui.showTournamentControlPanel(self._tourney,
                                                self._doMatchStartup,
                                                self._stopTourney,
                                                dlg.GetPath())

        dlg.Destroy()

    def exportWrestler(self, evt):
        wrestlers, wrestlerInfo = dblib.getWrestlerDictAndList()
        dlg = SelectDialog("Export Wrestler", wrestlerInfo,
                           "Select a wrestler to export.", single_select=1)
        if dlg.ShowModal() == wxID_OK:
            wrestlerMod = wrestlers[dlg.GetSelection()]
            from lib.spw import Wrestler
            wrestler = Wrestler(wrestlerMod)
            
            from lib import actionCard
            path = getFileSavePath(self,
                                   "Export %s to PDF" % wrestler.getName(),
                                   "Portable Document Format (*.pdf)|.pdf")
            if path:
                actionCard.PdfActionCard(wrestler).writePDF(path)
        dlg.Destroy()

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        dc.Clear()
        img = wx.Image(os.path.join(JOWST_PATH, "resources", "wood-6.jpg"))
        winSize = self.GetClientSizeTuple()
        img = img.Scale(winSize[0], winSize[1])
        dc.DrawBitmap(wx.BitmapFromImage(img), 0, 0)
        
        
class JowstTeamFrame(wxPanel):
    def __init__(self, parent, team):
        wxPanel.__init__(self, parent, -1, style=wxSIMPLE_BORDER)
        self.parent = parent
        jtfSzr = wxBoxSizer(wxVERTICAL)
        self.lblDict = {}
        self.team = team
        self._wrestlers = []
        self._textLabels = []
        self.lblBox = wxBoxSizer(wxVERTICAL)
        
        dtAndScoreItems = (("scoreBox", "scoreLabel", "%-22s"%"Total Score:",
                            "totalScore",(40, 20)),
                           ("dtBox", "dtLabel", "Double Team Rounds: ",
                            "dtRoundCounter", (20, 20)))
        
        dtAndScoreBox = wxBoxSizer(wxVERTICAL)
        for boxName, lblName, lblTxt, intCtrlName, size in dtAndScoreItems:
            setattr(self, boxName, wxBoxSizer(wxHORIZONTAL))
            setattr(self, lblName, makeBold(wxStaticText(self, -1, lblTxt)))
            getattr(self, boxName).Add(getattr(self, lblName), 0)
            setattr(self, intCtrlName, wxLEDNumberCtrl(self, -1, size=size))
            intCtrl = getattr(self, intCtrlName)
            intCtrl.SetAlignment(wxLED_ALIGN_CENTER)
            intCtrl.SetValue("0")
            getattr(self, boxName).Add(getattr(self, intCtrlName), 0)
            dtAndScoreBox.Add(getattr(self, boxName), 0)
            dtAndScoreBox.Add((0, 2))
            
        # Team members and double team round box
        self.teamHeadBox = wxBoxSizer(wxHORIZONTAL)
        self.teamHeadBox.Add(self.lblBox, 1, wxEXPAND)
        self.lblList = []
        for boxnum in range(3):
            self.lblList.append(wxStaticText(self, -1, ""))
            self.lblBox.Add(self.lblList[boxnum], 1, wxEXPAND)
        self.currLblIdx = 0    
        self.teamHeadBox.Add(dtAndScoreBox, 0, wxALIGN_LEFT)

        # ActionCard Window
        self.acWin = ActionCardWin(self, self.team)

        # Team Buttons
        self.teamButtonBox = wxBoxSizer(wxHORIZONTAL)
        self.tagButton = wxButton(self, -1, "Tag Out...")
        EVT_BUTTON(self, self.tagButton.GetId(), self._tagOutClick)
        self.viewTeamButt = wxButton(self, -1, "View Team Member...")
        EVT_BUTTON(self, self.viewTeamButt.GetId(), self._viewTeamMemberClick)
        self.teamButtonBox.Add(self.tagButton, 0)
        self.teamButtonBox.Add(self.viewTeamButt,0)
        self.teamButtonBox.Add((5, 0))

        # Set up Team Frame
        jtfSzr.Add(self.teamHeadBox, 1, wxEXPAND)
        jtfSzr.Add((1,10))
        jtfSzr.Add(self.acWin, 8, wxEXPAND)
        jtfSzr.Add((1,10))
        jtfSzr.Add(self.teamButtonBox, 1, wxEXPAND)
        jtfSzr.Fit(self)
        self.SetSizer(jtfSzr)
        
        self.taggedOut = False
        self._manIn = None
        self.tagOutEligible = False
        self.tagButton.Enable(False)
        
    def addWrestler(self, man):
        name = man.getName()
        self._wrestlers.append(man)
        self.lblDict[name] = self.lblList[self.currLblIdx]
        self.lblDict[name].SetLabel(name)
        self.Layout()
        wxYieldIfNeeded()
        self.currLblIdx += 1
        
    def clearLabels(self):
        for name in self.lblDict.keys():
            self.lblDict[name].SetLabel("")
            if self.lblDict[name].GetBackgroundColour() != self.parent.defaultBG_Color:
                self.lblDict[name].SetBackgroundColour(self.parent.defaultBG_Color)
            self.Layout()
            wxYieldIfNeeded()
        self.lblDict = {}
        self.currLblIdx = 0
        
    def updateChoices(self, choicelist, prompt, caption):
        self._choicelist = choicelist
        self._prompt = prompt
        self._caption = caption

    def _tagOutClick(self, evt):
        if not self.tagOutEligible:
            dlg = wxMessageDialog(self, "You cannot tag out now.",
                          "Ineligible to tag.", wxOK | wxICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        dlg = wxSingleChoiceDialog(self, self._prompt, self._caption,
                                   self._choicelist[1:], wxOK|wxCANCEL)
        if dlg.ShowModal() == wxID_OK:
            self.parent.handlePromptResult(dlg.GetSelection() + 1,
                                           data=TAG_OUT_OCCURRED)
        dlg.Destroy()

    def _viewTeamMemberClick(self, evt):

        if not len(self._wrestlers):
            dlg = wxMessageDialog(self, "No team members to view.",
                                  "No team.", wxOK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        if len(self._wrestlers) > 1:
            WrestlerViewer(self, self._wrestlers)                    
        
    def setManIn(self, w):
        self._manIn = w
        for man in self.lblDict.keys():
            f = self.lblDict[man].GetFont()
            if not man == self._manIn.getName():
                f.SetWeight(wxNORMAL)
            else:
                f.SetWeight(wxBOLD)
            self.lblDict[man].SetFont(f)
            self.lblDict[man].Layout()
        wxYieldIfNeeded()
        
    def getManIn(self): return self._manIn

    def cleanup(self):
        self.totalScore.SetValue("0")
        self.dtRoundCounter.SetValue("0")
        self.currLblIdx = 0
        self._wrestlers = []
        self.clearLabels()
        self.destroyTextLabels()

    def addTextLabel(self, name, text, fgcolor, bgcolor, size):
        ctrl = wxTextCtrl(self, -1, text,
                          style=wxTE_READONLY|wxSIMPLE_BORDER|wxTE_CENTRE,
                          size=size)
        
        setattr(self, name, ctrl)
        ctrl.fgcolor = fgcolor
        ctrl.bgcolor = bgcolor
        ctrl.tip = wxToolTip("")
        ctrl.SetToolTip(ctrl.tip)
        self.teamButtonBox.Add(ctrl, 0, wxLEFT|wxRIGHT, border=2)
        self.Layout()
        self.disableTextLabel(name)
        self._textLabels.append(name)

    def enableTextLabel(self, name, tooltip):        
        ctrl = getattr(self, name)
        if not ctrl.IsEnabled():
            ctrl.Enable(1)
            ctrl.SetBackgroundColour(wxNamedColour(ctrl.bgcolor))
            ctrl.SetForegroundColour(wxNamedColour(ctrl.fgcolor))
            ctrl.Refresh()
        if tooltip:
            ctrl.tip.SetTip(tooltip)
            
    def disableTextLabel(self, name):
        ctrl = getattr(self, name)
        if ctrl.IsEnabled():
            ctrl.Disable()
        ctrl.tip.SetTip("")
        
    def destroyTextLabels(self):
        for label in self._textLabels:
            getattr(self, label).Destroy()
        self._textLabels = []
        
class ScoreCard(wxGrid):
    def __init__(self, parent, timelimit, teams, totalScoreWidgets=None):
        wxGrid.__init__(self, parent, -1)

        # No individual match should go more than 2 hrs.
        # Eventually we'll do a dynamic scorecard.
        if timelimit == NO_TIME_LIMIT: timelimit = 120
        self.totalWidgets = totalScoreWidgets
        
        self.CreateGrid(5, timelimit+2)
        self.SetColLabelSize(0)
        self.SetRowLabelSize(0)
        self.SetGridLineColour(wxNamedColour("WHITE"))
        self.EnableEditing(False)
        self.SetCellHighlightPenWidth(0)
        self.DisableDragGridSize()
        
        self._drawCell(0, 0, 2, timelimit+2, "scorecard", HeaderRenderer(BOLD))
        self._drawCell(2, 0, 1, 1, "Wrestler", HeaderRenderer(BOLD))
        
        # Round Headers
        for col in range(1, timelimit+1):
            self._drawCell(2, col, 1, 1, str(col), HeaderRenderer(BOLD))

        namerow = 3
        for team in teams:
            self._drawCell(namerow, 0, 1, 1, team, HeaderRenderer(ALL,
                                                                  borderColor="BLACK"))
            namerow += 1

        # Draw scorecard boxes
        for col in range(1, timelimit+1):
            self._drawCell(3, col, 1, 1, "", HeaderRenderer(ALL,
                                                            borderColor="BLACK"))
            self._drawCell(4, col, 1, 1, "", HeaderRenderer(ALL,
                                                            borderColor="BLACK"))

        self.teamScore = [[], []]

        # The 3 and 4 below are placeholders for the first element in the list,
        #  so the actual scoring will start in the second element in the list.
        self.teamScore[0] = [3] + [0] * timelimit
        self.teamScore[1] = [4] + [0] * timelimit
        self.col = 1
        
        self.AutoSize()
        self.SetAutoLayout(1)
                       
    def _drawCell(self, row, col, rspan, cspan, strText, rndrobj):
        self.SetCellSize(row, col, rspan, cspan)
        self.SetCellValue(row, col, strText)
        self.SetCellRenderer(row, col, rndrobj)

    def updateScore(self, team, points):
        row = self.teamScore[team][0]
        if self.col != 1 and self.teamScore[team][self.col] < 1:
            self.teamScore[team][self.col] = self._findNonZeroScore(team)

        self.teamScore[team][self.col] += points
        
        score = self.teamScore[team][self.col]
        self.SetCellValue(row, self.col, str(int(score)))
        if self.totalWidgets:
            self.totalWidgets[team].SetValue(str(int(score)))

        cellWidthIdx = len(str(int(score))) - 1
        if self.GetColSize(self.col) <= SCORECARD_CELL_WIDTHS[cellWidthIdx]:
            self.SetColSize(self.col, SCORECARD_CELL_WIDTHS[cellWidthIdx])
        self.Refresh()
        
    def _findNonZeroScore(self, team):
        tmpList = self.teamScore[team][1:]
        tmpList.reverse()
        for score in tmpList:
            if score > 0:
                return score
        return 0
        
    def nextRound(self):
        self.col += 1

    def currentRound(self):
        return self.col
        
class ActionCardWin(wxGrid):
    def __init__(self, parent, team):
        wxGrid.__init__(self, parent, -1)
        self.team = team
        self.parent = parent
        # Store column sizes for wrestler moves in the wrestlerMap dict
        self.wrestlerMap = {}
        self.SetSize(wxSize(300,400))
        self.CreateGrid(26, 3)
        self.SetGridLineColour(wxNamedColour("FOREST GREEN"))
        self.SetColLabelSize(0)
        self.SetRowLabelSize(0)
        self.EnableEditing(False)
        self.SetCellHighlightPenWidth(0)
        self.DisableDragGridSize()
        self._setupActionCard()
        
    def _setupActionCard(self):
        self._drawCell(0, 0, 1, 2, "", HeaderRenderer(ALL|BOLD))
        self._drawCell(GC_START_ROW, 0, 1, 2, "GENERAL CARD",
                       HeaderRenderer(ALL|BOLD))

        self._twoD6_box("GC")

        self._drawCell(DC_START_ROW, 0, 1, 2, "DEFENSIVE CARD",
                       HeaderRenderer(ALL|BOLD))
        self._twoD6_box("DC")

        self._drawCell(SPECIALTY_START_ROW, 0, 1, 2, "SPECIALTY:",
                       HeaderRenderer(ALL|BOLD))
        currRow = SPECIALTY_START_ROW + 1
        self._drawCell(currRow, 0, 1, 2, "", HeaderRenderer(EAST|WEST))

        currRow += 1
        for row in range(currRow, currRow + 6):
            self._drawCell(row, 0, 1, 2, "", GenericRenderer(EAST|WEST))

        subStr = "%-10s: " % ("SUB%s" % (" "* 11))
        self._drawCell(SUB_ROW, 0, 1, 2, subStr,
                       GenericRenderer(EAST|WEST|NORTH))
       
        tagStr = "%-10s: " % ("TAG-TEAM")
        self._drawCell(TAG_TEAM_ROW, 0, 1, 2, tagStr,
                       GenericRenderer(EAST|WEST))

        priStr = "%-10s: " % ("PRIORITY   ")
        self._drawCell(PRIORITY_ROW, 0, 1, 2, priStr,
                       GenericRenderer(EAST|WEST|SOUTH))            

        self._drawCell(OFFENSIVE_CARD_START_ROW, 2, 1, 1, "OFFENSIVE CARD",
                       HeaderRenderer(ALL|BOLD))
        self._drawMoveList(OFFENSIVE_CARD_START_ROW + 1, 11)

        self._drawCell(ROPES_START_ROW, 2, 1, 1, "=ROPES=",
                       HeaderRenderer(ALL|BOLD))
        self._drawMoveList(ROPES_START_ROW + 1, 11)
        
        self._setDefaultColSizes()
       
    def _twoD6_box(self, cardType):
        
        if cardType == "GC":
            startRow = GC_START_ROW + 1
        else:
            startRow = DC_START_ROW + 1

        cardIdx = 0
        for col in (0, 1):
            for row in range(startRow, startRow + 5):
                self.SetCellValue(row, col, "")

                if col == 0: flags = WEST
                else: flags = EAST

                self.SetCellRenderer(row, col, GenericRenderer(flags))

        self.SetCellSize(startRow + 5, 0, 1, 2)
        self.SetCellAlignment(startRow + 5, 0, wxALIGN_CENTER, -1)
        self.SetCellValue(startRow + 5, 0, "")
        self.SetCellRenderer(startRow + 5, 0,
                             GenericRenderer(EAST|WEST|CENTER_TEXT))

    def _drawMoveList(self, startRow, numMoves):
        for pos in range(0, numMoves):
            self._drawCell(startRow + pos, 2, 1, 1, "", GenericRenderer(EAST))
        
    def _setDefaultColSizes(self, name=None):
        self.SetColSize(0, DEFAULT_COL_SIZE)
        self.SetColSize(1, DEFAULT_COL_SIZE)
        self.SetColSize(2, DEFAULT_MOVE_COL_SIZE)

        self.FitInside()
        self.Refresh()
        
    def _drawCell(self, row, col, rspan, cspan, strText, rndrobj):
        self.SetCellSize(row, col, rspan, cspan)
        self.SetCellValue(row, col, strText)
        self.SetCellRenderer(row, col, rndrobj)
        

    def GetCellRenderer(self, row, col):
        r = wxGrid.GetCellRenderer(self, row, col)
        text = wxGrid.GetCellValue(self, row, col)
        x, y, w, h = wxGrid.CellToRect(self, row, col)
        r.setRendererAttrs((row, col, text, self, x, y, w, h))
        wxYieldIfNeeded()
        return r
        
    def populateActionCard(self, wrestler):
        name = wrestler.getName()
        self.currWrestler = name
        self.SetCellValue(0, 0, name)
        self._populateTwoD6_box("GC", wrestler)
        self._populateTwoD6_box("DC", wrestler)

        currRow = SPECIALTY_START_ROW + 1
        specMove = wrestler.getSpecialtyCard()[0]["MOVE_NAME"]
        self.SetCellValue(currRow, 0, specMove)

        currRow += 1
        specList = wrestler.getSpecialtyCard()

        cardIdx = 0

        for move in specList:
            moveType = convertToString(move["MOVE_TYPE"])
            if moveType not in ("*", "P/A", "(DQ)"):
                moveType = ""
            if moveType == "(DQ)":
                movePoints = ""
            else:
                movePoints = move["MOVE_POINTS"]
                
            strEntry = "%-4s%s %s" % (str(cardIdx + 1), movePoints, moveType)
            self.SetCellValue(currRow, 0, strEntry)
            currRow += 1
            cardIdx += 1

        subStr = "%-10s: %s" % ("SUB%s" % (" "* 11),
                                convertRangeTupleToString(wrestler.getSubmissionRange()))
        self.SetCellValue(SUB_ROW, 0, subStr)
       
        tagStr = "%-10s: %s" % ("TAG-TEAM",
                                convertRangeTupleToString(wrestler.getTagTeamRange()))
        self.SetCellValue(TAG_TEAM_ROW, 0, tagStr)

        priStr = "%-10s: %s/%s" % ("PRIORITY   ",
                                   convertPriorityToString(wrestler.getSinglesPriority()),
                                   convertPriorityToString(wrestler.getTagTeamPriority()))
        self.SetCellValue(PRIORITY_ROW, 0, priStr)            

        self._populateMoveList(wrestler.getOffensiveCard(), OFFENSIVE_CARD_START_ROW + 1)
        self._populateMoveList(wrestler.getRopesCard(), ROPES_START_ROW + 1)

        self.Refresh()
        wxYieldIfNeeded()
       
    def _populateTwoD6_box(self, cardType, wrestler):
        w = wrestler
        cardList = []
        
        if cardType == "GC":
            wCardList = w.getGeneralCard()
            startRow = GC_START_ROW + 1
        else:
            wCardList = w.getDefensiveCard()
            startRow = DC_START_ROW + 1

        cardIdx = 0
        for col in (0, 1):
            for row in range(startRow, startRow + 5):
                strNum = str(cardIdx + 2)
                strMove = convertToString(wCardList[cardIdx])
                strEntry = "%-4s%s" % (strNum, strMove)
                self.SetCellValue(row, col, strEntry)

                cardList.append((row, col)) # Remember Position
                cardIdx += 1

        strEntry = "%-4s%s" % ("12", convertToString(wCardList[10]))
        self.SetCellValue(startRow + 5, 0, strEntry)
        cardList.append((startRow + 5, 0))

        if cardType == "GC":
            self.gcList = cardList
        else:
            self.dcList = cardList

    def _populateMoveList(self, moveList, startRow):
        i = 0
        for move in moveList:
            strMoveNum = str(i+2)
            moveName = move["MOVE_NAME"]
            moveType = convertToString(move["MOVE_TYPE"])
            if moveType not in ("(DQ)", "(S)") and \
               moveName not in ("ROPES", "NA"):
                strMovePoints = str(move["MOVE_POINTS"])
            else:
                strMovePoints = ""
            strEntry = "%-4s%s  %s %s" % (strMoveNum, moveName,
                                          strMovePoints, moveType)
            self.SetCellValue(startRow + i, 2, strEntry)
            i += 1             
        
    def OnPaint(self, event):
        dc = wxPaintDC(self)
        self.PrepareDC(dc)
        dc.BeginDrawing()
        dc.SetPen(wxPen('GREEN'))
        dc.DrawRectangle(0,0,112,13)
        dc.EndDrawing()


class WrestlerViewer:
    def __init__(self, parent, wrestlers=[], name_and_set=0):
        self.parent = parent
        self.wrestlers = wrestlers
        self.wrestlerNames = map(lambda x: x.getName(), wrestlers)
        if len(self.wrestlers) == 1:
            self.wrestler = self.wrestlers[0]
            self.showActionCard()
        else:    
            if not name_and_set: self.showWrestlerSelectPrompt()
            else: self.showWrestlerSelectPromptWithSet()
        
    def showWrestlerSelectPrompt(self):
        dlg = wxSingleChoiceDialog(self.parent, "Select wrestler to view.",
                                   "View Team Member",
                                   self.wrestlerNames, wxOK|wxCANCEL)
        if dlg.ShowModal() == wxID_OK:
            self.wrestler = self.wrestlers[dlg.GetSelection()]
            self.showActionCard()
        dlg.Destroy()
            
    def showWrestlerSelectPromptWithSet(self):
        wrestlerInfo = []
        idx = 0
        for wrestler in self.wrestlers:
            wrestlerInfo.append((wrestler.getName(), wrestler.getNameSet(),
                                 str(idx)))
            idx += 1
            
        dlg = SelectDialog("View Wrestler", wrestlerInfo,
                           "Select a wrestler to view.", single_select=1)
        if dlg.ShowModal() == wxID_OK:
            self.wrestler = self.wrestlers[int(dlg.GetSelection())]
            self.showActionCard()
        dlg.Destroy()
        
    def showActionCard(self):
        frame = wxFrame(self.parent, -1, self.wrestler.getName(),
                        size=(440, 501))
        menubar = wxMenuBar()
        fileMenu = wxMenu()
        exportID = wxNewId()
        fileMenu.Append(exportID, "Export...")
        EVT_MENU(frame, exportID, self._exportActionCard)
        exitID = wxNewId()
        fileMenu.Append(exitID, "Exit")
        EVT_MENU(frame, exitID, self._viewerClose)
        menubar.Append(fileMenu, "&File")
        frame.SetMenuBar(menubar)
        
        frame.win = ActionCardWin(frame, 1)
        EVT_CLOSE(frame, self._viewerClose)
        frame.win.populateActionCard(self.wrestler)
        setIcon(frame)
        frame.Center()
        frame.Show(1)

    def _viewerClose(self, evt):
        evt.GetEventObject().Destroy()

    def _exportActionCard(self, evt):
        from lib import actionCard
        path = getFileSavePath(self.parent, "Export Wrestler to PDF",
                               "Portable Document Format (*.pdf)|.pdf")
        if path:
            actionCard.PdfActionCard(self.wrestler).writePDF(path)
        
        
class AboutWin(wxDialog):
    def __init__(self, parent):
        self.text = '''<HTML><BODY LANG="en-US" BGCOLOR="#000000">
<H1 ALIGN=CENTER><FONT COLOR="#ff0000">Pro Wrestling Superstar</FONT></H1>
<P ALIGN=CENTER><FONT COLOR="#ff0000"><B>v %s</B></FONT></P>
<HR>
<P ALIGN=CENTER STYLE="font-weight: medium"><FONT COLOR="#ff0000">Copyright
2003 John LeGrande</FONT></P>
<P ALIGN=CENTER STYLE="font-weight: medium"><FONT COLOR="#ff0000">Please
see <I>license.txt</I> for licensing information</FONT></P>
<p ALIGN=CENTER><wxp module="wx" class="Button">
    <param name="label" value="OK">
    <param name="id"    value="ID_OK">
</wxp></p>
</BODY>
</HTML>''' % VERSION
        import wx
        import wx.html
        import wx.lib.wxpTag

        wxDialog.__init__(self, parent, -1, 'Pro Wrestling Superstar',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        html.SetPage(self.text)
        btn = html.FindWindowById(wx.ID_OK)
        btn.SetDefault()
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)
        

class ChatPanel(wxPanel):
    def __init__(self, parent, sendMsg):
        self.sendMessage = sendMsg
        wxPanel.__init__(self, parent, -1)
        mainSzr = wxBoxSizer(wxVERTICAL)
        self.msgWin = wxTextCtrl(self, -1, style=wxTE_MULTILINE|wxTE_READONLY)
        mainSzr.Add(self.msgWin, 5, wxEXPAND)
        mainSzr.Add((0, 10))
        inputSzr = wxBoxSizer(wxHORIZONTAL)
        self.textEntry = wxTextCtrl(self, -1, style=wxTE_PROCESS_ENTER)
        inputSzr.Add(self.textEntry, 10, wxEXPAND)
        inputSzr.Add((10, 0))
        self.sendTextButt = wxButton(self, -1, "Send Text")
        EVT_BUTTON(self, self.sendTextButt.GetId(), self._sendText)
        inputSzr.Add(self.sendTextButt, 0, wxEXPAND)
        mainSzr.Add(inputSzr, 0, wxEXPAND)
        EVT_TEXT_ENTER(self, self.textEntry.GetId(), self._sendText)

        # Layout Chat Panel
        mainSzr.Fit(self)
        self.SetSizer(mainSzr)
        self.SetAutoLayout(1)
        mainSzr.Layout()
        

    def _sendText(self, evt):
        self.sendMessage(self.textEntry.GetValue())
        self.textEntry.Clear()

    def receiveMsg(self, player, msg):
        self.msgWin.AppendText("<%s> %s" % (player, msg))

    def setChatCB(self, chatCB):
        self.sendMessage = chatCB


class BaseHighlighter:
    def __init__(self):
        self.flash = None
        self.row = None
        self.col = None
        self.text = None
        self.grid = None
        self.x = self.y = self.width = self.height = None
        self._highlightFlag = None

    def startHighlightMode(self, flash=None):
        self.flash = flash
        if self.flash:
            global _highLighterThread
            _highLighterThread.start(self.grid.parent, (self.row, self.col,
                                                        self.text,
                                                        self.grid.team))
        else:
            self._highlightFlag = 1
            self.grid.SetCellValue(self.row, self.col, self.text)
            wxYieldIfNeeded()

    def stopHighlightMode(self):
        global _highLighterThread
        if _highLighterThread.isRunning():
            _highLighterThread.stop()
            time.sleep(.25)
        self._highlightFlag = None
        self.grid.SetCellValue(self.row, self.col, self.text)
        wxYieldIfNeeded()
        
    def setHighlightFlag(self, flag):
        self._highlightFlag = flag

    def setRendererAttrs(self, attrs):
        self.row, self.col, self.text, self.grid, self.x, self.y, self.width,\
                  self.height = attrs
        
class GenericRenderer(wxPyGridCellRenderer, BaseHighlighter):
    def __init__(self, flags=None, borderColor=None):
        wxPyGridCellRenderer.__init__(self)
        BaseHighlighter.__init__(self)
        
        self.flags = flags
        self._cellLocked = None
        self._highlightFlag = None
        self._membersSet = None
        self.hlThread = None
        self.grid = None
        if borderColor:
            self.borderColor = borderColor
        else:
            self.borderColor = "DARK GREEN"
        
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        if self._highlightFlag:
            brush = wxBrush("YELLOW", wxSOLID)
        else:
            brush = wxBrush(wxWHITE, wxSOLID)
        
        dc.SetBackgroundMode(wxSOLID)
        dc.SetBrush(brush)
        dc.SetPen(wxTRANSPARENT_PEN)
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)
        if self.flags:
            drawBorder(rect, dc, self.flags, self.borderColor)

        dc.SetBackgroundMode(wxTRANSPARENT)
        strNumFont = attr.GetFont()
        strNumFont.SetWeight(wxBOLD)

        strTextFont = attr.GetFont()
        dc.SetFont(strNumFont)

        # Text parsing hack.  Relatively flexible, but needs to be
        #  reworked.
        text = grid.GetCellValue(row, col)
        self.text = text
        matchObj= re.match("\D+:|\d+", text)
        if not matchObj:
            fieldEnd = 0
            strText = strNum = specMove = ""
        else:
            fieldEnd = matchObj.end()
            strText = text[fieldEnd:]
            strNum = text[0:fieldEnd]
            try:
                specMove = string.split(strText)[-1]
            except:
                specMove = ""

        if specMove != "(S)": specMove = ""
        else:
            strText = strText[0:-4]
            
        try:
            intNum = int(strNum)
        except ValueError:
            intNum = -1

        x = rect.x + 1
        y = rect.y + 1
        if intNum == 12 and self.flags&CENTER_TEXT:
            tmpW, tmpH = dc.GetTextExtent(text)
            midPt = round(rect.width / 2)
            midStr = round(tmpW / 2)
            x = int(midPt - midStr) + 1
            
        for rndrStr in (strNum, strText):
            #dc.SetTextForeground(random.choice(colors))
            dc.DrawText(rndrStr, x, y)
            w, h = dc.GetTextExtent(rndrStr)
            x = x + w

            # Pad for single-digit numbers
            if intNum < 10 and intNum > -1: x += 3 
            if x > rect.right - 5:
                break
            dc.SetFont(strTextFont)

        if len(specMove):
            specFont = attr.GetFont()
            specFont.SetWeight(wxBOLD)
            dc.SetFont(specFont)
            dc.DrawText(specMove, x, y)
        
    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wxSize(w, h)

        
class HeaderRenderer(wxPyGridCellRenderer, BaseHighlighter):
    def __init__(self, flags=None, borderColor=None):
        wxPyGridCellRenderer.__init__(self)
        BaseHighlighter.__init__(self)
        
        self.flags = flags
        self.grid = None
        self.rect = None
        self.dc = None
        self._highlightFlag = None
        self._cellLocked = None
        self.hlThread = None
        if borderColor:
            self.borderColor = borderColor
        else:
            self.borderColor = "DARK GREEN"

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        if self._highlightFlag:
            brush = wxBrush("YELLOW", wxSOLID)
        else:
            brush = wxBrush(wxWHITE, wxSOLID)

        dc.SetBackgroundMode(wxSOLID)
        dc.SetBrush(brush)
        dc.SetPen(wxTRANSPARENT_PEN)
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)
        if self.flags:
            drawBorder(rect, dc, self.flags, self.borderColor)
            
        dc.SetBackgroundMode(wxTRANSPARENT)
        textFont = attr.GetFont()
        if self.flags&BOLD:
            textFont.SetWeight(wxBOLD)
            
        dc.SetFont(textFont)

        text = grid.GetCellValue(row, col)
        self.text = text

        w, h = dc.GetTextExtent(text)
        midPt = round(rect.width / 2)
        midStr = round(w / 2)
        x = rect.x + int(midPt - midStr) + 1
        y = rect.y + 1
            
        dc.DrawText(text, x, y)
        
    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wxSize(w, h)


class HighlighterThread:
    def __init__(self):
        self.win = None
        self.data = None
        self._highlightMode = None
        self._isRunning = False
        self.threadQueue = Queue.Queue()
        self.keepGoing = threading.Event()
        self.keepGoing.set()
        self.hlStopped = threading.Event()
        threading.Thread(target=self._doHighlight).start()

    def start(self, parent, data):
        self._isRunning = True
        self._highlightMode = threading.Event()
        self._highlightMode.set()
        self.threadQueue.put((parent.parent, data)) #Main Window, renderer data
        
    def stop(self, shutdown=None):
        if self._highlightMode:
            self._highlightMode.clear()
            self.hlStopped.wait()
        if shutdown:
            self.keepGoing.clear()
            self.threadQueue.put((None, None))
        
    def _doHighlight(self):
        while self.keepGoing.isSet():
            win, data = self.threadQueue.get()
            highlightFlag = 1
            self._isRunning = True
            self.hlStopped.clear()
            while self._highlightMode and self._highlightMode.isSet():
                evt = UpdateHighlighter(data, highlightFlag)
                wxPostEvent(win, evt)
                highlightFlag = not highlightFlag
                for timeslice in range(100):
                    if not self._highlightMode.isSet(): break
                    time.sleep(.01)
            self._isRunning = False
            if win and data:
                evt = UpdateHighlighter(data, None)
                wxPostEvent(win, evt)
            self.hlStopped.set()
        self._isRunning = False
        self.hlStopped.set()
         
    def isRunning(self):
        return self._isRunning
    
# Event code for highlighter thread
wxEVT_UPDATE_HIGHLIGHTER = wxNewEventType()

def EVT_UPDATE_HIGHLIGHTER(win, func):
    win.Connect(-1, -1, wxEVT_UPDATE_HIGHLIGHTER, func)

    
class UpdateHighlighter(wxPyEvent):
    def __init__(self, data, isHighlighted=None):
        wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_UPDATE_HIGHLIGHTER)
        self.isHighlighted = isHighlighted
        self.row = data[0]
        self.col = data[1]
        self.text = data[2]
        self.team = data[3]

_highLighterThread = None
def startHighlighterThread():
    global _highLighterThread
    _highLighterThread = HighlighterThread()

def shutdownHighlighterThread():
    global _highLighterThread
    _highLighterThread.stop(shutdown=1)

from gui import diceRoll
class ButtonColumn(wxBoxSizer):
    def __init__(self, parent):
        wxBoxSizer.__init__(self, wxVERTICAL)
        timeSzr = wxBoxSizer(wxVERTICAL)
        timeSzr.Add(makeBold(wxStaticText(parent, -1, "Match Time")), 0,
                    wxALIGN_CENTER)
        timeSzr.Add((0, 5))
        self.matchTime = wxLEDNumberCtrl(parent, -1, (-1,-1), (80,25))
        self.matchTime.SetAlignment(wxLED_ALIGN_RIGHT)
        self.matchTime.SetValue("0-00")
        timeSzr.Add(self.matchTime, 0, wxALIGN_CENTER|wxEXPAND)
        self.rollDiceButt = wxButton(parent, ROLL_DICE_BUTTON, "Roll Dice")
        wxInitAllImageHandlers()
        jpg = wxEmptyBitmap(80, 80)
        self.matchImage = wxStaticBitmap(parent, -1, jpg, (-1, -1), (80, 80))
        self.setMatchImage()
        
        self.Add(timeSzr, 0, wxALIGN_CENTER)
        self.Add((0, 20))
        self.Add(self.matchImage, 0)
        self.Add((0, 20))
        diceSizer = wxBoxSizer(wxHORIZONTAL)
        self.dieOne = diceRoll.DiceRoll(parent)
        self.dieTwo = diceRoll.DiceRoll(parent)

        diceSizer.Add(self.dieOne, 0, wxALIGN_CENTER_VERTICAL)
        diceSizer.Add(self.dieTwo, 0, wxALIGN_CENTER_VERTICAL)
        self.Add(diceSizer, 0)
        self.Add((0, 10))
        self.Add(self.rollDiceButt, 3, wxSHAPED|wxALIGN_TOP)

    def setMatchImage(self, matchType="Regular", imagefile=None):
        mTypes = {"Regular":"regularMatch.jpg",
                  "Steel Cage":"cageMatch.jpg",
                  "Texas Death":"texasDeath.jpg"}
        if imagefile:
            mTypes[matchType] = imagefile
        
        ipath = os.path.normpath(os.path.join(JOWST_PATH, "resources",
                                              mTypes[matchType]))
        img = wxImage(ipath)
        img.Rescale(80, 80)
        self.matchImage.SetBitmap(wxBitmapFromImage(img))
            


class JowstFrame(wxFrame):
    def __init__(self, title):
        wxFrame.__init__(self, None, -1, title, size=(1024, 768))
        EVT_CLOSE(self, self.OnClose)
        self.jWin = MainJowstWindow(self)
        self.buildMenu()
        self.Show(1)
        self.Center(wxBOTH)
        startHighlighterThread()
        
    def buildMenu(self):
        menuDict =      {"&File":(("New Wrestler", True,
                                   self.jWin.startWrestlerBuilder),
                                  ("New Card", False, None),
                                  ("New Results Database", True,
                                   self.newResultsDB),
                                  ("Open Results Database", True,
                                   self.openResultsDB),
                                  ("Open Tournament", True,
                                   self.jWin.openTournament),
                                  ("SEPARATOR", True, None),
                                  ("Export Wrestler", True,
                                   self.jWin.exportWrestler),
                                  ("SEPARATOR", True, None),
                                  ("Delete Wrestlers", True,
                                   self.deleteWrestlers),
                                  ("Delete Results Database", True,
                                   self.deleteResultsDB),
                                  ("SEPARATOR", True, None),
                                  ("E&xit", True, self.OnClose)),
                         "&Run":(("Run Match", True, self.jWin.setupMatch),
                                 ("Run Card", False, None),
                                 ("Run New Tournament", True,
                                  self.jWin.startTourney),
                                 ("SEPARATOR", True, None),
                                 ("End Match", False, self.jWin.endMatch),
                                 ("End Card", False, None)),
                         "&View":(("View Wrestler", True,
                                   self.jWin.viewWrestler),
                                  ("View Card", False, None)),
                         "&Network":(("Start Network Game", True,
                                      self.jWin.setupNetworkMatch),
                                     ("Connect To Server", True,
                                      self.jWin.connectToNetworkMatch),
                                     ("SEPARATOR", True, None),
                                     ("Stop Network Game", False,
                                      self.jWin.stopNetworkGame),
                                     ("Stop Server", False,
                                      self.jWin.stopServer),
                                     ("Disconnect From Server", False ,
                                      self.jWin.disconnFromServer)),
                         "&Sound":(("Match Sounds", True,
                                    self.jWin.setMatchSounds),
                                   ("Dice Roll Sounds", True,
                                    self.jWin.setDiceRollSounds)),
                         "&Help":(("About...", True, self.jWin.showAboutWin),
                                  ("Start debugging", True, self.startLogging),
                                  ("Start Test", True, self.jWin.startTest),
                                  ("Stop Test", False, self.jWin.stopTest),
                                  ("View Debug Log", False,
                                   self.viewDebugLog),
                                  ("Open Log...", True, self.openLog))
                         }

        menuBar = wxMenuBar()
        for menuName in ("&File", "&Run", "&View", "&Network", "&Sound",
                         "&Help"):
            name = menuName.replace('&', '') + "Menu"
            setattr(self, name, wxMenu())
            for itemStr, enabled, cb in menuDict[menuName]:
                itemId = wxNewId()                
                if itemStr == "SEPARATOR":
                    getattr(self, name).AppendSeparator()
                else:
                    if itemStr in ("Match Sounds", "Dice Roll Sounds"):
                        getattr(self, name).AppendCheckItem(itemId, itemStr)
                        getattr(self, name).Check(itemId, 1)
                    else:
                        getattr(self, name).Append(itemId, itemStr)
                    getattr(self, name).Enable(itemId, enabled)
                if cb:
                    EVT_MENU(self, itemId, cb)
            menuBar.Append(getattr(self, name), menuName)
        self.SetMenuBar(menuBar)
        
    def startLogging(self, evt):
        if not self.app.logging:
            self.app.doLogging()
            self.HelpMenu.Enable(self.HelpMenu.FindItem("View Debug Log"), 1)

    def viewDebugLog(self, evt):
        logpath = self.app.logFilename
        if logpath:
            self.runEditor(logpath)

        if not logpath:
            dlg = wxMessageDialog(self, "Could not open debug log file",
                                  "Error Opening Log File", style=wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def openLog(self, evt):
        logdir = os.path.join(JOWST_PATH, "log")
        logpath = getFilePath(self, "Open Log File", "TEXT File (*.txt)|*.txt",
                              style=wxOPEN, curdir=logdir)
        self.runEditor(logpath)
        
    def runEditor(self, path):
        editor = os.environ.get("EDITOR", "vi")
        if sys.platform != "win32":
            retval = os.spawnlp(os.P_NOWAIT, editor, editor, path)
        else:
            os.startfile(path)
            retval = 0
        return retval
    
    def openResultsDB(self, evt):
        dlg = datagui.ResultDBSelector(self, "Open Results Database")
        dlg.addLabel("Select a results database to open")
        dlg.addDbSelector()
        if dlg.ShowModal() == wxID_OK:
            name, path = dlg.getNameAndPath()
            if not path:
                name = datagui.getNewResultDbName(self)
                path = dblib.getNewDbPath(name)
            datagui.ResultControlPanel(path, name)
        dlg.Destroy()

    def newResultsDB(self, evt):
        name = datagui.getNewResultDbName(self)
        if not name: return
        path = dblib.getNewDbPath(name)
        datagui.ResultControlPanel(path, name)
        
    def deleteWrestlers(self, evt):
        wrestlers, wrestlerInfo = dblib.getWrestlerDictAndList()
        dlg = SelectDialog("Delete Wrestlers", wrestlerInfo,
                           "Select Wrestlers to delete from the list below."
                           "\n\nHold down the 'CTRL' key to select multiple"
                           " wrestlers or to de-select wrestlers.",
                           parent=self)
        if dlg.ShowModal() == wxID_OK:
            selections = dlg.GetSelected()
            prompt = "Are you sure you want to delete the following wrestlers?"
            msgStr = ""
            for selection in selections:
                wrestler = wrestlers[selection]
                msgStr += "%s (%s)\n" % (wrestler.name,
                                         getattr(wrestler, "nameSet", ""))
            mdlg = ScrolledDialog(self, "%s\n\n" % msgStr,
                                  "Confirm Wrestler Deletion",
                                  prompt + "\n")
            if mdlg.ShowModal() == wxID_OK:
                pdlg = wxProgressDialog("Deleting Wrestlers",
                                        " " * 80,
                                        len(selections), self, wxPD_APP_MODAL)
                selidx = 0
                for selection in selections:
                    wrestler = wrestlers[selection]
                    wrestlerStr = "Deleting %s (%s)\n" % (wrestler.name,
                                                          getattr(wrestler,
                                                                  "nameSet",
                                                                  ""))
                    pdlg.Update(selidx, wrestlerStr)
                    fullpath = os.path.abspath(selection)
                    fPathNoExt = os.path.splitext(fullpath)[0]
                    os.unlink("%s.py" % fPathNoExt)
                    if os.path.exists("%s.pyc" % fPathNoExt):
                        os.unlink("%s.pyc" % fPathNoExt)
                    selidx += 1
                pdlg.Destroy()
                    
            mdlg.Destroy()
            

        dlg.Destroy()

        
        
        
    def deleteResultsDB(self, evt):
        dlg = datagui.ResultDBSelector(self, "Delete Results Database")
        dlg.addLabel("Select a results database to delete")
        dlg.addDbSelector(deleting=1)
        if dlg.lb.GetCount() < 1:
            mDlg = wxMessageDialog(self,
                                    "There are no databases to delete",
                                    "No Databases to Delete", style=wxOK)
            mDlg.ShowModal()
            mDlg.Destroy()
            return
            
        if dlg.ShowModal() == wxID_OK:
            choiceMade = 0
            name, path = dlg.getNameAndPath()
            while not choiceMade:
                mDlg = wxMessageDialog(self,
                                       "Are you sure you want to delete the "+\
                                       "%s database?" % name,
                                       "Confirm Deletion", style=wxYES_NO)
                if mDlg.ShowModal() == wxID_YES:
                    updateDataRegistry(name, path, "resultsRegistry", 1)
                    os.unlink(os.path.normpath(os.path.join(JOWST_PATH, path)))
                    choiceMade = 1
                    mDlg2 = wxMessageDialog(self,
                                            "%s database deleted" % name,
                                            "Database Deleted", style=wxOK)
                    mDlg2.ShowModal()
                    mDlg2.Destroy()
                mDlg.Destroy()
            
        dlg.Destroy()
        
    def OnClose(self, evt):
        # Try to cleanup, but there may be other loops running so we'll
        #  try to catch any additional exceptions
        try:
            self.jWin.endMatch(None)
        except:
            pass

        shutdownHighlighterThread()
        
        try:
            self.Destroy()
        except:
            pass

        # Make sure the interpreter dies...
        sys.exit()

def buildMenu(parent, menuDict, menus, checkitems=[]):
    menuBar = wxMenuBar()
    for menuName in menus:
        name = menuName.replace('&', '') + "Menu"
        setattr(parent, name, wxMenu())
        for itemStr, enabled, cb in menuDict[menuName]:
            itemId = wxNewId()                
            if itemStr == "SEPARATOR":
                getattr(parent, name).AppendSeparator()
            else:
                if itemStr in checkitems:
                    getattr(parent, name).AppendCheckItem(itemId, itemStr)
                    getattr(parent, name).Check(itemId, 1)
                else:
                    getattr(parent, name).Append(itemId, itemStr)
                getattr(parent, name).Enable(itemId, enabled)
            if cb:
                EVT_MENU(parent, itemId, cb)
        menuBar.Append(getattr(parent, name), menuName)
    parent.SetMenuBar(menuBar)
        
def getFileSavePath(parent, caption, wildcard):
    dbDir = os.path.join(JOWST_PATH, "db")
    dlg = wxFileDialog(parent, caption, dbDir, "",
                       wildcard, style=wxSAVE|wxOVERWRITE_PROMPT)

    path = None
    if dlg.ShowModal() == wxID_OK:
        path = dlg.GetPath()

    dlg.Destroy()
    
    return path

def getFilePath(parent, caption, wildcard, style, curdir=None):
    if not curdir:
        curdir = os.path.join(JOWST_PATH, "db")
    dlg = wxFileDialog(parent, caption, curdir, "",
                       wildcard, style=style)

    path = None
    if dlg.ShowModal() == wxID_OK:
        path = dlg.GetPath()

    dlg.Destroy()
    
    return path
        
# Disconnect Event
DISCONNECTED = wxNewEventType() 
 
def EVT_DISCONNECTED( window, function ): 
    """Event handler when someone disconnects from the server""" 
    window.Connect( -1, -1, DISCONNECTED, function ) 
 
class DisconnectedEvent(wxPyCommandEvent): 
    eventType = DISCONNECTED 
    def __init__(self, windowID, data):
        self.data = data
        wxPyCommandEvent.__init__(self, self.eventType, windowID) 
 
    def Clone( self ): 
        self.__class__( self.GetId() )

# Finish Event
FINISHED = wxNewEventType() 
 
def EVT_FINISHED( window, function ): 
    """Event handler when someone disconnects from the server""" 
    window.Connect( -1, -1, FINISHED, function ) 
 
class FinishedEvent(wxPyCommandEvent): 
    eventType = FINISHED 
    def __init__(self, windowID):
        wxPyCommandEvent.__init__(self, self.eventType, windowID) 
 
    def Clone( self ): 
        self.__class__( self.GetId() )
        
# Disconnect Event
MSG_ARRIVED = wxNewEventType() 
 
def EVT_MSG_ARRIVED( window, function ): 
    """Event handler when a message arives from the server or the match
       engine""" 
    window.Connect( -1, -1, MSG_ARRIVED, function ) 
 
class MsgArrivedEvent(wxPyCommandEvent): 
    eventType = MSG_ARRIVED 
    def __init__(self, windowID, msg, **kw):
        self.msg = msg
        self.kw = kw
        wxPyCommandEvent.__init__(self, self.eventType, windowID) 
 
    def Clone( self ): 
        self.__class__( self.GetId() )

class PopupWin(wxPopupWindow):
    def __init__(self, parent, text, style=0):
        wxPopupWindow.__init__(self, parent, style)
        self.SetBackgroundColour("CADET BLUE")
        lbl = wxStaticText(self, -1, text, pos=(10, 10))
        sz = lbl.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
        self.Center()
        
def makeBold(widg):
    f = widg.GetFont()
    f.SetWeight(wxBOLD)
    widg.SetFont(f)
    return widg

def drawBorder(rect, dc, flags, borderColor):
    x, y, w, h = (rect.x, rect.y, rect.width, rect.height)
    dc.SetPen(wxPen(borderColor, width=2))
    if flags&NORTH:
        x1, y1, x2, y2 = (x, y, x + w, y)
        dc.DrawLine(x1, y1, x2, y2)
    if flags&EAST:
        x1, y1, x2, y2 = (x + w, y, x + w, y + h)
        dc.DrawLine(x1, y1, x2, y2)             
    if flags&SOUTH:
        x1, y1, x2, y2 = (x, y + h, x + w, y + h)
        dc.DrawLine(x1, y1, x2, y2)
    if flags&WEST:
        x1, y1, x2, y2 = (x, y, x, y + h)
        dc.DrawLine(x1, y1, x2, y2)             

def minuteString(minute):
    suffixMap = {1:"st", 2:"nd", 3:"rd"}
    tmpMinute = minute
    
    if tmpMinute > 99:
        tmpMinute = tmpMinute % 100

    if tmpMinute in [11, 12, 13]:
        return "%dth" % minute

    tmpMinute = tmpMinute % 10
    if tmpMinute in suffixMap:
        return "%d%s" % (minute, suffixMap[tmpMinute])

    return "%dth" % minute

if __name__=='__main__':
    app = wxPySimpleApp()
    frame = JowstFrame("JOWST")
    app.MainLoop()
    

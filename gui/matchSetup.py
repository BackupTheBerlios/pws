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

from wxPython.wx import *
from wxPython.lib.intctrl import *

from lib import Interface
from data.globalConstants import *
from gui.dialogs import SelectDialog
from lib.util import getModules, makeGoodFilename

class MatchControlGUI:
    def __init__(self, parent, network=None):
        self.widgetMap = {}
        self.matchControlWidgets = []
        self.teamLists = [[], []]
        self.parent = parent
        self._currTeamBox = -1
        self.wrestlers = None
        self.stayDisabled = []
        self.addDeleteButtons = []

    def buildMatchControlGUI(self, matchSetupObj):
        self.matchSetupObj = matchSetupObj

        self.matchSetupSzr = wxBoxSizer(wxVERTICAL)
        self.matchSetupSzr.Add((makeBold(wxStaticText(self.parent, -1,
                                                      "Match Setup",
                                                      style=wxALIGN_CENTER),
                                         18)), 0, wxEXPAND)
        self.matchSetupSzr.Add((0, 5))
        self.matchSetupSzr.Add(wxStaticLine(self.parent, -1), 0,
                               wxEXPAND|wxLEFT|wxRIGHT, border=5)
        self.matchSetupSzr.Add((0, 20))
        matchTypeSzr = wxBoxSizer(wxHORIZONTAL)
        matchTypeSzr.Add(makeBold(wxStaticText(self.parent, -1,
                                               "Match Type")), 0,
                         wxEXPAND|wxALIGN_CENTER)

        matchModules = getModules("Matches")
        matchNames = []
        for file in matchModules.keys():
            matchNames.append(matchModules[file].name)
        matchNames.sort()
        matchTypes = ["Regular"] + matchNames

        matchTypeSzr.Add((10, 0))
        
        cID = wxNewId()
        self.matchChoice = wxChoice(self.parent, cID, choices=matchTypes)
        self.matchChoice.SetSelection(0)
        self.matchControlWidgets.append(self.matchChoice)
        
        matchTypeSzr.Add(self.matchChoice, 0, wxEXPAND|wxALIGN_CENTER)
        self.matchSetupSzr.Add(matchTypeSzr, 0, wxEXPAND|wxLEFT|wxRIGHT,
                               border=5)
        self.matchSetupSzr.Add((0, 20))

        timeLimitSzr = wxBoxSizer(wxHORIZONTAL)
        timeLimitSzr.Add(makeBold(wxStaticText(self.parent, -1,
                                               "Time Limit")), 0, wxEXPAND)
        timeLimitSzr.Add((10, 0))
        self.timeLimitEntry = wxIntCtrl(self.parent, value=30, size=(30,20))
        self.matchControlWidgets.append(self.timeLimitEntry)
        timeLimitSzr.Add(self.timeLimitEntry, 0, wxEXPAND)
        timeLimitSzr.Add((15, 0))
        cbID = wxNewId()
        self.noTimeLimitChkbox = wxCheckBox(self.parent, cbID, "No Time Limit")
        self.matchControlWidgets.append(self.noTimeLimitChkbox)
        timeLimitSzr.Add(self.noTimeLimitChkbox, 0, wxEXPAND)

        self.matchSetupSzr.Add(timeLimitSzr, 0,
                               wxEXPAND|wxLEFT|wxRIGHT, border=5)
        self.matchSetupSzr.Add((0, 20))
                
        self._addCheckboxToSetupSizer("DQ Enabled", 1, "dqEnabled")
        self.matchSetupSzr.Add((0, 10))

        self._addCheckboxToSetupSizer("Dramatic Pause", 1, "dramaticPause")
        self._addCheckboxToSetupSizer("Real Time Pin Counts", 1,
                                      "realtimePins")
        self._addCheckboxToSetupSizer("Real Time Count Outs", 1,
                                      "realtimeCountouts")
        self._addCheckboxToSetupSizer("Submission Drama", 1,
                                      "submissionDrama")
        self.matchSetupSzr.Add((0, 10))

        self._addCheckboxToSetupSizer("Strategy Pin Chart", 0, "strategyChart")
        self._addCheckboxToSetupSizer("Pin Only On P/A Roll", 0, "pinOnlyOnPA")
        self.matchSetupSzr.Add((0, 10))
        
        # Team Box
        teamSzr = wxBoxSizer(wxHORIZONTAL)
        teamSzr.Add(self._getTeamSelectionSizer(0), 1,
                    wxEXPAND|wxLEFT|wxRIGHT, border=5)
        teamSzr.Add(makeBold(wxStaticText(self.parent, -1, "VS"), 16), 0 ,
                    wxALIGN_CENTER|wxBOTTOM, border=20)
        teamSzr.Add(self._getTeamSelectionSizer(1), 1,
                    wxEXPAND|wxLEFT|wxRIGHT, border=5)
        self.matchSetupSzr.Add(teamSzr, 0, wxEXPAND)

            
    def enableWidgetEvents(self):
        EVT_CHOICE(self.matchChoice, self.matchChoice.GetId(),
                   self.setMatchType)
        EVT_INT(self.timeLimitEntry, self.timeLimitEntry.GetId(),
                self.setTimeLimit)
        EVT_CHECKBOX(self.noTimeLimitChkbox, self.noTimeLimitChkbox.GetId(),
                     self.setNoTimeLimit)
        EVT_CHECKBOX(self.dqEnabled, self.dqEnabled.GetId(), self.setDqEnabled)
        EVT_CHECKBOX(self.dramaticPause, self.dramaticPause.GetId(),
                     self.setDramaticPause)
        EVT_CHECKBOX(self.realtimePins, self.realtimePins.GetId(),
                     self.setRealtimePins)
        EVT_CHECKBOX(self.realtimeCountouts, self.realtimeCountouts.GetId(),
                     self.setRealtimeCountouts)
        EVT_CHECKBOX(self.submissionDrama, self.submissionDrama.GetId(),
                     self.setSubmissionDrama)
        EVT_CHECKBOX(self.strategyChart, self.strategyChart.GetId(),
                     self.setStrategyChart)
        EVT_CHECKBOX(self.pinOnlyOnPA, self.pinOnlyOnPA.GetId(),
                     self.setPinOnlyOnPA)

    def enableWidgets(self, enabled=1):
        for widget in self.matchControlWidgets:
            widget.Enable(enabled)

    def disableWidgets(self, widgets):
        self.stayDisabled = widgets
        for widget in widgets:
            getattr(self, widget).Disable()
            
    def disableAddDeleteButtons(self):
        for widget in self.addDeleteButtons:
            widget.Disable()

    def setPrefs(self, matchPrefs):
        matchType = matchPrefs.get("MATCH_TYPE")
        if matchType:
            self.matchChoice.SetStringSelection(matchType)
            self.setMatchType()

        if matchPrefs.has_key("TIME_LIMIT"):
            tl = matchPrefs.get("TIME_LIMIT")
            if tl == NO_TIME_LIMIT:
                self.noTimeLimitChkbox.SetValue(1)
                self.setNoTimeLimit()
            else:
                self.timeLimitEntry.SetValue(int(tl))
                self.setTimeLimit()

        for key, attr in (("DQ_ENABLED", "dqEnabled"),
                          ("DRAMATIC_PAUSE", "dramaticPause"),
                          ("REALTIME_PINS", "realtimePins"),
                          ("REALTIME_COUNTOUTS", "realtimeCountouts"),
                          ("SUBMISSION_DRAMA", "submissionDrama"),
                          ("STRATEGY_CHART", "strategyChart"),
                          ("PIN_ONLY_ON_PA", "pinOnlyOnPA")):
                          
            if matchPrefs.has_key(key):
                if matchType and matchType != "Regular" and \
                       key == "DQ_ENABLED":
                    continue
                
                ctrl = getattr(self, attr)
                ctrl.SetValue(matchPrefs.get(key))
                funcname = "set%s%s" % (attr[0].upper(), attr[1:])
                func = getattr(self, funcname)
                func()
                    
            
    def updateControlWidget(self, widget, val):
        if type(val) == type(""):
            getattr(self, widget).SetStringSelection(val)
        else:
            ctrl = getattr(self, widget)
            # Invert val for dramatic pause
            if widget == "timeLimitEntry":
                if val == NO_TIME_LIMIT: # Just update the checkbox
                    self.noTimeLimitChkbox.SetValue(1)
                    return 
                else:
                    self.noTimeLimitChkbox.SetValue(0)
            ctrl.SetValue(val)

    def _addCheckboxToSetupSizer(self, lbl, val, name, add=1):
        setattr(self, name, wxCheckBox(self.parent, -1, lbl))
        ctrl = getattr(self, name)
        ctrl.SetValue(val)
        if add:
            self.matchControlWidgets.append(ctrl)
        self.matchSetupSzr.Add(ctrl, 0, wxEXPAND|wxLEFT|wxRIGHT, border=5)
        self.matchSetupSzr.Add((0, 5))
                   
    def _getTeamSelectionSizer(self, teamNum):
        teamSelSzr = wxBoxSizer(wxVERTICAL)
        teamSelSzr.Add(makeBold(wxStaticText(self.parent,
                                             -1, "Team %s" % str(teamNum+1),
                                             style=wxALIGN_CENTER)),
                       0, wxEXPAND)
        teamSelSzr.Add((0, 5))
        teamList = wxCheckListBox(self.parent, -1, style=wxLB_MULTIPLE)
        teamList.SetToolTip(wxToolTip("Click a wrestler's check box to make that wrestler computer controlled"))
        self.teamLists[teamNum] = teamList
        self.widgetMap[teamList.GetId()] = teamNum
        teamSelSzr.Add(self.teamLists[teamNum], 0, wxEXPAND)
        EVT_CHECKLISTBOX(teamList, teamList.GetId(), self.setCPU)
        teamSelSzr.Add((0, 3))

        buttonSzr = wxBoxSizer(wxHORIZONTAL)
        addButtonID = wxNewId()
        addButton = wxButton(self.parent, addButtonID, "Add...")
        buttonSzr.Add(addButton, 0, wxEXPAND)
        buttonSzr.Add((5, 0))
        self.addDeleteButtons.append(addButton)
        self.widgetMap[addButtonID] = teamNum
        EVT_BUTTON(self.parent, addButtonID, self.addMembers)
        
        delButtonID = wxNewId()
        delButton = wxButton(self.parent, delButtonID, "Delete Selected")
        buttonSzr.Add(delButton, 0, wxEXPAND)
        self.addDeleteButtons.append(delButton)
        self.widgetMap[delButtonID] = teamNum
        EVT_BUTTON(self.parent, delButtonID, self.deleteMembers)

        teamSelSzr.Add(buttonSzr, 0, wxEXPAND)
        teamSelSzr.Add((0, 20))

        return teamSelSzr

    def setTeams(self, team1, team2, is_interactive):
        teamnum = 0
        for team in [team1, team2]:
            self._currTeamBox = teamnum
            members = []
            for wrestlerMod in team:
                members.append(wrestlerMod.path)
            self._addToTeam(prefills=members)

            # Set all wrestlers to CPUs if the tourney is not interactive
            if not is_interactive:
                lb = self.teamLists[teamnum]
                for idx in range(lb.GetCount()):
                    lb.Check(idx)
                    self._doSetCPU(lb.GetString(idx), teamnum, 1)
                                    
            teamnum += 1        

        
    def setNoTimeLimit(self, evt=None):
        if self.noTimeLimitChkbox.IsChecked():
            self.timeLimitEntry.Disable()
            self.matchSetupObj.setTimeLimit(NO_TIME_LIMIT)
        else:
            self.timeLimitEntry.Enable(1)
            self.matchSetupObj.setTimeLimit(self.timeLimitEntry.GetValue())

    def setTimeLimit(self, evt=None):
        self.matchSetupObj.setTimeLimit(self.timeLimitEntry.GetValue())
        
    def setDqEnabled(self, evt=None):
        self.matchSetupObj.setDQ(self.dqEnabled.IsChecked())
        
    def setDramaticPause(self, evt=None):
        self.matchSetupObj.setDramaticPause(self.dramaticPause.IsChecked())
        
    def setRealtimePins(self, evt=None):
        self.matchSetupObj.setRealtimePins(self.realtimePins.IsChecked())

    def setRealtimeCountouts(self, evt=None):
        self.matchSetupObj.setRealtimeCountouts(\
            self.realtimeCountouts.IsChecked() )

    def setSubmissionDrama(self, evt=None):
        self.matchSetupObj.setSubmissionDrama(\
            self.submissionDrama.IsChecked() )
        
    def setStrategyChart(self, evt=None):
        val = self.strategyChart.IsChecked()
        self.pinOnlyOnPA.Enable(not val)
        if val:
            self.pinOnlyOnPA.SetValue(not val)
        self.matchSetupObj.setStrategyChart(val)
        
    def setPinOnlyOnPA(self, evt=None):
        val = self.pinOnlyOnPA.IsChecked()
        self.strategyChart.Enable(not val)
        if val:
            self.strategyChart.SetValue(not val)
        self.matchSetupObj.setPinOnlyOnPA(val)

    def setMatchType(self, evt=None):
        matchname = self.matchChoice.GetStringSelection()
        self.matchSetupObj.setMatchType(matchname)
        if matchname != "Regular":
            matchModules = getModules("Matches")
            for matchModule in matchModules:
               if matchModules[matchModule].name == matchname:
                   matchmod = matchModules[matchModule]
                   break
            if not matchmod.dq:
                self.dqEnabled.Enable(0)
                self.dqEnabled.SetValue(0)
                self.matchSetupObj.setDQ(0)
        else:
            if "dqEnabled" not in self.stayDisabled:
                self.dqEnabled.SetValue(1)
                self.dqEnabled.Enable(1)
                self.matchSetupObj.setDQ(1)
            
            
    def setCPU(self, evt):
        lb = evt.GetEventObject()
        wrestler = lb.GetString(evt.GetSelection())
        teamnum = self.widgetMap[evt.GetId()]
        iscpu = lb.IsChecked(evt.GetSelection())
        self._doSetCPU(wrestler, teamnum, iscpu)

    def _doSetCPU(self, wrestler, teamnum, iscpu):
        if iscpu:
            self.matchSetupObj.addCPU(wrestler, teamnum)
        else:
            self.matchSetupObj.removeCPU(wrestler, teamnum)
        
    def setAllCPU(self, iscpu=1):
        for t in (0, 1):
            self._setTeamCPU(t, iscpu)
        
    def _setTeamCPU(self, teamnum, val):
        lb = self.teamLists[teamnum]
        for idx in range(lb.GetCount()):
            lb.Check(idx, val)
            self._doSetCPU(lb.GetString(idx), teamnum, 1)

    def addMembers(self, evt):
        self._currTeamBox = self.widgetMap[evt.GetId()]
        self.matchSetupObj.getWrestlers(self._selectWrestlers)

    def _selectWrestlers(self, wrestlers):           
        dlg = SelectDialog("Select Wrestlers", wrestlers,
                           "Select Wrestlers from the list below.\n\n"
                           "Hold down the 'CTRL' key to select multiple"
                           " wrestlers or to de-select wrestlers.",
                           parent=self.parent, ac_cb=self._getInstance)
        self._doWrestlerSelectDialog(dlg)

    def _getInstance(self, selection, cb):
        self.matchSetupObj.getWrestlerInstance(selection,
                                               cb)
        
    def _addToTeam(self, dlg=None, prefills=None):
        if dlg: wrestlers = dlg.GetSelected()
        else: wrestlers = prefills
            
        for wrestler in wrestlers:
            self.matchSetupObj.addWrestler(self._currTeamBox, wrestler,
                                           self.addMember)
        self.errs = 0
        if dlg: dlg.Destroy()
        
    def _doWrestlerSelectDialog(self, dlg):
        if dlg.ShowModal() == wxID_OK:
            self._addToTeam(dlg)
        # Cancel button clicked
        else:
            dlg.Destroy()
        
    def addMember(self, member, team):
        if type(member) != type(()):
            self.teamLists[team].Append(member)
        elif member[0] == WRESTLER_ALREADY_ON_TEAM_ERROR:
            dlg = wxMessageDialog(self.parent,
                                  "%s is already on the team." % member[1],
                                  "Team Member Collision", style=wxOK)
            if dlg.ShowModal() == wxID_OK and not self.errs:
                dlg.Destroy()
                self.errs += 1
        elif member[0] == TOO_MANY_WRESTLERS_ERROR:
            mdlg = wxMessageDialog(self.parent, "Too many wrestlers selected.",
                                   "Invalid Selection", style=wxOK)
            if mdlg.ShowModal() == wxID_OK: mdlg.Destroy()
        else: #If we're here...something got f'd up.
            pass
            
                
    def deleteMembers(self, evt=None, teamnum=-1):
        if teamnum < 0:
            teamNum = self.widgetMap[evt.GetId()]
        else:
            teamNum = teamnum
            
        teamList = self.teamLists[teamNum]
        if teamnum < 0:
            selections = teamList.GetSelections()
        else:
            selections = range(teamList.GetCount())

        # Track changes in the length of the list box as items are deleted
        self.listDelta = 0   
        
        for selection in selections:
            wrestler = teamList.GetString(selection - self.listDelta)
            self.matchSetupObj.removeWrestler(teamNum, wrestler,
                                              self.deleteWrestler)

    def deleteWrestler(self, idx, team):
        teamList = self.teamLists[team]
        if idx > -1:
            teamList.Delete(idx)
            self.listDelta += 1

    def getTeams(self, getTeamsCB, dlg=None):
        self.matchSetupObj.getTeams(getTeamsCB, dlg)

    def getCPUs(self, getCPUsCB):
        self.matchSetupObj.getCPUs(getCPUsCB)

    def getMatchType(self, getMatchTypeCB):
        self.matchSetupObj.getMatchType(getMatchTypeCB)

    def getTimeLimit(self, getTimeLimitCB):
        self.matchSetupObj.getTimeLimit(getTimeLimitCB)
    def getDQ(self, getDqCB): self.matchSetupObj.getDQ(getDqCB)

    def getDrama(self, getDramaCB):
        self.matchSetupObj.getDrama(getDramaCB)
        
    def getStrategyChart(self, getStratCB):
        self.matchSetupObj.getStrategyChart(getStratCB)

    def getSetupValues(self, cb=None):
        return self.matchSetupObj.getCurrentSetupValues(cb)
                           
class MatchSetupDialog(wxDialog, wxPanel):
    def __init__(self, setupObj, chatCB=None, panel_parent=None):
        if not panel_parent:
            wxDialog.__init__(self, None, -1, "Match Setup")
        else:
            wxPanel.__init__(self, panel_parent, -1)
            
        self.controlGUI = MatchControlGUI(self)
        self.controlGUI.pwTree = None
        self.setupObj = setupObj
        self.chatCB = chatCB
        self.msParamDict = {}
        self.state = None
        self.mainSzr = wxBoxSizer(wxVERTICAL)
        self.playerMap = {}

        if panel_parent:
            # Layout Match Setup Dialog
            self.mainSzr.Fit(self)
            self.SetSizer(self.mainSzr)
            self.SetAutoLayout(1)
            self.mainSzr.Layout()

    def buildMatchControlGUI(self):
        self.controlGUI.buildMatchControlGUI(self.setupObj)
        self.mainSzr.Add(self.controlGUI.matchSetupSzr, 0, wxEXPAND)

    def enableWidgetEvents(self): self.controlGUI.enableWidgetEvents()
    def enableWidgets(self, enable=1): self.controlGUI.enableWidgets(enable)
    def setTeams(self, team1, team2, is_interactive):
        self.controlGUI.setTeams(team1, team2, is_interactive)

    def setAllCPU(self, val):
        self.controlGUI.setAllCPU(val)

    def setPrefs(self, prefs):
        self.controlGUI.setPrefs(prefs)
        
    def disableWidgets(self, widgets):
        self.controlGUI.disableWidgets(widgets)
        
    def disableAddDeleteButtons(self):
        self.controlGUI.disableAddDeleteButtons()

    def deleteMembers(self, team):
        """Remove All members for a given team from the match setup UI"""
        self.controlGUI.deleteMembers(teamnum=team)
        
    def buildCommPanel(self):
        """This method will add the jowstgui.ChatPanel widget and the player
           wrestler tree to the match setup dialog"""
        commPanelSzr = wxBoxSizer(wxHORIZONTAL)
        # Import here to avoid recursive jowstgui import on startup
        from gui.jowstgui import ChatPanel
        self.chatPanel = ChatPanel(self, self.chatCB)
        commPanelSzr.Add(self.chatPanel, 2, wxEXPAND|wxLEFT, border=5)
        commPanelSzr.Add((2, 0))

        # Build player/wrestler tree
        self.pwTree = wxTreeCtrl(self, -1, size=(200, -1),
                                 style=wxTR_HIDE_ROOT)
        
        self.treeRoot = self.pwTree.AddRoot("Players")
        self.pwTree.SetItemBold(self.treeRoot)
        self.controlGUI.pwTree = self.pwTree
        commPanelSzr.Add(self.pwTree, 1, wxEXPAND|wxRIGHT, border=5)

        self.mainSzr.Add(commPanelSzr, 0, wxEXPAND) #|wxLEFT|wxRIGHT, border=5)
        
    def handleChatMessage(self, playername, msg):
        self.chatPanel.receiveMsg(playername, msg)
        
    # This should be the last call when building a match setup dialog
    def addButtons(self, starttext="Start Match", canceltext="Cancel",
                   disconnect=0):        
        self.disconnect = disconnect
        # Start Match and Cancel Buttons
        okCancelSzr = wxBoxSizer(wxHORIZONTAL)
        okCancelSzr.Add(wxButton(self, wxID_OK, starttext))
        EVT_BUTTON(self, wxID_OK, self.OnOk)
        okCancelSzr.Add((10, 0))
        okCancelSzr.Add(wxButton(self, wxID_CANCEL, canceltext))
        EVT_BUTTON(self, wxID_CANCEL, self.OnCancel)
        self.mainSzr.Add((0, 5))
        self.mainSzr.Add(okCancelSzr, 0, wxALIGN_RIGHT|wxBOTTOM|wxRIGHT,
                         border=5)

        # Layout Match Setup Dialog
        self.mainSzr.Fit(self)
        self.SetSizer(self.mainSzr)
        self.SetAutoLayout(1)
        self.mainSzr.Layout()
        self.Center()

    def addPlayer(self, player, clientplayer):
        self.playerMap[player] = {"BRANCH":
                                  self.pwTree.AppendItem(self.treeRoot,
                                                         player)}
        if player == clientplayer:
            self.pwTree.SetItemBold(self.playerMap[player]["BRANCH"])

    def removePlayer(self, player):
        self.pwTree.Delete(self.playerMap[player]["BRANCH"])
        self.playerMap.pop(player)
                                  
    def addWrestlerToPlayerTree(self, player, wrestler, team):
        self.playerMap[player][wrestler] = {"BRANCH":
                                            self.pwTree.AppendItem(self.playerMap[player]["BRANCH"],
                                                                  "%s (Team %s)" % (wrestler,
                                                                  team + 1))}
        self.pwTree.Expand(self.playerMap[player]["BRANCH"])
        
    def removeWrestlerFromPlayerTree(self, player, wrestler):
        self.pwTree.Delete(self.playerMap[player][wrestler]["BRANCH"])
        self.playerMap[player].pop(wrestler)

    def setPlayerReady(self, player):
        self.pwTree.SetItemTextColour(self.playerMap[player]["BRANCH"], wxRED)
        self.pwTree.SetItemBold(self.playerMap[player]["BRANCH"])
        self.pwTree.SetItemText(self.playerMap[player]["BRANCH"],
                                "%s (Ready)" % player)
        
    def OnOk(self, evt):
        self.setupObj.validateTeams(self._validationDone)

    def OnCancel(self, evt):         
        self.EndModal(wxCANCEL)
        if self.disconnect:
            self.state = DISCONNECT
                    
    def _validationDone(self, ok2go):
        if ok2go:
            self.EndModal(wxID_OK)
            self.state = READY_TO_START_MATCH
        else:
            dlg = wxMessageDialog(self, "Teams are uneven. Re-select teams.",
                                  "Uneven Teams", style=wxOK)
            if dlg.ShowModal() == wxID_OK: dlg.Destroy()
            

    def _setTeamParam(self, teams, data): self.msParamDict["TEAMS"] = teams
    def _setCPUsParam(self, cpus): self.msParamDict["CPUS"] = cpus
    def _setTimeLimitParam(self, timelimit):
        self.msParamDict["TIMELIMIT"] = timelimit
        
    def _setDqParam(self, dq): self.msParamDict["DQ"] = dq
    def _setDramaParam(self, drama):
        self.msParamDict["DRAMATIC_PAUSE"] = drama
        self.msParamDict["STARTUP_CB"](self.msParamDict)
    
    
    def getTeams(self, getTeamsCB): self.controlGUI.getTeams(getTeamsCB)
    def getCPUs(self, getCPUsCB): self.controlGUI.getCPUs(getCPUsCB)
    def getMatchType(self, getMatchTypeCB):
        self.controlGUI.getMatchType(getMatchTypeCB)
        
    def getTimeLimit(self, getTimeLimitCB):
        self.controlGUI.getTimeLimit(getTimeLimitCB)
        
    def getDQ(self, getDqCB): self.controlGUI.getDQ(getDqCB)
    
    def getDrama(self, getDramaCB):
        self.controlGUI.getDrama(getDramaCB)
        
    def getMatchObject(self, getMatchObjCB):
        self.setupObj.getMatchObject(getMatchObjCB)
        
    def getSetupValues(self, cb=None):
        return self.setupObj.getCurrentSetupValues(cb)

    def getMatchStartupParams(self, startupCB, setupUI):
        self.msParamDict["STARTUP_CB"] = startupCB
        self.msParamDict["SETUP_UI"] = setupUI
        self.getTeams(self._setTeamParam)
        self.getCPUs(self._setCPUsParam)
        self.getTimeLimit(self._setTimeLimitParam)
        self.getDQ(self._setDqParam)
        self.getDramaticPause(self._setDramaParam)
                
    
def makeBold(widg, ptsize=None):
    f = widg.GetFont()
    if ptsize: f.SetPointSize(ptsize)
    f.SetWeight(wxBOLD)
    widg.SetFont(f)
    return widg

        
            

from wxPython.wx import *
from lib import util, Interface, prefs, dblib
from data.globalConstants import *
from gui import matchSetup
from wxPython.lib.scrolledpanel import wxScrolledPanel
from wxPython.lib.intctrl import *
from wxPython.html import *
import os

class SelectionGUI(wxPanel):
    def __init__(self, parent, name, wrestlerNames, numTeams,
                 teamSize, startcb, network=0):
        wxPanel.__init__(self, parent, -1)
        self.name = name
        if not name:
            self.name = "Tournament"            
        self.parent = parent
        self.network = network
        self.numTeams = numTeams
        self.teamSize = teamSize
        self.startCB = startcb
        vSzr = wxBoxSizer(wxVERTICAL)

        lbl = wxStaticText(self, -1, "Selection for %s" % self.name)
        f = lbl.GetFont()
        f.SetPointSize(16)
        f.SetWeight(wxBOLD)
        lbl.SetFont(f)
        vSzr.Add(lbl, 0, wxALIGN_CENTER)
        vSzr.Add((0, 20))
        vSzr.Add(wxStaticText(self, -1, "Click a wrestler's checkbox to add"\
                              " the wrestler.  Uncheck a wrestler to remove."),
                 0, wxALIGN_CENTER)
        vSzr.Add((0, 10))
        splitWin = wxSplitterWindow(self, -1)
        splitWin.parent = self
        vSzr.Add(splitWin, 1, wxEXPAND)
        
        # List participants in the tourney
        self.seedList = SeedList(splitWin, numTeams, teamSize)

        # Insert a chat panel if it's a network tournament
        if network:
            from gui.jowstgui import ChatPanel
            self.chatPanel = ChatPanel()

        # Wrestlers available for selection in CheckListBox
        self.wrestlerList = wxCheckListBox(splitWin, -1, choices=wrestlerNames,
                                           size=(300,-1))
        self.wrestlerList.SetFirstItem(0)
        EVT_CHECKLISTBOX(self.wrestlerList, self.wrestlerList.GetId(),
                         self.setWrestler)

        splitWin.SplitVertically(self.seedList, self.wrestlerList, 500)
        
        buttSzr = wxBoxSizer(wxHORIZONTAL)
        startButton = wxButton(self, -1, "Start Tournament")
        EVT_BUTTON(self, startButton.GetId(), self._startTourney)
        buttSzr.Add(startButton, 0)
        buttSzr.Add((10, 0))
        cancelButton = wxButton(self, -1, "Cancel")
        EVT_BUTTON(self, cancelButton.GetId(), self._killWin)
        buttSzr.Add(cancelButton, 0)
        vSzr.Add(buttSzr, 0, wxALIGN_CENTER|wxALL, border=5)

        vSzr.Fit(self)
        self.SetSizer(vSzr)
        self.SetAutoLayout(1)
        self.Layout()
        self.Show(1)
        

    def setWrestler(self, evt):
        lb = self.wrestlerList
        if type(evt) == type(""):
            lb.Check(lb.FindString(evt), 0)
            return

        wrestler = lb.GetString(evt.GetSelection())
        
        if lb.IsChecked(evt.GetSelection()):
            self.seedList.addWrestler(wrestler)
        else: 
            self.seedList.removeWrestler(wrestler)

    def _killWin(self, evt): self.parent.Destroy()
    def _startTourney(self, evt):
        teams = []
        for row in range(self.numTeams):
            teamdata = []
            for col in range(self.teamSize):
                entryval = self.seedList.participantGrid[row][col]
                if not entryval.GetValue():
                    d = wxMessageDialog(self, "Not enough wrestlers selected "\
                                        "for tournament.", "Incomplete Setup",
                                    style=wxOK|wxICON_ERROR)
                    d.ShowModal()
                    d.Destroy()
                    return
                teamdata.append(entryval.GetValue().split(" - "))
            teams.append(teamdata)
        self.parent.Destroy()
        self.startCB(teams, self.name)
        
            
class SeedList(wxScrolledPanel):
    def __init__(self, parent, numTeams, teamSize):
        wxScrolledPanel.__init__(self, parent, -1)
        # Build participant grid
        self.participantGrid = []
        self.parent = parent
        vertSzr = wxBoxSizer(wxVERTICAL)
        from gui.jowstgui import makeBold

        for row in range(numTeams):
            self.participantGrid.append([])
            
            rowSzr = wxBoxSizer(wxHORIZONTAL)
            lbl = makeBold(wxStaticText(self, -1, "#%d" % (row + 1),
                                        size=(30, -1),
                                        style=wxST_NO_AUTORESIZE))
            rowSzr.Add(lbl, 0, wxLEFT, border=5)

            for col in range(teamSize):
                entry = wxTextCtrl(self, -1, size=(200, -1),
                                   style=wxTE_READONLY)
                entry.pos = (row, col)
                EVT_SET_FOCUS(entry, self.setSelection)
                self.participantGrid[-1].append(entry)
                rowSzr.Add(entry, 0, wxRIGHT, border=10)
            vertSzr.Add(rowSzr)

        self.currSelection = None
        self._doSetSelection(self.participantGrid[0][0])

        
        vertSzr.Fit(self)
        self.SetSizer(vertSzr)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        self.Layout()
        self.Show(1)

    def setSelection(self, evt):
        entry = evt.GetEventObject()
        self._doSetSelection(entry)
    
    def addWrestler(self, wrestler, cb=None):
        if not cb: self._addToGUI(wrestler)
        else:
            # pass _addToGUI to network call
            cb(self._addToGUI, wrestler)
            print "network add"

    def _addToGUI(self, wrestler):
        currValue = self.currSelection.GetValue()
        if currValue:
            self.parent.parent.setWrestler(currValue)
            self.currSelection.Refresh()
        self.currSelection.SetValue(wrestler)
        self.currSelection.SetBackgroundColour(wxWHITE)
        self.currSelection.Refresh()
        startrow = self.currSelection.pos[0]
        self._doSetSelection(self.findNextEmptyCell(startrow))

    def removeWrestler(self, wrestler, cb=None):
        if not cb: self._removeFromGUI(wrestler)
        else:
            print "network remove"
            # pass _addToGUI to network call
            cb(self._removeFromGUI, wrestler)

    def _removeFromGUI(self, wrestler):
        for row in self.participantGrid:
            for col in row:
                if col.GetValue() == wrestler:
                    col.SetValue("")
                    self._doSetSelection(col)
                    return 

    def findWrestler(self, wrestler):
        for row in self.participantGrid:
            for col in row:
                if col.GetValue() == wrestler:
                    return 1
        return 0
        
    def findNextEmptyCell(self, startrow=0):
        for row in self.participantGrid[startrow:]:
            for col in row:
                if col.GetValue() == "":
                    return col
        if startrow > 0:
            return self.findNextEmptyCell()
        else: return self.participantGrid[0][0]

    def _doSetSelection(self, entry):
        if self.currSelection:
            self.currSelection.SetBackgroundColour(wxWHITE)
            self.currSelection.Refresh()
        self.currSelection = entry
        entry.SetBackgroundColour(wxNamedColour("YELLOW"))
        entry.Refresh()
        entry.SetFocus()

        
def showTournamentGUI(cb):    
    tourneyDialog = TourneyStartDialog()
    if tourneyDialog.ShowModal() == wxID_OK:
        mods = dblib.getWrestlerData()
        modVals = mods.values()
        modVals.sort(cmpFunc)
        names = []
        for modVal in modVals:
            names.append("%s - %s" % (modVal.name, getattr(modVal, "nameSet",
                                                           "")))
        numTeams = int(tourneyDialog.numTeamsCtrl.GetValue())
        teamSize = int(tourneyDialog.teamSizeCtrl.GetValue())
        tourneyName = tourneyDialog.nameCtrl.GetValue()
        network = 0
        
        frame = wxFrame(None, -1, "Tournament Setup", size=(1024, 768))
        selgui = SelectionGUI(frame, tourneyName, names, numTeams, teamSize,
                              cb, network)
        frame.Center()
        util.setIcon(frame)
        frame.Show(1)

def cmpFunc(v1, v2): return cmp(v1.name, v2.name)
        
class TourneyStartDialog(wxDialog):
    def __init__(self):
        wxDialog.__init__(self, None, -1, "Tournament Size", size=(350, 200))
        sizePanel = wxPanel(self, -1)
        szr = wxBoxSizer(wxVERTICAL)
        szr.Add(wxStaticText(sizePanel, -1,
                             "Enter Tournament Configuration:\n\n"), 0,
                wxALIGN_CENTER)
        numTeamsSzr = wxBoxSizer(wxHORIZONTAL)
        numTeamsSzr.Add(wxStaticText(sizePanel, -1,
                                     "Number of competitors (or teams)"))
        numTeamsSzr.Add((5, 0))
        self.numTeamsCtrl = wxIntCtrl(sizePanel, -1, min=3, size=(40, -1))
        numTeamsSzr.Add(self.numTeamsCtrl)
        szr.Add(numTeamsSzr, 0, wxLEFT|wxRIGHT, border=5)
        szr.Add((0, 5))

        teamSizeSzr = wxBoxSizer(wxHORIZONTAL)
        teamSizeSzr.Add(wxStaticText(sizePanel, -1, "Team Size"))
        teamSizeSzr.Add((5, 0))
        self.teamSizeCtrl = wxIntCtrl(sizePanel, -1, value=1, min=1, max=3,
                                      size=(20, -1))
        teamSizeSzr.Add(self.teamSizeCtrl)
        szr.Add(teamSizeSzr, 0, wxLEFT|wxRIGHT, border=5)
        szr.Add((0, 5))
        
        nameSzr = wxBoxSizer(wxHORIZONTAL)
        nameSzr.Add(wxStaticText(sizePanel, -1, "Tournament Name"))
        nameSzr.Add((5, 0))
        self.nameCtrl = wxTextCtrl(sizePanel, -1, size=(200, -1))
        nameSzr.Add(self.nameCtrl)
        szr.Add(nameSzr, 0, wxLEFT|wxRIGHT, border=5)
        szr.Add((0, 5))

        szr.Add((0, 10))
        buttSzr = wxBoxSizer(wxHORIZONTAL)
        okButt = wxButton(sizePanel, -1, "OK")
        EVT_BUTTON(self, okButt.GetId(), self.validate)
        buttSzr.Add(okButt, 0, wxEXPAND)
        buttSzr.Add((10, 0))
        buttSzr.Add(wxButton(sizePanel, wxID_CANCEL, "Cancel"), 0, wxEXPAND)
        szr.Add(buttSzr, 0, wxALIGN_CENTER|wxLEFT|wxRIGHT, border=5)

        szr.Fit(sizePanel)
        sizePanel.SetSizer(szr)
        sizePanel.SetAutoLayout(1)
        sizePanel.Layout()
        sizePanel.Center()

    def validate(self, evt):
        msg = ""
        if self.teamSizeCtrl.GetValue() > 3:
            msg += "The maximum team size is 3\n\n"
        elif self.teamSizeCtrl.GetValue() < 1:
            msg += "The minimum team size is 1\n\n"

        if self.numTeamsCtrl.GetValue() < 3:
            msg += "The minimum number of teams is 3\n\n"

        if msg:
            errMsg = "The following problems were encountered:\n\n"
            errMsg += msg
            dlg = wxMessageDialog(self, errMsg, "Problems Encountered",
                                  style=wxOK|wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.EndModal(wxID_OK)

class TournamentControlPanel(wxPanel):
    def __init__(self, parent, tourney_data, match_start_cb, close_cb):
        from gui.jowstgui import makeBold
        self.tourney = tourney_data
        self.parent = parent
        self.startCB = match_start_cb
        self.closeCB = close_cb
        self.tourneyFile = None
        self.runningMatch = 0
        
        wxPanel.__init__(self, parent, -1, size=(-1, -1))

        self._buildMenu()
        self.statusBar = wxStatusBar(self.parent, -1)
        self.parent.SetStatusBar(self.statusBar)
        
        szr = wxBoxSizer(wxVERTICAL)
        lbl = wxStaticText(self, -1, self.tourney.getTourneyName())
        lblfont = lbl.GetFont()
        lblfont.SetPointSize(18)
        lbl.SetFont(lblfont)
        szr.Add(makeBold(lbl), 0, wxALIGN_CENTER)
        self.nbWin = wxNotebook(self, -1, style=wxNB_TOP)
        self.nbWin.parent = self
        from gui import brackets
        currRnd = self.tourney.currentRound
        rounds = self.tourney.getTourneyRounds()
        table = self.tourney.getTourneyTable()
        tourneyName = self.tourney.getTourneyName()
        self.bracketPage = brackets.BracketPageBuilder(rounds, table, currRnd,
                                                       tourneyName)
        
        import wx
        import wx.html
        import wx.lib.wxpTag
        self.html = wx.html.HtmlWindow(self.nbWin, -1)
        self.html.SetPage(self.bracketPage.getHTML())

        if not self.tourney.isFinished():
            self.lbMatchSelect = MatchSelectPanel(self.nbWin, self.tourney)
            self.nbWin.AddPage(self.lbMatchSelect, "Matches", 1)
        else:
            self.enableMenuItems((("FileMenu", ["Export Bracket...",
                                                "Print Bracket..."]),))
            self.closeCB()
            
        self.nbWin.AddPage(self.html, "Brackets")
        self.guiBuilding = 1

        szr.Add(self.nbWin, 1, wxEXPAND)

        if not self.tourney.isFinished():
            self.startButton = wxButton(self, -1, "Start Match")
            EVT_BUTTON(self, self.startButton.GetId(), self._startMatch)
            szr.Add(self.startButton, 0, wxALIGN_CENTER)
        
        EVT_NOTEBOOK_PAGE_CHANGED(self.nbWin, self.nbWin.GetId(),
                                  self._onPageChange)
        EVT_CLOSE(self.parent, self.Destroy)
        
        self.SetAutoLayout(True)
        szr.Fit(self)
        self.SetSizer(szr)
        self.Layout()
        self.Fit()
        self.Center()
        self.guiBuilding = 0
    
    def _buildMenu(self):
        from gui.jowstgui import buildMenu
        menuDict = {"&File":(("Save Tournament", True, self._saveTourney),
                             ("Save Tournament As...", True,
                              self._saveTourneyAs),
                             ("Export Bracket...", False,
                              self._exportBracket),
                             ("SEPARATOR", True, None),
                             ("Print Bracket...", False, self._printBracket),
                             ("SEPARATOR", True, None),
                             ("Stop Tournament", True, self.Destroy))
                    }
        buildMenu(self.parent, menuDict, ["&File"])

    def enableMenuItems(self, menuitems):
        self._doEnableMenuItems(menuitems, 1)

    def disableMenuItems(self, menuitems):
        self._doEnableMenuItems(menuitems, 0)

    def _doEnableMenuItems(self, menuitems, enable):
        for menuname, items in menuitems:
            menu = getattr(self.parent, menuname)
            for item in items:
                menu.Enable(menu.FindItem(item), enable)
        
    def _saveTourney(self, evt=None):
        if not self.tourneyFile:
            path = self._showSavePrompt("Save Tournament As...",
                                        "Tournament Files (*.trn)|*.trn")
            if path:
                self.tourneyFile = path
                self._doSave(self.tourneyFile)
        else:
            self._doSave(self.tourneyFile)

    def _saveTourneyAs(self, evt):
        path = self._showSavePrompt("Save Tournament As...",
                                    "Tournament Files (*.trn)|*.trn")
        if path:
            self.tourneyFile = path
            self._doSave(path)

    def _exportBracket(self, evt):
        path = self._showSavePrompt("Export Tournament Bracket...",
                                    "HTML Document (*.htm)|*.htm")
        if path:
            f = open(path, 'w')
            f.write(self.bracketPage.getHTML())
            f.close()
        
    def _showSavePrompt(self, caption, wildcard):
        path = None
        dbDir = os.path.join(util.JOWST_PATH, "db")
        dlg = wxFileDialog(self, caption, dbDir, "",
                           wildcard, style=wxSAVE|wxOVERWRITE_PROMPT)

        if dlg.ShowModal() == wxID_OK:
            path = dlg.GetPath()

        dlg.Destroy()
        return path

    def _doSave(self, path):
        db = dblib.BaseDB(path)
        db.save([["TOURNEY_DATA", self.tourney]])
        self.statusBar.SetStatusText("Saved %s" % path)
                                      
    def _printBracket(self, evt):
        printer = wxHtmlEasyPrinting()
        printer.GetPageSetupData().SetMarginTopLeft((10, 25))
        printer.GetPageSetupData().SetMarginBottomRight((10, 25))
        printer.PrintText(self.bracketPage.getHTML())
        
    def _startMatch(self, evt):
        prefs = self.lbMatchSelect.getSetupValues()
        for key in prefs:
            self.tourney.matchPrefs[key] = prefs[key]
        self.tourney.filename = self.tourneyFile
        self.runningMatch = 1
        self.startCB(self)

    def _onPageChange(self, evt):
        if self.guiBuilding: return
        items = (("FileMenu", ["Export Bracket...", "Print Bracket..."]),)
        if self.nbWin.GetPageText(evt.GetSelection()) != "Matches":
            if hasattr(self, "startButton"):
                self.startButton.Disable()
            self.enableMenuItems(items)
        else:
            self.disableMenuItems(items)
            self.startButton.Enable(1)
        evt.Skip()
            
    def getMatchObject(self, cb): self.lbMatchSelect.getMatchObject(cb)
    def getDrama(self, cb): self.lbMatchSelect.getDrama(cb)
    def Destroy(self, evt=None):
        if not self.runningMatch:
            dlg = wxMessageDialog(self, "Save tournament before stopping?",
                                  "Stopping Tournament",
                                  style=wxYES_NO|wxCANCEL|wxICON_QUESTION)
            retval = dlg.ShowModal()
            if retval in (wxID_YES, wxID_NO):
                if retval == wxID_YES:
                    self._saveTourney()
                self.closeCB()
                self.parent.Destroy()
        else:
            self.parent.Destroy()
           
        
class MatchSelectPanel(wxPanel):
    def __init__(self, parent, tourney):
        self.tourney = tourney
        roundstr = self.tourney.getRoundString()
        matchstrings = self.tourney.getMatchStrings()
        from gui.jowstgui import makeBold
        self.parent = parent
        wxPanel.__init__(self, parent, -1, size=(-1, -1))
        hSzr = wxBoxSizer(wxHORIZONTAL)
        szr = wxBoxSizer(wxVERTICAL)
        if roundstr in ["Quarterfinals", "Semifinals", "Finals"]:
            roundstr = "the %s" % roundstr
            
        szr.Add(makeBold(wxStaticText(self, -1,
                                      "Matches remaining in %s" % roundstr)),
                0,
                wxALIGN_CENTER)
        szr.Add((0, 10))
        szr.Add(wxStaticText(self, -1, "Select match:"), 0, wxALIGN_CENTER)

        self.matchSelect = wxListBox(self, -1, choices=matchstrings,
                                     style=wxLB_SINGLE)
        EVT_LISTBOX(self, self.matchSelect.GetId(), self._onSelection)
        szr.Add(self.matchSelect, 0, wxALIGN_CENTER)

        self.cpuControlled = wxCheckBox(self, -1,
                                        "Wrestlers are CPU controlled")
        EVT_CHECKBOX(self, self.cpuControlled.GetId(), self._setInteractive)
            
        szr.Add(self.cpuControlled, 1, wxALL, border=20)
        hSzr.Add(szr, 0, wxALL, border=20)

        setupObj = Interface.MatchSetup()
        suSzr = wxBoxSizer(wxVERTICAL)
        self.matchSetup = matchSetup.MatchSetupDialog(setupObj,
                                                      panel_parent=self)
        
        self.matchSetup.buildMatchControlGUI()
        self.matchSetup.disableAddDeleteButtons()
        self._setSelectedTeams()
        self.matchSetup.enableWidgetEvents()
        self.matchSetup.enableWidgets()

        # Tourney match preferences will be set after the first match
        if self.tourney.hasPrefs():
            self.matchSetup.setPrefs(self.tourney.matchPrefs)
        else:
            self.tourney.setPrefs(prefs.MatchPrefs())
            
        if not self.tourney.isInteractive():
            self.cpuControlled.SetValue(1)
            self._setInteractive()

        if self.tourney.isSemiFinalOrFinal():
            self.tourney.matchPrefs["DQ_ENABLED"] = 0
            self.tourney.matchPrefs["TIME_LIMIT"] = NO_TIME_LIMIT
            self.matchSetup.setPrefs(self.tourney.matchPrefs)
            self.matchSetup.disableWidgets(["dqEnabled", "timeLimitEntry",
                                            "noTimeLimitChkbox"])
            
        
        suSzr.Add(self.matchSetup, 1, wxEXPAND)
        hSzr.Add(suSzr, 5, wxEXPAND)                
        
        hSzr.Fit(self)
        self.SetSizer(hSzr)
        self.SetAutoLayout(1)
        self.Layout()
        self.Fit()

    def getMatchIndex(self): return self.matchSelect.GetSelection()

    def _onSelection(self, evt):
        # Remove Wrestlers from each team when a new match selection is made
        self.matchSetup.deleteMembers(0)
        self.matchSetup.deleteMembers(1)
        self._setSelectedTeams()

    def _setSelectedTeams(self):
        if self.tourney.isFinished(): return
        t1, t2 = self.tourney.getTeamsForMatch(self.matchSelect.GetSelection())
        self.matchSetup.setTeams(t1, t2, self.tourney.isInteractive())
        self.tourney.setCurrentMatch(self.matchSelect.GetSelection())

    def _setInteractive(self, evt=None):
        val = self.cpuControlled.IsChecked()
        self.tourney.setInteractive(not val)
        self.matchSetup.setAllCPU(val)
        
    def getMatchObject(self, cb): self.matchSetup.getMatchObject(cb)
    def getDrama(self, cb): self.matchSetup.getDrama(cb)

    def getSetupValues(self):
        valDict = self.matchSetup.getSetupValues()
        popThese = ("TEAMS", "CPUS")
        for key in popThese:
            valDict.pop(key)
            
        drama = valDict["DRAMA"]
        dramaTup = (("DRAMATIC_PAUSE", "getDramaPause"),
                    ("REALTIME_PINS", "getRealtimePins"),
                    ("REALTIME_COUNTOUTS", "getRealtimeCountouts"),
                    ("SUBMISSION_DRAMA", "getSubmissionDrama"))

        valDict.pop("DRAMA")
        for dkey, funcname in dramaTup:
            func = getattr(drama, funcname)
            valDict[dkey] = func()
                
        return valDict
            
        

def showTournamentControlPanel(tourney_manager, match_start_cb,
                               close_cb, filename=None):
    frame = wxFrame(None, -1, "Tournament Control Panel", size=(1024, 768))
    controlPanel = TournamentControlPanel(frame, tourney_manager,
                                          match_start_cb, close_cb)
    frame.Fit()
    controlPanel.tourneyFile = filename
    frame.Center()
    util.setIcon(frame)
    frame.Show(1)

from wxPython.wx import *
from wxPython.lib.maskedctrl import wxMaskedCtrl
from lib import dblib, util
from gui.dialogs import SelectDialog
import time, os

class ResultControlPanel(wxFrame):
    def __init__(self, path, name):
        wxFrame.__init__(self, None, -1, "Results Manager - %s" % name,
                         size=(800, 600))
        try:
            self.db = dblib.ResultManager(path, name)
        except OSError:
            mDlg = wxMessageDialog(self,
                                   "There was a problem creating the " +\
                                   "%s database." % name,
                                   "Problem Creating Database",
                                   style=wxOK|wxICON_ERROR)
            mDlg.ShowModal()
            mDlg.Destroy()
            self.Destroy()            

        self.nbWin = wxNotebook(self, -1)

        self.buildMenu()        
        self.name = name
        self.Center(wxBOTH)
        util.setIcon(self)
        self.Show(1)

    def saveResultChart(self, evt):
        wildcard = "HTML Document (*.htm)|*.htm"
        dbDir = os.path.join(util.JOWST_PATH, "db")
        dlg = wxFileDialog(self, "Save file as...", dbDir, "", wildcard,
                           wxSAVE|wxOVERWRITE_PROMPT)
        if dlg.ShowModal() == wxID_OK:
            path = dlg.GetPath()
            pageNum = self.nbWin.GetSelection()
            html = self.nbWin.GetPage(pageNum).pageText
            outfile = open(path, 'w')
            outfile.write(html)
            outfile.close()
        dlg.Destroy()
            
    def printResultChart(self, evt):
        pageNum = self.nbWin.GetSelection()
        html = self.nbWin.GetPage(pageNum)
        html.printer.GetPageSetupData().SetMarginTopLeft((10, 25))
        html.printer.GetPageSetupData().SetMarginBottomRight((10, 25))
        #html.printer.PreviewText(html.pageText)
        html.printer.PrintText(html.pageText)

    def viewSinglesResults(self, evt): self._viewResults(1)
    def viewTagResults(self, evt): self._viewResults(2)
    def viewSixManResults(self, evt): self._viewResults(3)

    def _viewResults(self, size):
        wrestlers, dlgChoices = self.db.getWrestlerDictAndList(size)
        if not len(dlgChoices):
            msg = wxMessageDialog(self, "No win/loss records available",
                                  "No records to view",
                                  style=wxOK|wxICON_EXCLAMATION)
            msg.ShowModal()
            msg.Destroy()
            return
            
        dlg = SelectDialog("View Win/Loss Record", dlgChoices,
                           "Select win/loss record(s) to view\n\n"
                           "Hold down the 'CTRL' key to select multiple"
                           " wrestlers or to de-select wrestlers.",
                           post_lb_cb=self._getCheckBox, parent=self)
        if dlg.ShowModal() == wxID_OK:
            pages = []
            for selection in dlg.GetSelected():
                name = self.db.getRecord(selection)["NAME"]
                pages.append((self._formatWinLossRecord(selection), name))
            if self.multiTabChkBox.IsChecked():
                for page, name in pages[:-1]:
                    self.nbWin.AddPage(self._getHTMLWin(page), name)
                page, name = pages[-1]
                self.nbWin.AddPage(self._getHTMLWin(page), name, select=1)
            else:
                pageStr = ""
                for page, name in pages:
                    pageStr += "%s<BR><HR><BR>" % page
                currPage = self.nbWin.GetSelection()
                if currPage > -1:
                    self.nbWin.DeletePage(currPage)
                self.nbWin.AddPage(self._getHTMLWin(pageStr), "Results",
                                   select=1)                
            self.enableMenuItems(self.FileMenu,
                                 ("Close Tab", "Close All Tabs",
                                  "Export...",
                                  "Print..."))

        dlg.Destroy()

    def _formatWinLossRecord(self, key):
        name = self.db.getRecord(key)["NAME"]
        wins = self.db.getNumWins(key)
        losses = self.db.getNumLosses(key)
        title = "Win/Loss Record for %s (%s)" % (name, self.name)
        htmlStr = "<HTML><TITLE>%s</TITLE><BODY>\n<CENTER>" % title +\
                  "<H3>%s</H3></CENTER>\n" % title
        htmlStr += "\n<B>Wins: </B>%d\n" % wins
        htmlStr += "<BR>\n<B>Losses: </B>%d\n" % losses
        htmlStr += "<BR>\n<B>Draws: </B>%d\n" % self.db.getNumDraws(key)
        if wins + losses < 1:
            winPerc = 0.0
        else:
            winPerc = 100.0 * (float(wins) / float(wins + losses))
        htmlStr += "<BR>\n<B>Winning Percentage: </B>%.1f%%\n" % winPerc

        htmlStr += "<BR><BR><TABLE WIDTH=100% BORDER=5 CELLPADDING=3><THEAD>"
        htmlStr += "<TR>\n"
        for col in ("DATE", "EVENT", "LOCATION", "OPPONENT",
                    "RESULT", "MATCH TYPE", "MATCH TIME"):
            htmlStr += "<TH><B>%s</B></TH>\n" % col
        htmlStr += "</TR></THEAD><TBODY>\n"

        for row in self.db.getResults(key, ["DATE", "EVENT", "LOCATION",
                                            "OPPONENT", "RESULT",
                                            "MATCH_TYPE", "MATCH_TIME"]):
            htmlStr += "<TR>"
            for item in row:
                htmlStr += "<TD><CENTER>%s</CENTER></TD>" % item
            htmlStr += "</TR>\n"

        htmlStr += "</TBODY></TABLE></BODY></HTML>"

        return htmlStr
    

    def viewSinglesRankings(self, evt): self._viewRankings(1)
    def viewTagRankings(self, evt): self._viewRankings(2)
    def viewSixManRankings(self, evt): self._viewRankings(3)

    def _viewRankings(self, size):
        keys = self.db.getKeys()
        rows = []
        for key in keys:
            team = key.split(';')
            if len(team) == size:
                name = self.db.getRecord(key)["NAME"]
                wins = self.db.getNumWins(key)
                losses = self.db.getNumLosses(key)
                draws = self.db.getNumDraws(key)
                if wins + losses < 1:
                    winPerc = 0.0
                else:
                    winPerc = float(wins) / float(wins + losses)
                winperc = "%.3f" % (winPerc)
                rows.append((winperc, name, wins, losses, draws))
        page = self._formatRankings(rows, size)
        title = "%s Rankings" % self._getRankingString(size)
        self.nbWin.AddPage(self._getHTMLWin(page), title, select=1)
        self.enableMenuItems(self.FileMenu,
                             ("Close Tab", "Close All Tabs",
                              "Export...",
                              "Print..."))

    def _formatRankings(self, data, size):
        ranking = self._getRankingString(size)
        data.sort(self._sortDescending)
        title = "%s Rankings (%s)" % (ranking, self.name)
        htmlStr = "<HTML><TITLE>%s</TITLE><BODY>\n<CENTER>" % title +\
          "<H3>%s</H3></CENTER>\n" % title
        htmlStr += "<BR><BR><TABLE WIDTH=100% BORDER=0 CELLPADDING=0><THEAD>"
        htmlStr += "<TR>\n"
        for col in ("", "NAME", "WINS", "LOSSES", "DRAWS",
                    "WINNING PERCENTAGE"):
            htmlStr += "<TH><B>%s</B></TH>\n" % col
        htmlStr += "</TR></THEAD><TBODY>\n"

        rank = 1
        width = self._getWidth(size)
        for row in data:
            rankStr  = "<TD ALIGN=RIGHT WIDTH=15>%d.</TD>" % rank
            htmlStr += "<TR>%s<TD %s>%s</TD>" % (rankStr, width,
                                                          row[1])
            for item in (row[2], row[3], row[4], row[0]):
                htmlStr += "<TD><CENTER>%s</CENTER></TD>" % item
            htmlStr += "</TR>\n"
            rank += 1

        htmlStr += "</TBODY></TABLE></BODY></HTML>"

        return htmlStr

    def _getRankingString(self, size):
        if size == 1:
            ranking = "Singles"
        elif size == 2:
            ranking = "Tag Team"
        else:
            ranking = "Six Man"

        return ranking

    def _getWidth(self, size):
        return ["", "WIDTH=40%%", "WIDTH=55%%"][size-1]
        
    def _sortDescending(self, v1, v2):
        return cmp(v2, v1)
        
    def _getHTMLWin(self, pageStr):
        import wx
        import wx.html
        import wx.lib.wxpTag
        import wxPython.html

        html = wx.html.HtmlWindow(self.nbWin, -1)
        html.SetPage(pageStr)
        html.pageText = pageStr
        html.printer = wxPython.html.wxHtmlEasyPrinting("", self)

        return html
        
    def _getCheckBox(self, parent):        
        self.multiTabChkBox = wxCheckBox(parent, -1,
                                         "Open selections in multiple tabs.")

        return self.multiTabChkBox
        
    def closeWin(self, evt): self.Destroy()

    def closeCurrentTab(self, evt):
        if self.nbWin.GetSelection() > -1:
            self.nbWin.DeletePage(self.nbWin.GetSelection())

        if self.nbWin.GetSelection() == -1:
            self.disableMenuItems(self.FileMenu,
                                  ("Close Tab", "Close All Tabs",
                                   "Export...",
                                   "Print..."))

    def closeAllTabs(self, evt):
        if self.nbWin.GetSelection() > -1:
            self.nbWin.DeleteAllPages()
        self.disableMenuItems(self.FileMenu,
                              ("Close Tab", "Close All Tabs",
                               "Export...", "Print..."))

    def enableMenuItems(self, menu, items):
        self._doMenuItemEnable(menu, items, 1)
        
    def disableMenuItems(self, menu, items):
        self._doMenuItemEnable(menu, items, 0)
        
    def _doMenuItemEnable(self, menu, items, enable):
        for item in items:
            menu.Enable(menu.FindItem(item), enable)
            
    def buildMenu(self):
        menuDict = {"&File":(("Export...", False,
                              self.saveResultChart),
                             ("Print...", False,
                              self.printResultChart),
                             ("Close Tab", False,
                              self.closeCurrentTab),
                             ("Close All Tabs", False,
                              self.closeAllTabs),
                             ("SEPARATOR", True, None),
                             ("Exit", True, self.closeWin)),
                    "&View":(("View Singles Win/Loss Records", True,
                              self.viewSinglesResults),
                             ("View Tag Team Win/Loss Records", True,
                              self.viewTagResults),
                             ("View Six Man Win/Loss Records", True,
                              self.viewSixManResults),
                             ("SEPARATOR", None, None),
                             ("View Singles Rankings", True,
                              self.viewSinglesRankings),
                             ("View Tag Team Rankings", True,
                              self.viewTagRankings),
                             ("View Six Man Rankings", True,
                              self.viewSixManRankings)
                             )
                   }

        menuBar = wxMenuBar()
        for menuName in ("&File", "&View"):
            name = menuName.replace('&', '') + "Menu"
            setattr(self, name, wxMenu())
            for itemStr, enabled, cb in menuDict[menuName]:
                itemId = wxNewId()                
                if itemStr == "SEPARATOR":
                    getattr(self, name).AppendSeparator()
                else:
                    getattr(self, name).Append(itemId, itemStr)
                    getattr(self, name).Enable(itemId, enabled)
                if cb:
                    EVT_MENU(self, itemId, cb)
            menuBar.Append(getattr(self, name), menuName)
        self.SetMenuBar(menuBar)

class ResultDBSelector(wxDialog):
    def __init__(self, parent, caption):
        wxDialog.__init__(self, parent, -1, caption)
        from db import dataRegistry
        self.resultDBs = dataRegistry.resultsRegistry

        self.szr = wxBoxSizer(wxVERTICAL)

    def addTextEntry(self, label, name, default="", entrysize=80):
        hszr = wxBoxSizer(wxHORIZONTAL)
        hszr.Add(wxStaticText(self, -1, label), 0)
        setattr(self, name, wxTextCtrl(self, -1, default, size=(entrysize,
                                                                -1)))
        hszr.Add((5, 0))
        entry = getattr(self, name)
        hszr.Add(entry, 0)
        self.szr.Add(hszr, 0, wxALL, border=5)

    def addDateEntry(self, label, name):
        hszr = wxBoxSizer(wxHORIZONTAL)
        hszr.Add(wxStaticText(self, -1, label), 0)
        setattr(self, name, wxMaskedCtrl(self, -1, time.strftime("%m/%d/%Y"),
                                         autoformat="USDATEMMDDYYYY/"))
        hszr.Add((5, 0))
        entry = getattr(self, name)
        hszr.Add(entry, 0)
        self.szr.Add(hszr, 0, wxALL, border=5)

    def addLabel(self, labelstr, name=None, bold=0, center=0):
        lbl = wxStaticText(self, -1, labelstr)
        if bold:
            from gui.jowstgui import makeBold
            lbl = makeBold(lbl)
        if name:
            setattr(self, name, lbl)
        if center:
            center = wxALIGN_CENTER

        self.szr.Add(lbl, 0, wxALL|center, border=5)

    def addDbSelector(self, deleting=0):
        if not len(self.resultDBs):
            if not deleting:
                lbchoices = ["Create a new results database"]
            else:
                lbchoices = []
        else:
            lbchoices = self.resultDBs.keys()
            lbchoices.sort()
            if not deleting:
                lbchoices.append("Create a new results database")
            
        self.szr.Add((0, 10))
        self.lb = wxListBox(self, -1, choices=lbchoices)
        self.szr.Add(self.lb, 0, wxALIGN_CENTER|wxALL|wxEXPAND, border=5)

    def addSpacer(self, size):
        self.szr.Add((0, size))
        
    def addLine(self):
        self.szr.Add(wxStaticLine(self, -1), 0, wxALL|wxEXPAND, border=5)
        
    def getResultDb(self):
        name = self.lb.GetStringSelection()
        path = self.resultDBs.get(name, None)
        if not path:
            name = getNewResultDbName(self)
            if not name:
                return None
        return dblib.getDb(path, name)

    def getNameAndPath(self):
        name = self.lb.GetStringSelection()
        path = self.resultDBs.get(name, None)
        return name, path
    
    def ShowModal(self):
        hszr = wxBoxSizer(wxHORIZONTAL)
        hszr.Add(wxButton(self, wxID_OK, "OK"), 0, wxALIGN_CENTER)
        hszr.Add((10, 0))
        hszr.Add(wxButton(self, wxID_CANCEL, "Cancel"), 0, wxALIGN_CENTER)
        self.szr.Add(hszr, 0, wxALIGN_CENTER|wxALL, border=5)
        self.szr.Fit(self)
        self.SetSizer(self.szr)
        self.SetAutoLayout(1)
        self.szr.Layout()
        self.Centre()
        return wxDialog.ShowModal(self)

def getNewResultDbName(parent):
    name = None
    choiceMade = None
    dlg = None
    while not choiceMade:
        dlg = wxTextEntryDialog(parent,
                                "Enter the name of the new results database:",
                                "New Results Database")
        if dlg.ShowModal() == wxID_OK:
            name = dlg.GetValue()
            from db import dataRegistry
            if dataRegistry.resultsRegistry.get(name, None):
                mDlg = wxMessageDialog(parent,
                                       "A results database already exists " +\
                                       "with this name.",
                                       "Database Exists", style=wxOK)
                mDlg.ShowModal()
                mDlg.Destroy()
            else:
                choiceMade = 1
        else:
            mDlg = wxMessageDialog(parent,
                                   "Are you sure you do not want to create" +\
                                   " a results database?",
                                   "Confirm database creation", style=wxYES_NO)
            if mDlg.ShowModal() == wxID_YES:
                choiceMade = 1
            mDlg.Destroy()
            
    dlg.Destroy()
    return name
                                         
if __name__ == '__main__':
    app = wxPySimpleApp()
    import os
    ResultControlPanel(os.path.join("data", "result1.db"), "Test")
##    d = ResultDBSelector(None, "Test Selector")
##    d.addDateEntry("Date Entry", "matchDate")
##    d.ShowModal()
##    d.Destroy()
    app.MainLoop()

    

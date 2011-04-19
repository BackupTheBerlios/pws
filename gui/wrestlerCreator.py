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
import os
from wxPython.wx import *
from wxPython.lib.scrolledpanel import wxScrolledPanel
import wx

from gui.dialogs import SelectDialog
from data.formattedStrings import formattedStrings
from lib import wrestlerBuilder, dblib
from lib.util import JOWST_PATH, convertToString, setIcon, getWrestlerModule

class WrestlerCreator(wxScrolledPanel):
    def __init__(self, parent):
        wxScrolledPanel.__init__(self, parent, -1)
        self.parent = parent
        self.notebookWin = CreatorNotebook(self)
        self.notebookWin.SetSelection(0)
        EVT_CLOSE(self.parent, self._onClose)
        titleSzr = wxBoxSizer(wxHORIZONTAL)

        self.isDirtyLbl = boldLabel("", self, wxALIGN_LEFT)
        titleSzr.Add(self.isDirtyLbl, 1, wxLEFT, border=5)
        
        self.nameLbl = boldLabel("", self, wxALIGN_RIGHT)
        titleSzr.Add(self.nameLbl, 1, wxRIGHT, border=5)
        
        mainSzr = wxBoxSizer(wxVERTICAL)
        mainSzr.Add((0, 5))
        mainSzr.Add(titleSzr, 0, wxEXPAND)
        mainSzr.Add(self.notebookWin, 1, wxEXPAND|wxLEFT|wxRIGHT, border=5)
        self.addButtons(mainSzr)
        
        mainSzr.Fit(self)
        self.SetSizer(mainSzr)
        
        self.SetupScrolling()
        self.SetAutoLayout(1)
        self.Layout()

    def addButtons(self, szr):
        buttSzr = wxBoxSizer(wxHORIZONTAL)

        self.loadButt = wxButton(self, -1, "Load")
        EVT_BUTTON(self.loadButt, self.loadButt.GetId(), self.loadWrestler)
        buttSzr.Add(self.loadButt, 0, wxALIGN_CENTER)
        buttSzr.Add((10, 0))
        
        self.saveAsButt = wxButton(self, -1, "Save As...")
        EVT_BUTTON(self.saveAsButt, self.saveAsButt.GetId(), self.saveWrestler)
        buttSzr.Add(self.saveAsButt, 0, wxALIGN_CENTER)
        buttSzr.Add((10, 0))

        self.saveButt = wxButton(self, -1, "Save")
        EVT_BUTTON(self.saveButt, self.saveButt.GetId(), self.saveWrestler)
        buttSzr.Add(self.saveButt, 0, wxALIGN_CENTER)
        buttSzr.Add((10, 0))

        self.clearButt = wxButton(self, -1, "Clear")
        EVT_BUTTON(self.clearButt, self.clearButt.GetId(), self.clearFields)
        buttSzr.Add(self.clearButt, 0, wxALIGN_CENTER)
        buttSzr.Add((10, 0))

        szr.Add((0, 5))
        szr.Add(buttSzr, 0, wxALIGN_CENTER)
        szr.Add((0, 5))

    def updateName(self, evt):
        obj = evt.GetEventObject()
        self.nameLbl.SetLabel(obj.GetValue())
        self.setDirty()
        self.Layout()

    def setDirty(self, isdirty=1):
        if isdirty:
            self.notebookWin.dirty = True
            self.isDirtyLbl.SetLabel("*")            
        else:
            self.isDirtyLbl.SetLabel("")
            
    def saveWrestler(self, evt):
        try:
            self.notebookWin.saveWrestler(evt.GetId() == self.saveAsButt.GetId())
        except:
            dlg = wxMessageDialog(self,
                                  formattedStrings["WRESTLER_SAVE_ERROR"] %
                                  (self.notebookWin.step,
                                   self.notebookWin.nameCtrl.GetValue()),
                                  "Problem saving wrestler", wxOK|wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
                                  

    def _onClose(self, evt):
        if self.notebookWin.isDirty():
            dlg = wxMessageDialog(self,
                                  formattedStrings["BUILDER_CLOSE_MSG"],
                                  style=wxYES_NO|wxNO_DEFAULT|\
                                  wxICON_EXCLAMATION)
            if dlg.ShowModal() == wxID_NO:
                dlg.Destroy()
                return
            dlg.Destroy()
        self.parent.Destroy()
            
    def loadWrestler(self, evt):
        if self.notebookWin.isDirty():
            dlg = wxMessageDialog(self,
                                  formattedStrings["BUILDER_IS_DIRTY_MSG"],
                                  style=wxYES_NO|wxNO_DEFAULT|\
                                  wxICON_EXCLAMATION)
            if dlg.ShowModal() == wxID_NO:
                dlg.Destroy()
                return
            dlg.Destroy()
        wrestlerDic = dblib.getWrestlerData()
        wrestlers = []
        for filename in wrestlerDic.keys():
            wrestler = wrestlerDic[filename]
            nameSet = getattr(wrestler, "nameSet", "")
            
            wrestlers.append((wrestler.name, nameSet, filename))
            
        dlg = SelectDialog("Select Wrestler", wrestlers,
                           "Select Wrestler To Load", single_select=1,
                           parent=self)
        
        if dlg.ShowModal() == wxID_OK:
            wrestler = wrestlerDic[dlg.GetSelection()]
            self.notebookWin.loadWrestler(wrestler)
            self.setDirty(0)
        dlg.Destroy()

    def clearFields(self, evt):
        dlg = wxMessageDialog(self,
                              formattedStrings["CLEAR_BUILDER_MSG"],
                              style=wxYES_NO|wxNO_DEFAULT|\
                              wxICON_EXCLAMATION)
        if dlg.ShowModal() == wxID_NO:
            dlg.Destroy()
            return
        dlg.Destroy()
        self.notebookWin.clearFields()
        self.notebookWin.dirty = False

class CreatorNotebook(wxNotebook):
    def __init__(self, parent):
        self.parentWin = parent
        wxNotebook.__init__(self, parent, -1)
        self.dirty = False
        self.specialtyCardLbl = None
        self.loadedFileName = None
        self.addBasicInfoTab()
        self.addGeneralCard()
        self.addDefensiveCard()
        self.addOffensiveCard()
        self.addRopesCard()
        self.addSpecialtyCard()


    def addBasicInfoTab(self):
        self.biPanel = wxScrolledPanel(self, -1)
        szr = wxBoxSizer(wxVERTICAL)
        self.addSectionHeaderToSizer(self.biPanel, szr,
                                     "BASIC WRESTLER INFORMATION")
        szr.Add((0, 5))

        # Name label and entry widget
        nameSzr = wxBoxSizer(wxHORIZONTAL)
        namelbl = wxStaticText(self.biPanel, -1, "Wrestler Name")
        namelbl.SetForegroundColour("FOREST GREEN")
        font = namelbl.GetFont()
        font.SetWeight(wxBOLD)
        namelbl.SetFont(font)
        nameSzr.Add(namelbl, 0, wxALIGN_RIGHT|wxST_NO_AUTORESIZE)
        nameSzr.Add((5, 0))
        self.nameCtrl = wxTextCtrl(self.biPanel, -1, "", size=(300, -1))
        EVT_TEXT(self.nameCtrl, self.nameCtrl.GetId(),
                 self.parentWin.updateName)
        nameSzr.Add(self.nameCtrl, 0, wxALIGN_LEFT)
        self.addToPageSizer(nameSzr, szr)
        szr.Add((0, 20))

        # Submission Range label and entry widgets
        self.subRow = TwoValueRow(self.biPanel, "SUBMISSION RANGE:",
                                  self.validateRange, size=(150, -1),
                                  evt_macro=EVT_KILL_FOCUS)
        subRangeDesc = formattedStrings["SUBMISSION_RANGE_DESCRIPTION"]
        self.addTwoValueRowToSizer(self.biPanel, self.subRow.szr, szr,
                                   subRangeDesc)

        # Tag Team Range label and entry widgets
        self.tagTeamRow = TwoValueRow(self.biPanel, "TAG TEAM RANGE:",
                                  self.validateRange, size=(150, -1),
                                      evt_macro=EVT_KILL_FOCUS)
        tagRangeDesc = formattedStrings["TAG_TEAM_RANGE_DESCRIPTION"]
        self.addTwoValueRowToSizer(self.biPanel, self.tagTeamRow.szr, szr,
                                   tagRangeDesc)

        # Priority label and entry widgets
        self.priorityRow = TwoValueRow(self.biPanel, "PRIORITY:",
                                       self.validatePriority,
                                       v1Str="Singles", v2Str="Tag Team",
                                       size=(150, -1))
        
        priDesc = formattedStrings["PRIORITIES_DESCRIPTION"]
        self.addTwoValueRowToSizer(self.biPanel, self.priorityRow.szr, szr,
                                   priDesc)

        # Name of the set this wrestler belongs to
        szr.Add(wxStaticLine(self.biPanel, -1), 0, wxEXPAND)
        szr.Add((0, 5))
        self.addToPageSizer(self.getLblAndTextCtrl("Set Name",
                                                   "nameSetCtrl",
                                                   lambda e: self.parentWin.setDirty()),
                                                   szr)

        self.addPanelToPage(self.biPanel, szr, "Basic Info")
        
        
    def getLblAndTextCtrl(self, lbltext, ctrlname, cb):
        szr = wxBoxSizer(wxHORIZONTAL)
        lbl = wxStaticText(self.biPanel, -1, lbltext)
        lbl.SetForegroundColour("FOREST GREEN")
        font = lbl.GetFont()
        font.SetWeight(wxBOLD)
        lbl.SetFont(font)
        szr.Add(lbl, 0, wxALIGN_RIGHT|wxST_NO_AUTORESIZE)
        szr.Add((5, 0))
        setattr(self, ctrlname,
                wxTextCtrl(self.biPanel, -1, "", size=(300, -1)))
        ctl = getattr(self, ctrlname)
        szr.Add(ctl, 0, wxALIGN_LEFT)
        EVT_TEXT(ctl, ctl.GetId(), cb)

        return szr
        
    def addTwoValueRowToSizer(self, win, tvrow, szr, desc):
        self.addToPageSizer(wxStaticLine(win, -1), szr)
        szr.Add((0, 5))
        self.addToPageSizer(tvrow, szr)
        szr.Add((0, 10))
        lbl = getFixedWidthLabel(win, desc)
        self.addToPageSizer(lbl, szr, wxLEFT, 10)
        szr.Add((0, 20))
        
    def addGeneralCard(self):
        args = [["OC", "OC/TT", "DC"], self.validateGenCard]
        self.addCard("generalCard", TwoColSizer, args, "General Card",
                     "GENERAL_CARD_PAGE_DESCRIPTION", )

    def addDefensiveCard(self):
        args = [["A", "B", "C", "REVERSE"], self.validateDefCard] 
        self.addCard("defensiveCard", TwoColSizer, args, "Defensive Card",
                     "DEFENSIVE_CARD_PAGE_DESCRIPTION")

    def addOffensiveCard(self):
        args = [11, ["", "P/A", "(S)", "*", "(XX)", "(DQ)", "ROPES"], 2,
                self.validateOffensiveCard]
        self.addCard("offensiveCard", MoveList, args, "Offensive Card",
                     "OFFENSIVE_CARD_PAGE_DESCRIPTION")
        
    def addRopesCard(self):
        args = [11, ["", "P/A", "(S)", "*", "(XX)", "(DQ)", "NA"], 2,
                self.validateRopesCard]
        self.addCard("ropesCard", MoveList, args, "=Ropes=",
                     "ROPES_CARD_PAGE_DESCRIPTION")
        

    def addSpecialtyCard(self):
        args = [6, ["", "P/A", "*", "(DQ)"], 1, self.validateSpecCard, 0]
        self.addCard("specialtyCard", MoveList, args, "Specialty Card",
                     "SPECIALTY_CARD_PAGE_DESCRIPTION")

    def addCard(self, attr, ctrl, ctrlArgs, pageStr, descKey):
        panel = wxScrolledPanel(self, -1)
        panel.setSpecialtyLbl = self.updateSpecialtyLabel
        szr = wxBoxSizer(wxVERTICAL)
        self.addSectionHeaderToSizer(panel, szr, pageStr.upper())

        # For the Specialty Card add a label to szr that will take
        #  the name of the specialty move
        if attr == "specialtyCard":
            self.specialtyCardLbl = boldLabel("", panel)
            self.specialtyCardLbl.theParent = panel
            szr.Add((0, 10))
            self.addToPageSizer(self.specialtyCardLbl, szr)
            szr.Add((0, 10))
            
        args = [panel] + ctrlArgs
        setattr(self, attr, ctrl(*args))
        getattr(self, attr).tag = pageStr 
        winSzr = getattr(self, attr).szr        
        self.addToPageSizer(winSzr, szr)
        szr.Add((0, 20))
        self.addToPageSizer(wxStaticLine(panel, -1), szr)
        szr.Add((0, 10))
        pageDesc = formattedStrings[descKey]
        descLbl = getFixedWidthLabel(panel, pageDesc)
        self.addToPageSizer(descLbl, szr, wxALIGN_CENTER)
        self.addPanelToPage(panel, szr, pageStr)

    def addPanelToPage(self, win, winSzr, pageName):
        self.AddPage(win, pageName)
        winSzr.Fit(win)
        win.SetSizer(winSzr)
        win.SetAutoLayout(1)
        win.Layout()
        win.SetupScrolling()
        
    def addSectionHeaderToSizer(self, win, szr, text, lines=1):
        if lines:
            szr.Add(wxStaticLine(win, -1), 0, wxEXPAND)
        lbl = boldLabel(text, win)
        lbl.SetForegroundColour("FOREST GREEN")
        szr.Add(lbl, 0, wxALIGN_CENTER|wxALL, border=5)
        if lines:
            szr.Add(wxStaticLine(win, -1), 0, wxEXPAND)
        
    def addToPageSizer(self, ctrl, szr, flags=wxEXPAND, border=0):
        szr.Add(ctrl, 0, flags, border=border)

    ########## VALIDATION FUNCTIONS ##########
    def validateGenCard(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()
        octtCount = 0
        for ctrl in self.generalCard.getChoiceControls():
            if ctrl.GetStringSelection() == "OC/TT":
                octtCount += 1
        if octtCount > 1:           
            evt.GetEventObject().SetStringSelection("OC")
            self._showMessageDialog("OC/TT", "General Card")

    def validateDefCard(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()
        
    def validateOffensiveCard(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()

        obj = evt.GetEventObject()
        for move in self.offensiveCard.moveItems:
            ctrl = move["MOVE_TYPE_CTRL"]
            moveType = ctrl.GetStringSelection()
            if ctrl.GetId() == obj.GetId():
                moveNameCtrl = move["MOVE_NAME_CTRL"]
                moveNameCtrl.Enable(1)
                movePointCtrl = move["MOVE_POINT_CTRL"]
                movePointCtrl.Enable(1)
                selMoveType = moveType

        if selMoveType == "ROPES":
            moveNameCtrl.SetValue("ROPES")
            moveNameCtrl.Enable(0)
            movePointCtrl.Clear()
            movePointCtrl.Enable(0)
        elif selMoveType == "(DQ)":
            movePointCtrl.Clear()
            movePointCtrl.Enable(0)            
        elif selMoveType == "(S)":
            specMove = self.specialtyCardLbl.GetLabel()
            movePointCtrl.Clear()
            movePointCtrl.Enable(0)
            if specMove:
                moveNameCtrl.SetValue(specMove)
            else:
                self.updateSpecialtyLabel(moveNameCtrl.GetValue())
        elif not self.checkForSpecMove():
            self.updateSpecialtyLabel("")

    def validateRopesCard(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()
        obj = evt.GetEventObject()
        specCount = 0
        
        for move in self.ropesCard.moveItems:
            ctrl = move["MOVE_TYPE_CTRL"]
            moveType = ctrl.GetStringSelection()
            if ctrl.GetId() == obj.GetId():
                moveNameCtrl = move["MOVE_NAME_CTRL"]
                moveNameCtrl.Enable(1)
                movePointCtrl = move["MOVE_POINT_CTRL"]
                movePointCtrl.Enable(1)
                selMoveType = moveType

        if selMoveType == "(S)":
            specMove = self.specialtyCardLbl.GetLabel()
            movePointCtrl.Clear()
            movePointCtrl.Enable(0)
            if specMove:
                moveNameCtrl.SetValue(specMove)
            else:
                self.updateSpecialtyLabel(moveNameCtrl.GetValue())
        elif selMoveType == "NA":
            moveNameCtrl.SetValue(selMoveType)
            moveNameCtrl.Enable(0)
            movePointCtrl.SetValue('0')
            movePointCtrl.Enable(0)
        elif selMoveType == "(DQ)":
            movePointCtrl.Clear()
            movePointCtrl.Enable(0)
        elif not self.checkForSpecMove():
            self.updateSpecialtyLabel("")

    def validateSpecCard(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()

        obj = evt.GetEventObject()
        for move in self.specialtyCard.moveItems:
            ctrl = move["MOVE_TYPE_CTRL"]
            moveType = ctrl.GetStringSelection()
            if ctrl.GetId() == obj.GetId():
                movePointCtrl = move["MOVE_POINT_CTRL"]
                movePointCtrl.Enable(1)
                selMoveType = moveType

        if selMoveType == "(DQ)":
            movePointCtrl.Clear()
            movePointCtrl.Enable(0)            

        
    def validateRange(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()        
        obj = evt.GetEventObject()
        val = obj.GetValue()
        if val:
            val = int(val)
            if val < 2:
                obj.SetValue("2")
                self._showInvalidValueDialog("The minimum value for this field is 2")
                obj.SetFocus()
            elif val > 12:
                obj.SetValue("12")
                self._showInvalidValueDialog("The maximum value for this field is 12")
                obj.SetFocus()

    def validatePriority(self, evt):
        self.dirty = 1
        self.parentWin.setDirty()
        obj = evt.GetEventObject()
        val = obj.GetValue()
        if val:
            try:
                val = float(val)
            except: pass

        if val < 1:
            obj.SetValue("1")
            self._showInvalidValueDialog("The minimum value for this field is 1")
            
    def isDirty(self):
        if self.dirty: return 1
        for move in self.offensiveCard.moveItems + self.ropesCard.moveItems +\
                self.specialtyCard.moveItems:
            if move["MOVE_NAME_CTRL"]:
                if move["MOVE_NAME_CTRL"].GetValue() or \
                       move["MOVE_POINT_CTRL"].GetValue():
                    return 1
        return False
        
    def checkForSpecMove(self):
        for move in self.offensiveCard.moveItems:
            if move["MOVE_TYPE_CTRL"].GetStringSelection() == "(S)" and \
               move["MOVE_NAME_CTRL"].GetValue():
                return True

        for move in self.ropesCard.moveItems:
            if move["MOVE_TYPE_CTRL"].GetStringSelection() == "(S)" and \
               move["MOVE_NAME_CTRL"].GetValue():
                return True
        return False

    def setSpecialtyLbl(self, evt):
        obj = evt.GetEventObject()
        self.updateSpecialtyLabel(obj.GetValue())
        
    def updateSpecialtyLabel(self, lblstr):
        self.specialtyCardLbl.SetLabel(lblstr)
        self.specialtyCardLbl.theParent.Layout()
        
    def _showMessageDialog(self, msg, card):
        dlg = wxMessageDialog(self,
                              "%s can only be selected once on the" % msg +\
                              " %s" % card,
                              "Invalid Selection", wxOK|wxICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    def _showInvalidValueDialog(self, msg):
        dlg = wxMessageDialog(self, msg, "Invalid Value", wxOK|wxICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    def saveWrestler(self, saveas=1):
        if not self.isDirty(): return
        self.step = "Building"
        wb = wrestlerBuilder.WrestlerBuilder()
        wb.setName(self.nameCtrl.GetValue())
        self.step = "General Card"
        self.addCardToBuilder(self.generalCard, wb.addToGeneralCard)
        self.step = "Offensive Card"
        self.addCardToBuilder(self.offensiveCard, wb.addToOffensiveCard)
        self.step = "Defensive Card"
        self.addCardToBuilder(self.defensiveCard, wb.addToDefensiveCard)
        self.step = "Specialty Card"
        wb.setSpecialty(self.specialtyCardLbl.GetLabel())
        self.addCardToBuilder(self.specialtyCard, wb.addToSpecialtyCard)
        self.step = "Ropes Card"
        self.addCardToBuilder(self.ropesCard, wb.addToRopesCard)

        self.step = "Submission Values"
        vals = self.subRow.getValues()
        wb.setSubMin(vals[0])
        if int(vals[0]) >= int(vals[1]): vals[1] = vals[0]
        wb.setSubMax(vals[1])

        self.step = "Tag Team Values"
        vals = self.tagTeamRow.getValues()
        wb.setTagTeamMin(vals[0])
        if int(vals[0]) >= int(vals[1]): vals[1] = vals[0]
        wb.setTagTeamMax(vals[1])

        self.step = "Priority Values"
        vals = self.priorityRow.getValues()
        wb.setPriSingles(vals[0])
        wb.setPriTagTeam(vals[1])

        self.step = "Name"
        wb.setNameSet(self.nameSetCtrl.GetValue())
        
        self.step = "Save process"
        
        wrestlerPath = os.path.normpath(os.path.join(JOWST_PATH, "Wrestlers"))
        dosave = 1
        if (not self.loadedFileName) or saveas:
            dlg = wxFileDialog(self, "Save wrestler as...", wrestlerPath,
                               wildcard="Python source (*.py)|*.py|",
                               style=wxSAVE|wxOVERWRITE_PROMPT)
            dlg.SetFilterIndex(0)
            if dlg.ShowModal() == wxID_OK:
                self.loadedFileName = dlg.GetPath()
            else: dosave = 0
            dlg.Destroy()
        if dosave:
            wb.writeToFile(self.loadedFileName)
            self.setStatusText("Wrote " + self.loadedFileName)
            self.parentWin.setDirty(0)
            compiledFile = os.path.splitext(self.loadedFileName)[0] + ".pyc"
            if os.path.exists(compiledFile):
                os.unlink(compiledFile)
                     
    def addCardToBuilder(self, ctrl, builderfunc):
        for itemvals in ctrl.getItemList():
            builderfunc(*itemvals)

    def loadWrestler(self, wrestler):
        self.clearFields()
        # Ensure we're working with a *.py
        self.loadedFileName = wrestler.path
        
        wrestler = getWrestlerModule(wrestler.path)
        self.setStatusText("Loaded " + self.loadedFileName)
        self.nameCtrl.SetValue(wrestler.name)
        self.populateTwoValueRow("sub", wrestler)
        self.populateTwoValueRow("tagTeam", wrestler)
        self.populateTwoValueRow("priority", wrestler)        
        self.setCardValues("generalCard", wrestler)
        self.setCardValues("defensiveCard", wrestler)
        self.setCardValues("offensiveCard", wrestler)
        self.setCardValues("ropesCard", wrestler)
        self.setCardValues("specialtyCard", wrestler)
        if hasattr(wrestler, "nameSet"):
            self.nameSetCtrl.SetValue(wrestler.nameSet)
        
    def setCardValues(self, cardName, wrestler):
        twoColCards = ("generalCard", "defensiveCard")
        if cardName in twoColCards:
            self.populateTwoColSizer(cardName, wrestler)
        elif cardName == "specialtyCard":
            self.updateSpecialtyLabel(wrestler.Specialty.keys()[0])
            self.populateMoveList(cardName, wrestler)
        else:
            self.populateMoveList(cardName, wrestler)

    def populateTwoColSizer(self, cardName, wrestler):
        """Populate a TwoColSizer using a wrestler module as the source"""
        choiceCtrls = getattr(self, cardName).choiceControls
        itemList = getattr(wrestler, cardName[0].upper() + cardName[1:])
        idx = 0
        for item in itemList:
            choiceCtrls[idx].SetStringSelection(convertToString(item))
            idx += 1
            
    def populateMoveList(self, cardName, wrestler):
        """Populate a MoveList using a wrestler module as the source"""
        moveItems = getattr(self, cardName).moveItems
        if cardName not in ("specialtyCard", "ropesCard"):          
            itemList = getattr(wrestler, cardName[0].upper() + cardName[1:])
        elif cardName == "specialtyCard":
            specDict = getattr(wrestler,
                               (cardName[0].upper() + cardName[1:])[:-4])
            itemList = specDict.values()[0]
        else:
            cardName = cardName[:-4]
            itemList = getattr(wrestler, cardName[0].upper() + cardName[1:])
            
        idx = 0
        for item in itemList:
            if item.has_key("MOVE_NAME"):
                moveItems[idx]["MOVE_NAME_CTRL"].SetValue(item["MOVE_NAME"])

            if item.has_key("MOVE_POINTS"):
                points = str(item["MOVE_POINTS"])
                moveItems[idx]["MOVE_POINT_CTRL"].SetValue(points)

            moveType = convertToString(item["MOVE_TYPE"])
            if moveType:  # Process (S), (XX), (DQ), P/A, *
                if moveType != "(S)" or \
                       (moveType == "(S)" and cardName != "specialtyCard"):
                    ctrl = moveItems[idx]["MOVE_TYPE_CTRL"]
                    ctrl.SetStringSelection(moveType)
                    if moveType in ("(DQ)", "(S)"):
                        # No points ahould be entered for DQ and (S)
                        moveItems[idx]["MOVE_POINT_CTRL"].Enable(0)
            elif item["MOVE_NAME"] == "ROPES":
                moveItems[idx]["MOVE_TYPE_CTRL"].SetStringSelection("ROPES")
                moveItems[idx]["MOVE_NAME_CTRL"].Enable(0)
                moveItems[idx]["MOVE_POINT_CTRL"].Enable(0)
            elif item["MOVE_NAME"] == "NA":
                moveItems[idx]["MOVE_TYPE_CTRL"].SetStringSelection("NA")
                moveItems[idx]["MOVE_NAME_CTRL"].Enable(0)
                moveItems[idx]["MOVE_POINT_CTRL"].Enable(0)
                
            idx += 1
            
    def populateTwoValueRow(self, cardRow, wrestler):
        """Populate a TwoValueRow using a wrestler module as the source"""
        values = getattr(self, cardRow + "Row").values
        wrestlerRow = getattr(wrestler, cardRow[0].upper() + cardRow[1:])
        values[0].SetValue(str(wrestlerRow[0]))
        if len(wrestlerRow) > 1:
            values[1].SetValue(str(wrestlerRow[1]))

    def clearFields(self):
        self.loadedFileName = None
        self.nameCtrl.Clear()
        self.clearTwoValueRow("sub")
        self.clearTwoValueRow("tagTeam")
        self.clearTwoValueRow("priority")
        self.nameSetCtrl.Clear()
        self.clearCardValues("generalCard")
        self.clearCardValues("defensiveCard")
        self.clearCardValues("offensiveCard")
        self.clearCardValues("ropesCard")
        self.clearCardValues("specialtyCard")
        self.parentWin.setDirty(0)

    def clearTwoValueRow(self, name):
        vals = getattr(self, name+"Row").values
        for val in vals:
            val.Clear()

    def clearCardValues(self, cardname):
        if cardname not in ("generalCard", "defensiveCard"):
            self.clearMoveList(cardname)
        else:
            self.clearTwoColSizer(cardname)
            
    def clearTwoColSizer(self, cardname):
        choiceCtrls = getattr(self, cardname).choiceControls
        for ctrl in choiceCtrls:
            ctrl.SetSelection(0)
            
    def clearMoveList(self, cardname):
        moveItems = getattr(self, cardname).moveItems
        for item in moveItems:
            # init move name ctrl
            if item["MOVE_NAME_CTRL"]:
                item["MOVE_NAME_CTRL"].Clear()
                item["MOVE_NAME_CTRL"].Enable(1)
            # init move point ctrl
            item["MOVE_POINT_CTRL"].Clear()
            item["MOVE_POINT_CTRL"].Enable(1)
            # clear move type selection
            item["MOVE_TYPE_CTRL"].SetSelection(0)

    def setStatusText(self, strText):
        self.parentWin.parent.statusBar.SetStatusText(strText, 0)
            
class TwoColSizer:
    def __init__(self, parent, choices, choiceCB=None):
        self.parent = parent
        self.choices = choices
        self.choiceCB = choiceCB
        self.choiceControls = [None] * 11
        self.szr = wxBoxSizer(wxVERTICAL)
        self.tblszr = wxBoxSizer(wxHORIZONTAL)
        self.leftColSzr = wxBoxSizer(wxVERTICAL)
        self.rightColSzr = wxBoxSizer(wxVERTICAL)
        
        for row in range(5):
            self.leftColSzr.Add(self.getSizerElem(row), 1,
                                wxTOP|wxBOTTOM|wxALIGN_CENTER, 
                                border=3)
            self.rightColSzr.Add(self.getSizerElem(row+5), 1,
                                wxTOP|wxBOTTOM|wxALIGN_CENTER, border=3)

        self.tblszr.Add(self.leftColSzr, 1, wxEXPAND)
        self.tblszr.Add(self.rightColSzr, 1, wxEXPAND)        
        self.szr.Add(self.tblszr, 1, wxEXPAND)

        lastRowSzr = wxBoxSizer(wxHORIZONTAL)
        lastRowSzr.Add((0,0),1, wxEXPAND)
        lastRow = LabelChoice(self.parent, "12", self.choices, self.choiceCB)
        lastRowSzr.Add(lastRow.szr, 1)
        lastRowSzr.Add((0,0),1, wxEXPAND)
        self.szr.Add(lastRowSzr, 0, wxALL|wxALIGN_CENTER, border=3)
        self.choiceControls[10] = lastRow.choiceCtrl

    def getSizerElem(self, rowNum):
        szrElem = wxBoxSizer(wxHORIZONTAL)
        lblChoice = LabelChoice(self.parent, str(rowNum + 2),
                                self.choices, self.choiceCB)
        self.choiceControls[rowNum] = lblChoice.choiceCtrl
        return lblChoice.szr

    def getChoiceControls(self): return self.choiceControls

    def getItemList(self):
        idx = 0
        retlist = []
        for ctrl in self.choiceControls:
            retlist.append((idx, ctrl.GetStringSelection()))
            idx += 1

        return retlist
        
       
class LabelChoice:
    def __init__(self, parent, lblStr, choicelist, choiceCB=None):
        self.lblStr = lblStr
        self.choices = choicelist
        self.choiceCB = choiceCB
        self.szr = wxBoxSizer(wxHORIZONTAL)
        lbl = boldLabel(lblStr, parent, wxALIGN_RIGHT, (20, -1))
        lbl.SetForegroundColour("FOREST GREEN")
        self.szr.Add(lbl, 0, wxEXPAND)
        self.szr.Add((10, 0))
        self.choiceCtrl = wxChoice(parent, -1, choices=choicelist)
        if self.choiceCB:
            EVT_CHOICE(self.choiceCtrl, self.choiceCtrl.GetId(), choiceCB)
        self.szr.Add(self.choiceCtrl, 1, wxEXPAND)
        
class MoveList:
    def __init__(self, parent, size, choices=[], lblMod=0, choiceCB=None,
                 shownames=1):
        self.parent = parent
        self.size = size
        self.choices = choices
        self.lblMod = lblMod
        self.choiceCB = choiceCB
        self.moveItems = []
        self.szr = wxBoxSizer(wxVERTICAL)

        for row in range(size):
            lblStr = str(row + lblMod)
            moveRow = MoveRow(parent, self.choices, lblStr, self.choiceCB,
                              shownames, lblMod)
            self.moveItems.append(moveRow.moveItems)
            self.szr.Add(moveRow.szr, 1,
                         wxALIGN_CENTER|wxTOP|wxBOTTOM, border=3)

    def getItemList(self):
        idx = 0
        retlist = []
        for item in self.moveItems:
            moveName = None
            movePoints = item["MOVE_POINT_CTRL"].GetValue()
            moveType = item["MOVE_TYPE_CTRL"].GetStringSelection()
            if item["MOVE_NAME_CTRL"]:
                moveName = item["MOVE_NAME_CTRL"].GetValue()
                retlist.append((idx, moveName, movePoints, moveType))
            else:
                retlist.append((idx, movePoints, moveType))
            idx += 1

        return retlist
    
class MoveRow:
    def __init__(self, parent, choicelist, lblStr, choiceCB, shownames=1,
                 lblMod=0):
        self.parent = parent
        self.szr = wxBoxSizer(wxHORIZONTAL)
        self.szr.Add(boldLabel(lblStr, parent,
                               wxALIGN_RIGHT|wxST_NO_AUTORESIZE,
                               lblsize=(20, -1)), 0, wxEXPAND)

        self.szr.Add((10, 0))
        moveNameCtrl = None
        if shownames:
            moveNameCtrl = wxTextCtrl(parent, -1, "", size=(200,-1))
            EVT_TEXT(moveNameCtrl, moveNameCtrl.GetId(),
                     self.setSpecialtyLbl)
            nameTip = wxToolTip("Enter Move Name")
            moveNameCtrl.SetToolTip(nameTip)
            self.szr.Add(moveNameCtrl, 0, wxEXPAND)
            self.szr.Add((10, 0))
        movePointCtrl = wxTextCtrl(parent, -1, "", size=(20, 13))            
        pointTip = wxToolTip("Enter number of points for the move")
        movePointCtrl.SetToolTip(pointTip)
        self.szr.Add(movePointCtrl, 0, wxEXPAND)
        self.szr.Add((10, 0))
        moveTypeCtrl = wxChoice(parent, -1, choices=choicelist)
        typeTip = wxToolTip("Move type selection")
        moveTypeCtrl.SetToolTip(typeTip)
        self.szr.Add(moveTypeCtrl, 0, wxEXPAND)

        if choiceCB:
            EVT_CHOICE(moveTypeCtrl, moveTypeCtrl.GetId(), choiceCB)

        self.moveItems = {"MOVE_POINT_CTRL":movePointCtrl,
                          "MOVE_TYPE_CTRL":moveTypeCtrl,
                          "MOVE_NAME_CTRL":moveNameCtrl}

    def setSpecialtyLbl(self, evt):
        if self.moveItems["MOVE_TYPE_CTRL"].GetStringSelection() == "(S)":
            self.parent.setSpecialtyLbl(\
                self.moveItems["MOVE_NAME_CTRL"].GetValue())

            
class TwoValueRow:
    def __init__(self, parent, lblStr, entryCB=None, v1Str="Min", v2Str="Max",
                 size=(70, -1), color="FOREST GREEN", evt_macro=EVT_TEXT):
        self.szr = wxBoxSizer(wxHORIZONTAL)
        self.lblStr = lblStr
        lbl = boldLabel(lblStr, parent, wxST_NO_AUTORESIZE, lblsize=size)
        lbl.SetForegroundColour(color)
        self.szr.Add(lbl, 0)
        self.szr.Add((10, 0))
        val1 = wxTextCtrl(parent, -1, "", size=(25, -1))
        val2 = wxTextCtrl(parent, -1, "", size=(25, -1))
        val1.tag = lblStr
        val2.tag = lblStr
        self.values = [val1, val2]
        if entryCB:
            try:
                evt_macro(parent, self.values[0].GetId(), entryCB)
                evt_macro(parent, self.values[1].GetId(), entryCB)
            except:
                evt_macro(self.values[0], entryCB)
                evt_macro(self.values[1], entryCB)
                

        lbl1 = wxStaticText(parent, -1, v1Str)
        lbl1.SetForegroundColour("BLUE")
        self.szr.Add(lbl1, 0, wxALIGN_LEFT)
        self.szr.Add((5, 0))
        self.szr.Add(self.values[0], 0, wxALIGN_LEFT)
        self.szr.Add((10, 0))
        lbl2 = wxStaticText(parent, -1, v2Str)
        lbl2.SetForegroundColour("BLUE")
        self.szr.Add(lbl2, 0, wxALIGN_LEFT)
        self.szr.Add((5, 0))
        self.szr.Add(self.values[1], 0, wxALIGN_LEFT)

    def getValues(self):
        val1 = self.values[0].GetValue()
        val2 = self.values[1].GetValue()
        if not val1:
            if self.lblStr == "TAG TEAM RANGE:": val1=2; val2=2
            elif self.lblStr == "SUBMISSION RANGE:": val1=2; val2=12
            else: val1=1; val2=1

        if not val2: val2 = val1
        return [self._convertPlus(val1), self._convertPlus(val2)]        

    def _convertPlus(self, val):
        try:
            float(val)
        except:
            if val[-1] == '+' and val.find('.5') == -1:
                val = self._convertPlus(val[:-1] + '.5')
                float(val)
            else: raise ValueError

        return val

def boldLabel(text, parent, alignment=wxALIGN_CENTER, lblsize=(-1,-1),
              ptsize=None):
    lbl = wxStaticText(parent, -1, text, style=alignment, size=lblsize)
    font = lbl.GetFont()
    if ptsize: font.SetPointSize(ptsize)
    font.SetWeight(wxBOLD)
    lbl.SetFont(font)
    return lbl

def getFixedWidthLabel(parent, text, flags=0):
    lbl = wxStaticText(parent, -1, text, style=flags)
    #f = wx.Font(10, wxMODERN, wxNORMAL, wxNORMAL)
    #lbl.SetFont(f)
    lbl.SetFont(wx.SystemSettings.GetFont(wxSYS_OEM_FIXED_FONT))
    return lbl

def italicizeLabel(lbl):
    f = lbl.GetFont()
    f.SetStyle(wxITALIC)
    lbl.SetFont(f)
    return lbl

def startBuilder(parent):
    """Call this when starting the Wrestler Builder from another GUI window"""
    frame = wxFrame(parent, -1, "Wrestler Builder")
    frame.win = WrestlerCreator(frame)
    frame.statusBar = wxStatusBar(frame, -1)
    frame.SetStatusBar(frame.statusBar)
    setIcon(frame)
    frame.Show(1)
    
if __name__ == '__main__':
    app = wxPySimpleApp()
    frame = wxFrame(None, -1, "Wrestler Builder")
    frame.win = WrestlerCreator(frame)
    setIcon(frame)
    frame.Show(1)
    app.MainLoop()

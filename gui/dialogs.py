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

import sys
from wxPython.wx import *
from wxPython.lib.mixins.listctrl import wxColumnSorterMixin, wxListCtrlAutoWidthMixin
from wxPython.lib.scrolledpanel import wxScrolledPanel
import pwsconfig

class YesOrNoDialog(wxDialog):
    def __init__(self, parent, caption, size=(420,-1)):
        wxDialog.__init__(self, parent, -1, caption)
        self.size = size
        self.htmlTable = "<TABLE WIDTH=100% BORDER=5 CELLPADDING=3><THEAD>\n"
        self.htmlString = '<HTML><BODY>'
        self.headersSet = 0
        self.caption = caption
        
    def addLine(self, line='<BR>\n'):
        self.htmlString += line

    def addHeading(self, line, size=1):
        self.htmlString += "<H%d>%s</H%d>" % (size, line, size)

    def setTableHeaders(self, headers):
        if self.headersSet: return
        self.headersSet = 1
        self.htmlTable += "<TR>"
        for header in headers:
            self.htmlTable += "<TH><B>%s</B></TH>\n" % header
        self.htmlTable += "</TR></THEAD><TBODY>\n"

    def addTableRow(self, rowitems):
        self.htmlTable += "<TR>"
        for item in rowitems:
            self.htmlTable += "<TD><CENTER>%s</CENTER></TD>" % item
        self.htmlTable += "</TR>"

    def insertTable(self):
        self.htmlString += self.htmlTable + "</TBODY></TABLE>"
        
    def ShowModal(self):
        import wx
        import wx.html
        import wx.lib.wxpTag

        html = wx.html.HtmlWindow(self, -1, size=self.size)
        # Add Yes/No buttons
        self.htmlString += \
                        """<center>
                        <wxp module="wx" class="Button" width="15%">
                        <param name="label" value="Yes">
                        <param name="id" value="ID_YES">
                        </wxp>
                        <wxp module="wx" class="Button" width="15%">
                        <param name="label" value="No">
                        <param name="id" value="ID_NO">
                        </wxp>
                        </center></BODY></HTML>
                        """
        html.SetPage(self.htmlString)
        yesbtn = html.FindWindowById(wx.ID_YES)
        EVT_BUTTON(self, yesbtn.GetId(), self._onYes)
        nobtn = html.FindWindowById(wx.ID_NO)
        EVT_BUTTON(self, nobtn.GetId(), self._onNo)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)
        return wxDialog.ShowModal(self)

    def _onYes(self, evt): self.EndModal(wxID_YES)
    def _onNo(self, evt): self.EndModal(wxID_NO)
        
class ScrolledDialog(wxDialog):
    def __init__(self, parent, msg, caption, label=""):
        wxDialog.__init__(self, parent, -1, caption)
        szr = wxBoxSizer(wxVERTICAL)        
        if label:
            from gui.jowstgui import makeBold
            szr.Add(makeBold(wxStaticText(self, -1, label)), 0,
                    wxALIGN_CENTER|wxTOP|wxLEFT|wxRIGHT, border=10)
        szr.Add(wxTextCtrl(self, -1, msg,
                           style=wxTE_MULTILINE|wxTE_READONLY,
                           size=(320, 240)),
                1, wxALL|wxEXPAND, border=10)

        hszr = wxBoxSizer(wxHORIZONTAL)
        hszr.Add(wxButton(self, wxID_OK, "OK"))
        hszr.Add((10, 0))
        hszr.Add(wxButton(self, wxID_CANCEL, "Cancel"))
        szr.Add(hszr, 0, wxALIGN_CENTER|wxALL, border=5)
        
        szr.Fit(self)
        self.SetSizer(szr)
        self.SetAutoLayout(1)
        self.Layout()
        self.Center()

        
class MessageDialog(wxDialog):
    def __init__(self, parent, msg, caption, image=None, cb=None,
                 size=(350, 200)):
        wxDialog.__init__(self, parent, -1, caption, size=size)
        wxBell()
        MessagePanel(self, msg, image=image, cb=cb)

class MessagePanel(wxPanel):
    def __init__(self, parent, msg, image=None, cb=None):
        wxPanel.__init__(self, parent, -1)
        self.parent = parent
        vszr = wxBoxSizer(wxVERTICAL)
        infoszr = wxBoxSizer(wxHORIZONTAL)
        if image:
            infoszr.Add(self.getImage(image))
            infoszr.Add((30, 0))
        infoszr.Add(wxStaticText(self, -1, msg), 0, wxTOP|wxLEFT|wxRIGHT,
                    border=5)
        vszr.Add(infoszr, 1, wxEXPAND)
        vszr.Add((0, 20))
        butt = wxButton(self, -1, "OK")
        if not cb: cb = self.defaultCB
        EVT_BUTTON(self, butt.GetId(), cb)
        vszr.Add(butt, 0, wxALIGN_CENTER)
        vszr.Fit(self)
        self.SetSizer(vszr)
        self.SetAutoLayout(1)
        self.Layout()
        self.Center()
        self.Show(1)

    def defaultCB(self, evt):
        self.parent.Destroy()
        
    def getImage(self, imgpath):
        #wxInitAllImageHandlers()
        img = wxImage(imgpath)
        jpg = wxBitmapFromImage(img)
        return wxStaticBitmap(self, -1, jpg, (-1, -1))
        
class SelectDialog(wxDialog, wxColumnSorterMixin):
    def __init__(self, title, selections, prompt, single_select=0,
                 parent=None, pre_lb_cb=None, post_lb_cb=None,
                 ac_cb=None):
        self.choices = []
        wrestlerData = {}
        for i in range(1, len(selections) + 1):
            wrestlerData[i] = selections[i-1]
            
        wxDialog.__init__(self, parent, -1, title, pos=wxDefaultPosition)
        dlgSzr = wxBoxSizer(wxVERTICAL)
        dlgSzr.Add(wxStaticText(self, -1, prompt), 0,
                   wxALIGN_CENTER|wxEXPAND|wxALL,
                   border=10)

        if pre_lb_cb:
            # Allow a widget to be inserted before the listbox
            dlgSzr.Add(pre_lb_cb(self), 0, wxALIGN_CENTER)
                       
        styleopts = wxLC_REPORT|wxSUNKEN_BORDER|wxLC_VRULES
        if single_select: styleopts = styleopts|wxLC_SINGLE_SEL
        self.listCtrl = JowstListCtrl(self, -1, size=(300, 300),
                                      style=styleopts)
        self.listCtrl.parent = self
        self.populateListCtrl(wrestlerData)
        self.itemDataMap = wrestlerData
        wxColumnSorterMixin.__init__(self, 2)
        self.SortListItems(0, True)
        if ac_cb:
            self.ac_cb = ac_cb
            EVT_LEFT_DCLICK(self.listCtrl, self._showActionCard)
        dlgSzr.Add(self.listCtrl, 0, wxALIGN_CENTER|wxEXPAND|wxALL, border=10)

        if post_lb_cb:
            # Allow a widget to be inserted after the listbox
            dlgSzr.Add(post_lb_cb(self), 0, wxALIGN_CENTER)

        buttSzr = wxBoxSizer(wxHORIZONTAL)
        buttSzr.Add(wxButton(self, wxID_OK, "OK"), 0, wxEXPAND)
        buttSzr.Add((10, 0))
        buttSzr.Add(wxButton(self, wxID_CANCEL, "Cancel"), 0, wxEXPAND)
        dlgSzr.Add(buttSzr, 0, wxALIGN_CENTER|wxALL, border=5)
        
        EVT_LIST_ITEM_SELECTED(self, self.listCtrl.GetId(),
                               self.OnItemSelected)
        EVT_LIST_ITEM_DESELECTED(self, self.listCtrl.GetId(),
                                 self.OnItemDeselected)
        dlgSzr.Fit(self)
        self.SetSizer(dlgSzr)
        self.SetAutoLayout(1)
        self.Layout()
        self.Center()

    def GetListCtrl(self): return self.listCtrl
    
    def GetSelected(self): return self.choices
    def GetSelection(self): return self.choices[0]
    def GetLastSelection(self): return self.choices[-1]
    
    def populateListCtrl(self, wrestlerData):
        self.listCtrl.InsertColumn(0, "Name")
        self.listCtrl.InsertColumn(1, "Set")
        items = wrestlerData.items()
        for i in range(len(items)):
            id = wxNewId()
            key, data = items[i]
            self.listCtrl.InsertStringItem(i, data[0])
            self.listCtrl.SetStringItem(i, 1, data[1])
            self.listCtrl.SetItemData(i, key)

        self.listCtrl.SetColumnWidth(0, wxLIST_AUTOSIZE)
        self.listCtrl.SetColumnWidth(1, wxLIST_AUTOSIZE)            

    def OnItemSelected(self, evt):
        wrestlerFileName = self.itemDataMap[evt.GetData()][2] 
        self.choices.append(wrestlerFileName)

    def OnItemDeselected(self, evt):
        wrestlerFileName = self.itemDataMap[evt.GetData()][2] 
        self.choices.remove(wrestlerFileName)

    def _showActionCard(self, evt):
        selection = evt.GetEventObject().parent.GetLastSelection()
        self.ac_cb(selection, self._doShowActionCard)
        
    def _doShowActionCard(self, wrestler):
        from gui.jowstgui import WrestlerViewer
        WrestlerViewer(None, [wrestler])        
        

                                           
class JowstListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wxDefaultPosition,
                 size=wxDefaultSize, style=0):
        wxListCtrl.__init__(self, parent, ID, pos, size, style)
        wxListCtrlAutoWidthMixin.__init__(self)
        
class NetworkingStartDialog(wxDialog):
    def __init__(self, caption, title):
        wxDialog.__init__(self, None, -1, title)
       
        self.dlgSzr = wxBoxSizer(wxVERTICAL)
        font = wxFont(18, wxSWISS, wxNORMAL, wxNORMAL)
        hdr = wxStaticText(self, -1, caption)
        hdr.SetFont(font)
        self.dlgSzr.Add(hdr, 0, wxALL|wxALIGN_CENTER, border=10)
        self.dlgSzr.Fit(self)
        self.SetSizer(self.dlgSzr)
        self.SetAutoLayout(1)
        
    def addConnectToServerField(self):
        szr = wxBoxSizer(wxHORIZONTAL)
        szr.Add(wxStaticText(self, -1,
                             "Server hostname or ip address:"),
                0, wxALL, border=5)
        
        self.serverNameCtrl = wxTextCtrl(self, -1, '', size=(125, -1))
        szr.Add(self.serverNameCtrl, 0, wxALL, border=5)
        self.dlgSzr.Add(szr, 0)
        self.dlgSzr.Fit(self)

    def addPortField(self):
        portSzr = wxBoxSizer(wxHORIZONTAL)
        portSzr.Add(wxStaticText(self, -1, "Server Port:"), 0, wxALL, border=5)
        self.portCtrl = wxTextCtrl(self, -1, "7101", size=(40, -1))
        EVT_TEXT(self, self.portCtrl.GetId(), self._checkPort)
        portSzr.Add(self.portCtrl, 0, wxALL, border=5)
        self.dlgSzr.Add(portSzr, 0)
        self.dlgSzr.Fit(self)

    def _checkPort(self, evt):
        if self.portCtrl.GetValue() == "7100":
            dlg = wxMessageDialog(self,
                                  "7100 is a reserved port.  Select another.",
                                  "Invalid port number", wxOK | wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            
    def addServerPasswordField(self):
        passwdSzr = wxBoxSizer(wxHORIZONTAL)
        passwdSzr.Add(wxStaticText(self, -1, "Password:"), 0, wxALL,
                      border=5)
        self.passwdCtrl = wxTextCtrl(self, -1, '', size=(125, -1))
        passwdSzr.Add(self.passwdCtrl, 0, wxALL, border=5)
        self.dlgSzr.Add(passwdSzr)
        self.dlgSzr.Fit(self)

    def addButtons(self):
        buttSzr = wxBoxSizer(wxHORIZONTAL)
        buttSzr.Add(wxButton(self, wxID_OK, "OK"), 0, wxEXPAND)
        buttSzr.Add((10, 0))
        buttSzr.Add(wxButton(self, wxID_CANCEL, "Cancel"), 0, wxEXPAND)
        self.dlgSzr.Add(buttSzr, 0, wxALIGN_CENTER|wxALL, border=5)
        self.dlgSzr.Fit(self)


    def addPlayerNameField(self):
        playerName = 'player1'
        playerNameSzr = wxBoxSizer(wxHORIZONTAL)
        playerNameSzr.Add(wxStaticText(self, -1, "Player Name:"), 0,
                          wxALL, border=5)
        if hasattr(pwsconfig, "playerName"):
            playerName = pwsconfig.playerName
        self.playerNameCtrl = wxTextCtrl(self, -1, playerName,
                                         size=(125, -1))
        playerNameSzr.Add(self.playerNameCtrl, 0, wxALL, border=5)
        self.dlgSzr.Add(playerNameSzr, 0)
        self.dlgSzr.Fit(self)
        
    def addAdminPasswordField(self):
        adminPasswdSzr = wxBoxSizer(wxHORIZONTAL)
        adminPasswdSzr.Add(wxStaticText(self, -1,
                                        "Administrative Password:"), 0,
                           wxALL, border=5)
        
        self.adminPasswdCtrl = wxTextCtrl(self, -1, '', size=(125, -1))
        adminPasswdSzr.Add(self.adminPasswdCtrl, 0, wxALL, border=5)
        self.dlgSzr.Add(adminPasswdSzr, 0)
        self.dlgSzr.Fit(self)

    def addNumPlayersField(self):
        numPlayersSzr = wxBoxSizer(wxHORIZONTAL)
        numPlayersSzr.Add(wxStaticText(self, -1, "Number of Players:"), 0,
                          wxALL, border=5)
        self.numPlayersCtrl = wxTextCtrl(self, -1, '6', size=(20, -1))
        numPlayersSzr.Add(self.numPlayersCtrl, 0, wxALL, border=5)
        self.dlgSzr.Add(numPlayersSzr, 0)
        self.dlgSzr.Fit(self)
        

    def getServerName(self): return self.serverNameCtrl.GetValue()
    def getPort(self): return int(self.portCtrl.GetValue())
    def getServerPassword(self): return self.passwdCtrl.GetValue()
    def getNumPlayers(self): return int(self.numPlayersCtrl.GetValue())
    def getPlayerName(self): return self.playerNameCtrl.GetValue()    


from wxPython.wx import *

class DiceRoll(wxPanel):
    def __init__(self, parent, size=(40, 40)):
        self.size = size
        wxPanel.__init__(self, parent, -1, size=size)
        self.SetBackgroundColour("BLACK")
        EVT_PAINT(self, self.OnPaint)
        self.width  = size[0] - 12
        self.height = size[1] - 12
        self.x = (size[0] - self.width) / 2
        self.y = (size[1] - self.height) / 2
        
        self.LEFT   = self.x + self.width / 4
        self.CENTER = self.x + self.width / 2
        self.RIGHT  = self.x + 3 * (self.width / 4)
        self.TOP    = self.y + self.height / 4
        self.BOTTOM = self.y + 3 * (self.height / 4)

        self.currPips = 1
        self.disabled = False

    def OnPaint(self, evt):
        dc = wxPaintDC(self)
        self.DoDrawing(dc)

    def DoDrawing(self, dc=None):
        if self.disabled: return
        if not dc:
            dc = wxClientDC(self)
        self.drawDice(dc)
        if self.currPips: self.drawPips(self.currPips)
        
    def drawDice(self, dc):
        dc.BeginDrawing()
        dc.SetPen(wxPen('RED'))
        dc.SetBrush(wxRED_BRUSH)
        dc.DrawRectangle(self.x, self.y, self.width, self.height)
        dc.EndDrawing()
        
    def getPos(self, num):
        return \
        {1:[(self.CENTER, self.CENTER)],
         2:[(self.LEFT, self.TOP), (self.RIGHT, self.BOTTOM)],
         3:[(self.CENTER, self.CENTER),(self.LEFT, self.TOP),
            (self.RIGHT, self.BOTTOM)],
         4:[(self.LEFT, self.TOP), (self.RIGHT, self.TOP),
            (self.LEFT, self.BOTTOM), (self.RIGHT, self.BOTTOM)],
         5:[(self.LEFT, self.TOP), (self.RIGHT, self.TOP),
            (self.LEFT, self.BOTTOM), (self.RIGHT, self.BOTTOM),
            (self.CENTER, self.CENTER)],
         6:[(self.LEFT, self.TOP), (self.RIGHT, self.TOP),
            (self.LEFT, self.BOTTOM), (self.RIGHT, self.BOTTOM),
            (self.LEFT, self.CENTER), (self.RIGHT, self.CENTER)]
         }[num]
    
    def drawPips(self, num):
        dc = wxClientDC(self)
        self.drawDice(dc)
        dc.SetPen(wxPen('WHITE'))
        dc.SetBrush(wxWHITE_BRUSH)
        for x, y in self.getPos(num):
            dc.DrawCircle(x, y, 3)
        self.currPips = num

    def disable(self):
        self.disabled = True
        self.redrawRect('GREY', wxGREY_BRUSH, wxCROSS_HATCH)

    def enable(self):
        self.disabled = False
        self.redrawRect("BLACK", wxBLACK_BRUSH)
        
    def redrawRect(self, penColor, brushColor, style=None):
        dc = wxClientDC(self)
        dc.SetPen(wxPen(penColor))
        dc.SetBrush(brushColor)
        if style:
            b = dc.GetBrush()
            b.SetStyle(style)
            dc.SetBrush(b)
        dc.DrawRectangle(0, 0, self.size[0], self.size[1])

    def isDisabled(self): return self.disabled
        

if __name__ == '__main__':
    app = wxPySimpleApp()
    f = wxFrame(None, -1, "Test Draw")
    d = DiceRoll(f)
    f.Show(1)
    import time
    time.sleep(1)
    d.drawPips(4)
    d.disable()
    time.sleep(1)
    d.enable()
    app.MainLoop()
            

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

import sys, os, random
from wxPython.wx import *
from gui.jowstgui import JowstFrame
from lib.util import setIcon, JOWST_PATH
from data.globalConstants import VERSION
from twisted.internet import reactor
from twisted.python import log

class MyApp(wxPySimpleApp):
    logging = False
    def OnInit(self):
        # Twisted Reactor Code
        #reactor.startRunning()
        EVT_TIMER(self,999999,self.OnTimer)
        self.timer=wxTimer(self,999999)
        #self.timer.Start(250,False)
        # End Twisted Code
	# Do whatever you need to do here
        return True

    def makeReactorCurrent(self):
        reactor.runUntilCurrent()
        
    def OnTimer(self,event):
        reactor.runUntilCurrent()
        reactor.doIteration(0)

    def doLogging(self):
        try:
            pid = str(os.getpid())
        except:  # Just grab a random number
            pid = str(random.randint(1000, 9999))
            
        logFilename = os.path.join(JOWST_PATH, "log", "debug."+
                                   pid + ".txt")
        self.log = open(logFilename, 'w')
        self.logFilename = logFilename
        log.startLogging(self.log, 1)
        self.logging = True
        
def startup(debug):
    app = MyApp()
    if debug: app.doLogging()
    frame = JowstFrame("Pro Wrestling Superstar")
    frame.app = app
    setIcon(frame)
    app.MainLoop()


if __name__=='__main__':
    debug = 0
    if "-debug" in sys.argv:
        debug = 1
    startup(debug) 

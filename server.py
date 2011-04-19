from lib.Networking import JowstServer
from gui.dialogs import NetworkingStartDialog
from lib.util import JOWST_PATH

import socket, os, xmlrpclib, random
from wxPython.wx import *
from twisted.python import log

try:
    _pid = os.getpid()
except:
    _pid = random.randint(1000, 9999)

_logFilename = os.path.join(JOWST_PATH, "log", "server."+
                            str(_pid) + ".txt")
_logFile = open(_logFilename, 'w')
log.startLogging(_logFile, 1)

CLIENT_TOKEN = os.environ["JOWST_CLIENT_TOKEN"]

def stopClient():
    """Connect to the client's xml handshake server and shut it down"""
    handshaker = xmlrpclib.Server("http://localhost:7100")
    clientShutdown = None
    s = 0
    while not clientShutdown:
        try:
            clientShutdown = handshaker.stopClient(CLIENT_TOKEN)
        except socket.error:
            print s
            time.sleep(1)
        except xmlrpclib.Fault:  # Server was shutdown
            clientShutdown = 1
        s +=1
        if s == 30:  # 30 second timeout
            clientShutdown = 1
  
def runserver():
    app = wxPySimpleApp(0)
    startserver = None
    caption = "Starting Server on %s" % socket.gethostname()
    dlg = NetworkingStartDialog(caption, "Start Server")
    dlg.addPortField()
    dlg.addServerPasswordField()
    dlg.addNumPlayersField()
    dlg.addPlayerNameField()
    dlg.addButtons()
    if dlg.ShowModal() == wxID_OK:
        port = int(dlg.getPort())
        serverPasswd = dlg.getServerPassword()
        numPlayers = dlg.getNumPlayers()
        playerName = dlg.getPlayerName()
        startserver = 1
    else:
        stopClient()
    dlg.Destroy()
    if startserver: JowstServer().startServer(passwd=serverPasswd, port=port,
                                              num_players=numPlayers,
                                              hostPlayerName=playerName,
                                              clientToken=CLIENT_TOKEN)
    app.MainLoop()
    
if __name__ == '__main__':
    runserver()

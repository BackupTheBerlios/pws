from twisted.cred import portal, checkers, credentials
from twisted.spread import pb
from twisted.internet import reactor, defer
#from twisted.flow import flow
#from twisted.flow.threads import Threaded

import xmlrpclib
from twisted.web import xmlrpc, server       

from wxPython.wx import EVT_IDLE

from lib.util import generateRandomPassword
from gui.matchSetup import MatchSetupDialog
from lib import Interface, spw
from data.globalConstants import *

import time, socket, Queue, threading, random

class CopyWrestler(spw.Wrestler, pb.Copyable): pass
class ClientWrestler(spw.Wrestler, pb.RemoteCopy): pass
class CopyDice(spw.Dice, pb.Copyable): pass
class ClientDice(spw.Dice, pb.RemoteCopy): pass
class CopyDramaQueen(Interface.DramaQueen, pb.Copyable): pass
class ClientDramaQueen(Interface.DramaQueen, pb.RemoteCopy): pass

pb.setUnjellyableForClass(CopyWrestler, ClientWrestler)                        
pb.setUnjellyableForClass(CopyDice, ClientDice)
pb.setUnjellyableForClass(CopyDramaQueen, ClientDramaQueen)

class Switchboard:
    def __init__(self):
        self.chatService = Chat()
        self.matchSetupService = MatchSetup(self._setState)
        self.players = []
        self.numPlayers = 0
        self.state = MATCH_SETUP
        
    def joinMatchSetupAsPlayer(self, player):
        if self.state == MATCH_SETUP:
            self.matchSetupService.addPlayer(player)
            self.chatService.addPlayer(player)
            self.players.append(player)
            self.numPlayers += 1
            return (self.matchSetupService, self.chatService)

    def joinMatchSetupAsHost(self, host):
        if self.state == MATCH_SETUP:
            self.matchSetupService.addHost(host)
            self.hostPlayerName = host.name
            return (self.matchSetupService, None)

    def startMatch(self):
        self.state = MATCH_RUNNING
        self.realm.state = self.state
        players = self.matchSetupService.getPlayers()
        playerMap = self.matchSetupService.getPlayerMap()
        self.matchService = Match(self.matchSetupService.matchSetupObj, players,
                                  playerMap, self.matchSetupService.reset)

    def sendPromptResultToMatchService(self, name, result):
        self.matchService.handlePromptResult(name, result)
        
    def leaveServer(self, player):
        if self.state == MATCH_SETUP:
            self.matchSetupService.removePlayer(player)
        self.removePlayer(player)
        self.numPlayers -= 1
        
    def removePlayer(self, playerName):
        for playerObj in self.players:
            if playerObj.name == playerName:
                disconnectedPlayer = playerObj
                break
        self.chatService.removePlayer(playerName)
        self.players.remove(disconnectedPlayer)
        self.realm.disconnectClient(playerName)
        
    def shutdownServer(self):
        if self.state == MATCH_RUNNING:
            self.matchService.stopMatch(SHUTTING_DOWN)

        self.state = SHUTTING_DOWN
        self._disconnectPlayers()

    def _disconnectPlayers(self):
        for player in self.players:
            if not player.isHost():
                d = player.client.callRemote("disconnect")
                d.addCallback(self._disconnectPlayer, player)
                player.state = DISCONNECT
        self._doShutdown()
        
    def _disconnectPlayer(self, doit, player):
        self.players.remove(player)
        self.realm.disconnectClient(player.name)

    def _doShutdown(self):
        reactor.callLater(5, self.shutdownCB)      
        self.realm.disconnectClient(self.players[0].name)  # Disconnect Host       
        
    def stopNetGame(self):
        if self.state == MATCH_RUNNING:
            self.matchService.stopMatch()

        self.state = MATCH_SETUP

        return MATCH_SETUP

    def _setState(self, state):
        self.state = state
        
class Chat(pb.Viewable):
    def __init__(self):
        self.players = []
        
    def view_receiveChatMessage(self, perspective, msg):
        # Make sure we have a valid message
        if len(msg.strip()):
            msg = "%s\n" % msg
            self.sendChatMessage(perspective.name, msg)

    def addPlayer(self, player):
        self.players.append(player)
        msg = "%s has joined the server.\n" % (player.name)
        self.sendChatMessage("*****SERVER MESSAGE*****", msg)

    def removePlayer(self, playerName):
        for playerObj in self.players:
            if playerObj.name == playerName:
                disconnectedPlayer = playerObj
                break

        self.players.remove(disconnectedPlayer)
        msg = "%s has left the server.\n" % (playerName)
        self.sendChatMessage("*****SERVER MESSAGE*****", msg)
        
    def sendChatMessage(self, sender, msg):
        for player in self.players:
            player.client.callRemote("receiveChatMessage", sender, msg)
            
class MatchSetup(pb.Viewable):
    def __init__(self, switchBoardStateCB):
        self.players = []
        self.readyPlayers = []
        self.playerMap = {}
        self.host = None
        self.hostClientName = None
        self.matchSetupObj = Interface.MatchSetup(network=1)
        # The following widgets (dict values) can only be changed by the host.
        # The keys are the associated match setup methods.
        self.widgetUpdateMap = {
                                 "setTimeLimit": "timeLimitEntry",
                                 "setDQ": "dqEnabled",
                                 "setDramaticPause": "dramaticPause",
                                 "setRealtimePins": "realtimePins",
                                 "setRealtimeCountouts":"realtimeCountouts",
                                 "setSubmissionDrama":"submissionDrama",
                                 "setStrategyChart":"strategyChart",
                                 "setPinOnlyOnPA":"pinOnlyOnPA",
                                 "setMatchType": "matchChoice"
                               }
        self.cpuUpdateMap = {
                             "addCPU": 1,
                             "removeCPU": 0
                            }
        
        self.queue = Queue.Queue()
        self.playerConnections = 0
        self.swicthboardStateCB = switchBoardStateCB
        
    def view_getCurrentSetupValues(self, perspective):
        playerDict = {}
        valdict = self.matchSetupObj.getCurrentSetupValues()
        playerDict.update(self.playerMap)

        # Remove the player perspectives from the dictionary that will be returned
        for player in self.playerMap.keys():
            playerDict[player] = {}
            for key in self.playerMap[player].keys():
                if key != "CLIENT": playerDict[player][key] = self.playerMap[player][key]
        valdict["PLAYER_MAP"] = playerDict
        return valdict
        
    def view_playerReady(self, perspective):
        self.readyPlayers.append(perspective.name)
        self._sendUpdate("setPlayerReady", perspective.name, perspective)
        
    def view_sendMatchSetupMsg(self, perspective, msg, *args):
        result = -1
        func = getattr(self.matchSetupObj, msg)
        if msg in self.widgetUpdateMap.keys():
            if not perspective.isHost(): return
            func(*args)
            newargs = list(args) + [perspective]
            self._sendUpdate("updateWidget", self.widgetUpdateMap[msg], *newargs)
        elif msg in ("addCPU", "removeCPU"):
            if args[0] in self.playerMap[perspective.name].keys() or perspective.isHost():
                func(*args)
                newargs = list(args) + [self.cpuUpdateMap[msg], perspective]
                self._sendUpdate("updateCPU", *newargs)
            else:
                # Prevent players from updating a wrestler they don't control
                newargs = list(args) + [not self.cpuUpdateMap[msg], perspective]
                perspective.client.callRemote("updateCPU", *newargs[:-1])
        else:
            newargs = list(args) + [self._putInQueue]
            if msg != "removeWrestler":  # Don't remove wrestler at this point
                func(*newargs)
                result = self.queue.get()

            if type(result) != type(()):
                playerName = perspective.name
                if msg == "addWrestler":
                    team, filename = args[:2]
                    wrestlerName = self.matchSetupObj.getWrestlerName(filename)
                    self.playerMap[perspective.name][wrestlerName] = team 
                    self._sendUpdate("receiveWrestlerUpdate", team, wrestlerName, 1, perspective)
                    self._sendUpdateToAllPlayers("updatePlayerTree", team, wrestlerName, 1, playerName)
                elif msg == "removeWrestler":
                    team, wrestlerName = args[:2]
                    if wrestlerName in self.playerMap[playerName].keys() or perspective.isHost():
                        func(*newargs)
                        result = self.queue.get()
                        self.playerMap[perspective.name].pop(wrestlerName, None)
                        self._sendUpdate("receiveWrestlerUpdate", team, wrestlerName, 0, perspective)
                        self._sendUpdateToAllPlayers("updatePlayerTree", team, wrestlerName, 0, playerName)
                    else:
                        result = -1
            return result                                

    def _putInQueue(self, val, *args):
        self.queue.put(val)
        
    def _sendUpdate(self, *args):
        newargs = args[:-1]
        perspective = args[-1]
        # Send messages to all clients, except for the client who called for
        #  an update
        for player in self.players:
            if player.name != perspective.name and player.name not in self.readyPlayers:
                player.client.callRemote(*newargs)

    def _sendUpdateToAllPlayers(self, *args):
        # Send update to all clients
        for player in self.players:
            if player.name not in self.readyPlayers:
                player.client.callRemote(*args)
                
    def addPlayer(self, player):
        # New player added, send message to all clients
        self._sendUpdateToAllPlayers("addNewPlayer", player.name)
        self.playerConnections += 1
        self.players.append(player)
        self.playerMap[player.name] = {"CLIENT":player}

    def addHost(self, host):
        self.host = host
        self.hostClientName = self.host.name

    def removePlayer(self, player):
        wrestlerItems = []
        for key in self.playerMap[player].keys():
            if key != "CLIENT":
                wrestlerItems.append((key, self.playerMap[player][key]))
            else:
                playerPersp = self.playerMap[player][key]
        for item in wrestlerItems:
            """item[1] = team number, item[0] = wrestler name"""
            self.matchSetupObj.removeWrestler(item[1], item[0], self._putInQueue)
            self.queue.get()
            self._sendUpdate("receiveWrestlerUpdate", item[1], item[0], 0, playerPersp)
            
        self.playerMap.pop(player)
        for playerObj in self.players:
            if playerObj.name == player:
                disconnectedPlayer = playerObj
                break
        self.players.remove(disconnectedPlayer)
        self._sendUpdateToAllPlayers("removePlayer", player)

    def reset(self):
        self.matchSetupObj = Interface.MatchSetup(network=1)
        self.readyPlayers = []
        # Re-initialize the playerMap
        for player in self.playerMap.keys():
            for key in self.playerMap[player].keys():
                if key != "CLIENT": self.playerMap[player].pop(key)
        self.swicthboardStateCB(MATCH_SETUP)
        
    def getPlayerMap(self): return self.playerMap
    def getPlayers(self): return self.players
    
class Match:
    def __init__(self, setupObj, players, playerMap, matchSetupReset):
        self.prompts =("GENERIC_PROMPT", "YES_OR_NO_PROMPT", "CHOICE_LIST")
        self.players = players
        self.playerMap = playerMap
        self._resultQueue = Queue.Queue()
        self._messageQueue = Queue.Queue()
        self._signalQueue = Queue.Queue()
        self.resetCB = matchSetupReset
        setupObj.getDrama(self._setDrama)
        setupObj.getMatchObject(self._setMatchObject)
        self.readyPlayers = 0
        self._playersReadyForNextRound = []
        self.waitingForPromptResults = 0
        self.playerPrompted = ''
        self.state = STARTING_MATCH

    def sendMessage(self, msg, **kw):
        self._currentMessage = msg
        if msg not in self.prompts:
            deferreds = []
            self.waitingForPromptResults = 1
            for player in self.players:
                origkw = {}
                origkw.update(kw)
                if player.isHost() and msg == "FINISH":
                    kw['resultdata'] = self.matchObj.getMatchResultData()
                    mType = self.matchObj.getMatchType()
                    noWinner = self.matchObj.isDraw() or \
                           self.matchObj.isDoubleCountout()

                    kw['resultdata']["MATCH_TYPE"] = mType
                    kw['resultdata']["NO_WINNER"] = noWinner                   
                    
                deferreds.append(player.client.callRemote("receiveMessage",
                                                          msg, **kw))
                kw = origkw
            return defer.DeferredList(deferreds)
        else:
            wrestler = kw['man']
            wrestlerName = wrestler.getName()
            wrestlerTeam = wrestler.getTeamNum()
            for player in self.playerMap.keys():
                if self.playerMap[player].has_key(wrestlerName):
                    if self.playerMap[player][wrestlerName] == wrestlerTeam:
                        playerClient = self.playerMap[player]["CLIENT"]
                        self.waitingForPromptResults = 1
                        self.playerPrompted = player
                        return playerClient.client.callRemote("receiveMessage", msg, **kw)
                        
    def handlePromptResult(self, name, result):
        if not self.waitingForPromptResults:
            print "not waiting for prompt"
            return
        if self._currentMessage in self.prompts:
            if name != self.playerPrompted:
                print name, "was not prompted"
                return
            self.waitingForPromptResults = 0
            self.playerPrompted = ''
            self._resultQueue.put(result)
        else:
            if name not in self._playersReadyForNextRound:
                self._playersReadyForNextRound.append(name)
            if len(self._playersReadyForNextRound) == len(self.players):
                self.waitingForPromptResults = 0
                self._playersReadyForNextRound = []
                self._resultQueue.put(result)
        
    def _setMatchObject(self, matchObj):
        self.matchObj = matchObj
        self.matchObj.setInterfaces(self._resultQueue, self._messageQueue,
                                    self._signalQueue)
        teams = self.matchObj.getTeams()
        matchtype = self.matchObj.getMatchType()
        timelimit = self.matchObj.getTimeLimit()
        imageFile = self.matchObj.getImageFile()
        labelData = self.matchObj.getLabelData()
        
        # Tell clients to setup their GUIs
        for player in self.players:
            playerWrestlers = []
            # Build a list of wrestlers the player controls
            for key in self.playerMap[player.name]:
                if key != "CLIENT":
                    playerWrestlers.append(key)
                    
            player.client.callRemote("startMatch", teams, playerWrestlers,
                                     timelimit, self.drama,
                                     matchtype, imageFile, labelData).addCallback(self._setReadyPlayer)
        
    def _setDrama(self, drama): self.drama = drama
    def _setReadyPlayer(self, player):
        if player in self.playerMap.keys():
            self.readyPlayers += 1

        # Start Match When everyone is ready
        if self.readyPlayers == len(self.playerMap.keys()):
            self.matchThread = threading.Thread(target=self._matchRunner)
            #reactor.callLater(0, self._checkMessageQueue)
            threading.Thread(target=self._checkMessageQueue).start()
            self.matchThread.start()
            self.state = MATCH_RUNNING

    def _handleError(self, result):
        print "Unexpected event"
        
    def _checkMessageQueue(self):
        #if not self._messageQueue.empty():
        while self.state not in (SHUTTING_DOWN, MATCH_STOPPED):
            msg, kw = self._messageQueue.get()
            #print `msg`, kw
            if msg:
                self.sendMessage(msg, **kw).addErrback(self._handleError)

        #if self.state not in (SHUTTING_DOWN, MATCH_STOPPED):
        #    reactor.callLater(0, self._checkMessageQueue)
            
    def stopMatch(self, server_state=MATCH_STOPPED):
        self.matchObj.stopMatch()
        self.state = server_state
            
    def _matchRunner(self):
        self.matchObj.runMatch()
        # We know for sure the match is done if we get the
        # 'MATCH_STOPPED' signal in the signalQueue
        self.state = self._signalQueue.get()
        self._messageQueue.put((None, None))
        if self.state != SHUTTING_DOWN:
            for player in self.players:
                try: 
                    player.client.callRemote("matchEndMessage", "Resetting Game Arena...", "reset")
                except:  # If client has disconnected, continue
                    print "Could not send match end message to", player.name
            time.sleep(5)
            # Tell clients to cleanup their GUIs if the match was
            #  stopped by the host or if the match finished cleanly
            for player in self.players:
                try: 
                    player.client.callRemote("restartGame", "reset")
                except:  # If client has disconnected, continue
                    print "Could not send restart message to", player.name

            self.resetCB()

        # Cleanup queues
        for q in (self._resultQueue, self._messageQueue, self._signalQueue):
            while not q.empty():
                q.get()

    def getPlayerMap(self): return self.playerMap
    def getPlayers(self): return self.players

    
class Player(pb.Avatar):
    def __init__(self, client):
        self.client = client
        self.name = None
        self.connections = 0
        self.state = CONNECTED

    # self.server = Switchboard() in joinMatchSetupAsPlayer
    def perspective_joinMatchSetup(self):
        if self.name:
            return self.server.joinMatchSetupAsPlayer(self)
        else: return None
    def perspective_leaveServer(self):
        self.state = DISCONNECT
        self.server.leaveServer(self.name)

    def perspective_sendPromptResult(self, result):
        self.server.sendPromptResultToMatchService(self.name, result)
        
    def disconnect(self):
        if self.state != DISCONNECT:
            self.server.leaveServer(self.name)

    def validateIdentity(self, transport, playernames):
        d = self.client.callRemote("getClientName")
        d.addCallback(self._validateName, transport, playernames)
        return d
  
    def isHost(self): return False
    def _validateName(self, name, transport, playernames):
        if name in playernames:
            newname = name
            val = 1
            while newname in playernames:
                newname += str(val)
                val += 1
            self.client.callRemote("setClientName", newname)
            self.name = newname
        else:
            self.name = name
        return (self.name, transport)
        
class Host(pb.Avatar, Player):
    def __init__(self, client):
        Player.__init__(self, client)
        
    # self.server = Switchboard() in joinMatchSetupAsPlayer
    def perspective_joinMatchSetup(self):
        if self.name:
            self.server.joinMatchSetupAsHost(self)
            return Player.perspective_joinMatchSetup(self)
        else: return None

    def perspective_startMatch(self):
        self.server.startMatch()
    def perspective_stopServer(self):
        self.server.shutdownServer()

    def perspective_stopNetGame(self):
        return self.server.stopNetGame()
        
    def disconnect(self):
        # If we're somehow unexpectedly disconnected, try to
        #  shut down the server.
        if self.server.state != SHUTTING_DOWN:
            self.server.shutdownServer()

    def isHost(self): return True
    def _validateName(self, name):
        self.name = name

from twisted.python import failure
class JowstRealm:
    __implements__ = portal.IRealm
    numConnections = 0
    hostConnected = False
    connectedClients = {}
    
    def requestAvatar(self, avatarID, mind, *interfaces):
        assert pb.IPerspective in interfaces
        if self.numConnections + 1 > self.maxPlayers or self.state == MATCH_RUNNING:
            avatarID = ''

        if avatarID == "player" and self.hostConnected:
            p = Player(mind)
            p.server = self.server
            d = p.validateIdentity(mind.broker.transport, self.connectedClients.keys())
            d.addCallback(self._addPlayerToClientList)
            self.numConnections += 1
            return pb.IPerspective, p, p.disconnect
        elif avatarID == "host" and not self.hostConnected:
            self.hostConnected = True
            self.clientHost = Host(mind)
            self.clientHost.server = self.server
            self.clientHost.name = self.hostPlayerName
            self.numConnections += 1
            self.connectedClients[self.hostPlayerName] = mind.broker.transport
            return pb.IPerspective, self.clientHost, self.clientHost.disconnect
        else:
            mind.broker.transport.loseConnection()
            return defer.fail(pb.Error(TooManyConnections))

    def _addPlayerToClientList(self, validatedData):
        name = validatedData[0]
        # If someone else snuck in during validation, boot
        #  the slow poke
        if name in self.connectedClients.keys():
            validatedData[1].loseConnection()
            self.numConnections -= 1
            return

        self.connectedClients[name] = validatedData[1]

    def disconnectClient(self, playerName):
        self.connectedClients[playerName].loseConnection()
        self.connectedClients.pop(playerName)
        self.numConnections -= 1

class TooManyConnections: pass

class JowstClient(pb.Referenceable):
    def __init__(self, usertype, ifCB, name, passwd='', hostname="localhost",
                 port=7101, host=0,
                 clientToken=None):
        self.usertype = usertype
        self.passwd = passwd
        self.hostname = hostname
        self.port = port
        self.handshakePort = None
        self.factory = pb.PBClientFactory()
        self.host = host
        self.clientToken = clientToken
        self._setupGUI = None
        self.name = name
        self._sendMessage = ifCB
        self.remoteSetupObj = None
        self.setupQueue = Queue.Queue()
        self._isConnected = False
        self.state = None

        
        if self.host:
            self.handshakeListener = Handshaker()
            self.handshakeListener.stopClientCB = self.stopClient
            self.handshakeListener.setPasswdCB = self.setHostPassword
            
    def isHost(self): return self.host
        
    def remote_addNewPlayer(self, playerName):
        self._setupGUI.addPlayer(playerName, self.name)

    def remote_setPlayerReady(self, player):
        self._setupGUI.setPlayerReady(player)
        
    def remote_updateWidget(self, widget, val):
        print "updating", widget
        self._setupGUI.controlGUI.updateControlWidget(widget, val)

    def remote_updateCPU(self, wrestler, team, val):
        print "updateCPU", wrestler, team, 1
        widget = self._setupGUI.controlGUI.teamLists[team]
        widget.Check(widget.FindString(wrestler), val)
        
    def remote_getClientName(self): return self.name
    def remote_setClientName(self, name): self.name = name
    def remote_receiveWrestlerUpdate(self, team, name, add):
        widget = self._setupGUI.controlGUI.teamLists[team]
        if add: widget.Append(name)
        else: widget.Delete(widget.FindString(name))
        
    def remote_updatePlayerTree(self, team, name, add, player):
        if add: self._setupGUI.addWrestlerToPlayerTree(player, name, team)
        else: self._setupGUI.removeWrestlerFromPlayerTree(player, name)
        
    def remote_startMatch(self, teamlist, playerWrestlers, timeLimit, dramaobj,
                          matchType, matchImage, labelData):
        print "starting match"
        self._sendMessage("CLOSE_POPUP_WIN", win_name="serverWait")
        self._sendMessage("START_MATCH", teams=teamlist, player_wrestlers=playerWrestlers,
                          timelimit=timeLimit, drama=dramaobj, network=1,
                          matchtype=matchType, matchimage=matchImage,
                          labeldata=labelData)
        return self.name

    def remote_removePlayer(self, player):
        self._setupGUI.removePlayer(player)
        
    def remote_receiveMessage(self, msg, **kw):
        kw["callback"] = self.sendResult
        self._sendMessage(msg, **kw)

    def remote_receiveChatMessage(self, player, msg):
        if self.state == MATCH_SETUP:
            self._setupGUI.handleChatMessage(player, msg)
        else:
            self._sendMessage("CHAT_MSG", playername=player, message=msg)
    
    def remote_matchEndMessage(self, text, winName):
        self._sendMessage("SHOW_POPUP_WIN", win_text=text, win_name=winName)

    def remote_restartGame(self, winName):
        self._sendMessage("CLOSE_POPUP_WIN", win_name=winName)
        self._restartNetGame(None)
            
    def remote_disconnect(self):
        # Try to destroy setup GUI if one exists
        try:
            self._setupGUI.Destroy()
        except:
            pass
        self._disconnect(None)
        self._sendMessage("CLEANUP_UI")
        return 1

    def _sendMatchSetupMsg(self, msg, *args):
        return self.remoteSetupObj.callRemote("sendMatchSetupMsg", msg, *args)
        
    def sendChatMsg(self, msg):
        self.remoteChatObj.callRemote("receiveChatMessage", msg)
            
    def sendResult(self, result):
        self.perspective.callRemote("sendPromptResult", result)
        
    def isConnected(self): return self._isConnected
    
    def _populateSetupGUI(self, valdict):
        self._setupGUI.controlGUI.timeLimitEntry.SetValue(valdict["TIME_LIMIT"])
        if valdict["TIME_LIMIT"] == NO_TIME_LIMIT:
            self._setupGUI.controlGUI.noTimeLimitChkbox.SetValue(1)
        else:
            self._setupGUI.controlGUI.noTimeLimitChkbox.SetValue(0)
        self._setupGUI.controlGUI.dqEnabled.SetValue(valdict["DQ_ENABLED"])

        dramaPause = valdict["DRAMA"].getDramaPause()
        rtpins = valdict["DRAMA"].getRealtimePins()
        rtcountouts = valdict["DRAMA"].getRealtimeCountouts()
        subdrama = valdict["DRAMA"].getSubmissionDrama()

        self._setupGUI.controlGUI.dramaticPause.SetValue(dramaPause)
        self._setupGUI.controlGUI.realtimePins.SetValue(rtpins)
        self._setupGUI.controlGUI.realtimeCountouts.SetValue(rtcountouts)
        self._setupGUI.controlGUI.submissionDrama.SetValue(subdrama)

        # Add teams to teamlists and set up their CPU status
        t = 0
        for team in valdict["TEAMS"]:
            teamCPUs = valdict["CPUS"][t]
            widget = self._setupGUI.controlGUI.teamLists[t]
            for member in team:
                widget.Append(member)
                if member in teamCPUs:
                    widget.Check(widget.FindString(member), 1)
            t += 1

        # Add Players and the wrestlers they control to the player Tree
        for player in valdict["PLAYER_MAP"].keys():
            self._setupGUI.addPlayer(player, self.name)
            for wrestler in valdict["PLAYER_MAP"][player].keys():
                self._setupGUI.addWrestlerToPlayerTree(player, wrestler,
                                                       valdict["PLAYER_MAP"][player][wrestler])
                
            
                    
    def setPerspective(self, perspective):
        self._isConnected = True
        self.perspective = perspective
        self.perspective.callRemote("joinMatchSetup").addCallback(self._setRemoteObjects)
        if self.isHost():
            self._setupObj = Interface.HostMatchSetup(self._sendMatchSetupMsg)
            self._showHostMatchSetupGUI()
        else:
            self._setupObj = Interface.ClientMatchSetup(self._sendMatchSetupMsg)
            self._showPlayerMatchSetupGUI()
        
    def _showHostMatchSetupGUI(self):
        trueItems = ("Stop Network Game", "Stop Server")
        falseItems = ("Start Network Game", "Connect To Server")
        self._sendMessage("ENABLE_MENUS", menuname="NetworkMenu",
                          trueitems=trueItems, falseitems=falseItems)

        trueItems = []
        falseItems = ("Run Match")
        self._sendMessage("ENABLE_MENUS", menuname="RunMenu",
                          trueitems=trueItems, falseitems=falseItems)

        self._setupGUI = MatchSetupDialog(self._setupObj, self.sendChatMsg)
        self._setupGUI.buildMatchControlGUI()
        self._setupGUI.enableWidgetEvents()
        self._setupGUI.enableWidgets()
        self._setupGUI.buildCommPanel()
        self._setupGUI.addButtons(canceltext="Stop Server", disconnect=1)
        self._showSetupGUI()

    def _setRemoteObjects(self, objTuple):
        if not self.remoteSetupObj:
            self.remoteSetupObj = objTuple[0]
        if objTuple[1]:
            self.remoteChatObj = objTuple[1]
        
    def _showPlayerMatchSetupGUI(self):
        self._setupGUI = MatchSetupDialog(self._setupObj, self.sendChatMsg)
        self._setupGUI.buildMatchControlGUI()
        self._setupGUI.enableWidgets(0)
        self._setupGUI.buildCommPanel()
        self._setupGUI.addButtons(starttext="Ready", canceltext="Disconnect", disconnect=1)
        self._showSetupGUI()

    def _showSetupGUI(self):
        self._setupGUI.Show(1)
        self.setupQueue.put(1)
        self.state = MATCH_SETUP
        EVT_IDLE(self._setupGUI, self._checkState)

    def _checkState(self, evt):
        """This method checks the state of the match setup GUI
           TODO: This should be moved to the MainJowstWindow class"""
        if self._setupGUI.state == READY_TO_START_MATCH:
            if self.isHost():
                self.perspective.callRemote("startMatch")
            else:
                self.remoteSetupObj.callRemote("playerReady")
                self._sendMessage("SHOW_POPUP_WIN", win_name="serverWait",
                                  win_text="Waiting for host to start match...")
            self._setupGUI.state = STARTING_MATCH
            self._setupGUI.Destroy()
            self.state = MATCH_RUNNING
        elif self._setupGUI.state == DISCONNECT:
            if self.isHost():
                d = self.perspective.callRemote("stopServer")
            else:
                d = self.perspective.callRemote("leaveServer")
            d.addCallbacks(self._disconnect, self.handleShutdownFailure)
            self._setupGUI.Destroy()
        elif not self.setupQueue.empty() and self.remoteSetupObj:
            guibuilt = self.setupQueue.get()
            # Ask for current match setup
            self.remoteSetupObj.callRemote("getCurrentSetupValues").addCallback(self._populateSetupGUI)
            
            
    def _disconnect(self, val):
        self._sendMessage("DISCONNECT_MSG", message="Disconnected from Server",
                          caption="Disconnected")
                
    def startClient(self):
        if self.isHost():
            self.handshakePort = reactor.listenTCP(7100, server.Site(self.handshakeListener),
                                                   interface='localhost')
        else: self.connectToService()

    def stopNetGame(self):
        self.perspective.callRemote("stopNetGame")       

    def disconnectFromServer(self):
        self.perspective.callRemote("leaveServer")
        self._disconnect(None)

    def stopServer(self):
        self.perspective.callRemote("stopServer").addCallbacks(self._disconnect,
                                                               self.handleShutdownFailure)
    def _restartNetGame(self, server_state):
        self._sendMessage("CLEANUP_UI", shutdown=0)
        if self.isHost():
            self._showHostMatchSetupGUI()
        else:
            self._showPlayerMatchSetupGUI()
        
    def setHostPassword(self, adminpasswd, passwd, hostPlayerName, clientToken):
        retval = 0
        if clientToken == self.clientToken:
            self.name = hostPlayerName
            self.passwd = passwd
            self.adminpasswd = adminpasswd
            self.connectToService()
            retval = 1
        return retval

    def stopClient(self, clientToken):
        retval = 0
        if clientToken == self.clientToken:
            self.handshakePort.stopListening()
            retval = 1
        return retval
            
    def connectToService(self):
        if self.handshakePort:
            self.handshakePort.stopListening()
            self.handshakePort = None
            
        reactor.connectTCP(self.hostname, self.port, self.factory)
        if self.isHost():
            self.passwd = self.adminpasswd
            
        defPer = self.factory.login(credentials.UsernamePassword(self.usertype,
                                                                 self.passwd),
                                    client=self)
        defPer.addCallback(self.setPerspective)
        defPer.addErrback(self.handleError)

    def handleError(self, failure):
        print failure
        self._sendMessage("DISCONNECT_MSG",
                          message="Unable to connect to server\nbecause the maximum\n" +\
                                  "connection limit was reached,\nthe incorrect password" +\
                                  " was entered,\nor the host was not found.",
                          caption="Unable to connect to server.")

    def handleShutdownFailure(self, failure):
        pass

class JowstServer:
    dedicated = 0
    def connectToHandshaker(self):
        handshaker = xmlrpclib.Server("http://localhost:7100")
        passwdSet = None
        s = 0
        
        while not passwdSet:
            try:
                print "connected to host client"
                shookhands = handshaker.handshake()
                if shookhands:
                    passwdSet = handshaker.setHostPassword(self.adminpasswd,
                                                           self.passwd,
                                                           self.playerName,
                                                           self.clientToken)
                        
            except socket.error:
                print s
                time.sleep(1)
            s +=1
            if s == 60:
                reactor.stop()
                
    def startServer(self, adminpasswd='', passwd='', port=7101, num_players=6, hostPlayerName='host_player',
                    clientToken=None):
        self.adminpasswd = adminpasswd
        self.passwd = passwd
        self.port = port
        self.maxPlayers = num_players
        self.serverPort = None
        self.playerName = hostPlayerName
        self.clientToken = clientToken
        if not self.adminpasswd: self.adminpasswd = generateRandomPassword()
        self.startService()
        if not self.dedicated: self.connectToHandshaker()
        reactor.run()


    def startService(self):
        realm = JowstRealm()
        realm.server = Switchboard()
        realm.server.shutdownCB = self.shutdownServer
        realm.server.realm = realm
        realm.state = MATCH_SETUP
        realm.hostPlayerName = self.playerName
        realm.maxPlayers = self.maxPlayers
        self.checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
        self.checker.addUser("host", self.adminpasswd)
        self.checker.addUser("player", self.passwd)
        p = portal.Portal(realm, [self.checker])
        self.serverPort = reactor.listenTCP(self.port, pb.PBServerFactory(p))

    def shutdownServer(self):
        reactor.stop()
        
class Handshaker(xmlrpc.XMLRPC):
    setPasswdCB = None
    stopClientCB = None
    def xmlrpc_handshake(self):
        return 1

    def xmlrpc_setHostPassword(self, adminpasswd, passwd, playername, clientToken):
        return self.setPasswdCB(adminpasswd, passwd, playername, clientToken)

    def xmlrpc_stopClient(self, clientToken):
        self.stopClientCB(clientToken)

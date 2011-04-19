import math, random

class Team:
    def __init__(self, data, seed):
        self.data = data
        self.seed = seed
    def getSeed(self): return self.seed    
    def getData(self): return self.data
    
class SingleEliminationSeeds:
    def __init__(self, maxSize):
        self.maxSize = maxSize

    def getSeedOrder(self):
        return self.expand([1, 2])
        
    def expand(self, currList):
        currSize = len(currList)
        newSize = currSize * 2
        seeds = [c for c in range(1, newSize + 1)]
        newList = [0 for x in range(newSize)]
        newList[0] = 1
        lowseed = seeds[-1]
        if lowseed <= self.maxSize:
            newList[1] = lowseed

        for idx in range(1, len(currList)):
            newList[idx * 2] = currList[idx]
            lowseed = newSize - currList[idx] + 1
            if lowseed <= self.maxSize:
                newList[idx * 2 + 1] = lowseed

        if newSize < self.maxSize:
            newList = self.expand(newList)

        return newList


class Node:
    """
    Node in the Tournament Tree
    """
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.team = None
        self.isdirty = 0

    def setTeam(self, team):
        self.team = team
        self.isdirty = 1
    

class Tournament:
    def __init__(self, tourneyTeams):
        self.numSeeds = len(tourneyTeams)
        self.tourneyRounds = int(math.ceil(math.log(self.numSeeds, 2)))
        self.numByes = pow(2, self.tourneyRounds) - self.numSeeds
        self.roundTeams = [[] for r in range(self.tourneyRounds + 1)]
        self.tourneyTeams = tourneyTeams
        self.seedorder = SingleEliminationSeeds(self.numSeeds).getSeedOrder()
                
    def cmpSeeds(self, s1, s2): return cmp(s1.getSeed(), s2.getSeed())
    def setupTree(self):
        self.tree = self.buildTree(self.tourneyRounds)
        self.buildFirstRoundNodes()

    def buildFirstRoundNodes(self):
        byeFlag = False
        seedCount = 0
        # Sort seeds in ascending order
        self.tourneyTeams.sort(self.cmpSeeds)
        currParentIdx = 0
        for seed in range(0, len(self.seedorder), 2):
            currParentNode = self.roundTeams[2][currParentIdx]
            highseed, lowseed = self.seedorder[seed], self.seedorder[seed + 1]
            highnode = Node()
            highnode.setTeam(self.getTeam(highseed))
            self.roundTeams[0].append(highnode)
            if lowseed > 0:
                lownode = Node()
                lownode.setTeam(self.getTeam(lowseed))
                self.roundTeams[0].append(lownode)                
                firstRoundNode = Node()
                firstRoundNode.parent = currParentNode
                firstRoundNode.left = highnode
                firstRoundNode.right = lownode
                highnode.parent = firstRoundNode
                lownode.parent = firstRoundNode
                self.roundTeams[1].append(firstRoundNode)
                byeFlag = False
                if seedCount % 2:
                    # low seed for the second round node
                    # This individual node has been "filled"
                    currParentNode.right = firstRoundNode
                    currParentIdx += 1
                else:
                    currParentNode.left = firstRoundNode
            else:
                if not byeFlag:
                    currParentNode.left = highnode
                    byeFlag = True
                else:
                    currParentNode.right = highnode
                    byeFlag = False
                    currParentIdx += 1
                    
                highnode.parent = currParentNode
            seedCount += 1

                
    def getTeam(self, seed):
        return self.tourneyTeams[seed - 1]
    
    def buildTree(self, level):
        node = Node()
        if level != 2:
            node.left = self.buildTree(level - 1)
            node.left.parent = node
            node.right = self.buildTree(level - 1)
            node.right.parent = node

        self.roundTeams[level].append(node)    

        return node
    
    def getRoundNodes(self, level):
        teams = []
        # Special case the first round
        if level == 1:            
            nodes = self.roundTeams[0]
            firstRoundNodes = self.roundTeams[1]
            for node in nodes:
                inFirstRound = 0
                for frnode in firstRoundNodes:
                    if node.parent == frnode:
                        teams.append(node)
                        inFirstRound = 1
                        break

                if not inFirstRound:
                        teams.append(node)
                        teams.append(None)
                        
            return teams
        else:
            return self.roundTeams[level]
        
    def getMatches(self, level):
        matchlist = []
        for i in range(len(self.roundTeams[level])):
            team1Node = self.roundTeams[level][i].left
            team2Node = self.roundTeams[level][i].right
                
            if not team1Node.team and team1Node.isdirty and team2Node.team:
                team2Node.parent.setTeam(team2Node.team)
            elif not team2Node.team and team2Node.isdirty and team1Node.team:
                team1Node.parent.setTeam(team1Node.team)

            matchlist.append((team1Node, team2Node))
 
        return matchlist    

class TournamentManager:
    def __init__(self, teams, tourney_name="Tournament", prefs=None):
        self.matchPrefs = prefs
        self.tourney = Tournament(teams)
        self.tourney.setupTree()
        self.currentRound = 1
        tourneyRounds = self.tourney.tourneyRounds
        self.tourneyTable = []
        self._buildTourneyTable(pow(2, tourneyRounds))
        self.name = tourney_name
        self.currentMatches = self.tourney.getMatches(1)
        # The index of the current in the currentMatches list
        self.currentMatch = None
        self.interactive = True
        self.winner = None
        self.finished = 0

    def setPrefs(self, prefs):
        self.matchPrefs = prefs

    def hasPrefs(self):
        return self.matchPrefs != None
    
    def _buildTourneyTable(self, size):
        if not size: return
        col = []
        for row in range(size):
            col.append('<BR>')
        self.tourneyTable.append(col)
        return self._buildTourneyTable(size/2)
            
    def getTourneyName(self): return self.name

    def getRoundString(self):
        """Return round name"""
        round = self.currentRound
        roundStr = "Round %d" % round
        if round == self.tourney.tourneyRounds - 2 and \
               self.tourney.tourneyRounds > 3:
            roundStr = "Quaterfinals"
        elif round == self.tourney.tourneyRounds - 1 and \
                 self.tourney.tourneyRounds > 2:
            roundStr = "Semifinals"
        elif round == self.tourney.tourneyRounds:
            roundStr = "Finals"

        return roundStr

    def getMatchStrings(self):
        """Return the match strings for the remaining matches in the current
           round"""
        matchStrings = []
        for team1, team2 in self.currentMatches:
            t1 = team1.team
            t2 = team2.team
            if not t1 or not t2: continue
            
            team1Str = self._getTeamString(t1.getData())
            team2Str = self._getTeamString(t2.getData())
            matchStrings.append("#%d %s vs. #%d %s" % (t1.getSeed(), team1Str,
                                                       t2.getSeed(), team2Str))
        return matchStrings
                                
    def getTeamsForMatch(self, idx):
        teams = [[], []]
        t1, t2 = self.currentMatches[idx]
        teams[0] = [teamMod for teamMod in t1.team.getData()]
        teams[1] = [teamMod for teamMod in t2.team.getData()]
        return teams
        
    def getTourneyRounds(self): return self.tourney.tourneyRounds

    def getTourneyTable(self):
        for roundnum in range(self.currentRound, self.currentRound + 3):
            if roundnum <= self.getTourneyRounds():
                nodes = self.tourney.getRoundNodes(roundnum)
                teams = self._getRoundTeams(nodes)
                self._updateTourneyTable(roundnum - 1, teams)

        if self.winner:
            winner = self.winner.getData()
            self.tourneyTable[-1][0] = self._getTeamString(winner)
            self.finished = 1

        return self.tourneyTable

    def _updateTourneyTable(self, roundnum, teams):
        teamidx = 0
        for team in teams:
            if team:
                seednum = 0
                if roundnum == 0:
                    seednum = team.getSeed()
                teamStr = self._getTeamString(team.getData(), seednum)
                self.tourneyTable[roundnum][teamidx] = teamStr

            teamidx += 1                       
                            
    def _getTeamString(self, teamdata, seednum=0):
        teamStr = ""
        if seednum:
            teamStr = " (%d) " % seednum
        for teamMod in teamdata:
            teamStr += "%s, " % teamMod.name
        return teamStr[:-2]

    def _getRoundTeams(self, roundnodes):
        teams = []
        for node in roundnodes:
            # Could possibly be a list of leaf nodes from the first round
            if not node:
                teams.append(None)
            elif not node.left and not node.right:
                teams.append(node.team)
            else:
                teams.append(node.left.team)
                teams.append(node.right.team)

        return teams
    
    def setCurrentMatch(self, idx):
        self.currentMatchIdx = idx

    def setWinner(self, teamidx):
        """Tells the tourney manager which team won the current match"""
        currMatch = self.currentMatches[self.currentMatchIdx]
        if teamidx < 0:
            currMatch[0].parent.setTeam(None)
        else:
            currMatch[teamidx].parent.setTeam(currMatch[teamidx].team)
        self.currentMatches.pop(self.currentMatchIdx)
        if len(self.currentMatches) < 1:
            if self.currentRound == self.tourney.tourneyRounds:
                self.winner = currMatch[teamidx].team
                return
            self.currentRound += 1
            self.currentMatches = self.tourney.getMatches(self.currentRound)
            # Remove any matches where there are 1 or less opponents
            self.currentMatches = [m for m in self.currentMatches \
                                   if m[0].team and m[1].team]
            
            
    def getWinner(self): return self.winner
    def isFinished(self): return self.finished
    def setInteractive(self, isInteractive=True):
        self.interactive = isInteractive
        
    def isInteractive(self): return self.interactive
    def isSemiFinalOrFinal(self):
        """Let caller know if this is a two round tournament or the tournament
           is in the semifinal or final round"""
        return self.tourney.tourneyRounds == 2 or self.getRoundString() \
               in ["Semifinals", "Finals"]
        
if __name__ == '__main__':
    class d:
        def __init__(self, n): self.name = n
    tlist = []    
    for t in range(1, 4):
        tlist.append(Team([d("Name%d" % t)], t))
    m = TournamentManager(tlist)
    while not m.isFinished():
        print m.getMatchStrings()
        print m.getTourneyTable()
        print "Is semifinal or final:", m.isSemiFinalOrFinal()
        if not m.isFinished():
            m.setCurrentMatch(0)        
            m.setWinner(random.randint(0,1))
            
                    
    print m.getWinner().getData()[0].name

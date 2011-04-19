from lib import Interface
from lib.util import getModules, JOWST_PATH
from lib import spw

class GuiTester:
    def __init__(self, testCB):
        self.testCB = testCB
        self.wrestlerFiles = getModules("Wrestlers")
        self.numWrestlers = len(self.wrestlerFiles)
        self._exceptions = ["E:\\pws\\Wrestlers\\TestAndreTheGiant.py",
                            "E:\\pws\\Wrestlers\\TestAndreTheGiant.pyc",
                            "E:\\pws\\Wrestlers\\TestHulkHogan.py",
                            "E:\\pws\\Wrestlers\\TestHulkHogan.pyc"]
        self.buildTests()
        

    def buildTests(self, numWrestlersToTest=None):
        self.tests = []
        idx = 0
        for file in self.wrestlerFiles:
            wrestler = self.wrestlerFiles[file]
            if file in self._exceptions: continue

            # Singles Match Test
            self.tests.append(([wrestler], [wrestler]))
            #self.tests.append(([self.wrestlerFiles["F:\\pws\\Wrestlers\\RoadWarrior_Hawk.py"]], [self.wrestlerFiles["F:\\pws\\Wrestlers\\RoadWarrior_Animal.py"]]))

            # Tag Match Test
            #team1 = [wrestler, self.getMate(idx+1, wrestler)]
            #team2 = [team1[0], team1[1]]
            #self.tests.append((team1, team2))

            # Six Man Match Test
            #team1 = self.getTwoMates(idx+1, wrestler, [wrestler])
            #team2 = [team1[2], team1[0], team1[1]]
            #self.tests.append((team1, team2))

            idx += 1

    def runMatch(self, teams, dq=0, timelimit=30):
        t1 = spw.getTeamList(teams[0], 0)
        t2 = spw.getTeamList(teams[1], 1)
        matches = getModules("Matches")
        for match in matches:
            if matches[match].name == "Boot Camp":
                m = matches[match]
        match = m.SpecialtyMatch
        #match = spw.Match
        m = match(t1, t2, dqEnabled=dq, timeLimit=timelimit)
        m.useStrategyPinChart(1)
        from lib.Interface import DramaQueen
        d = DramaQueen(0,0,0,0)
        self.testCB(m, d)

    def run(self):
        self.runTest()

    def next(self):
        self.runTest()
        
    def runTest(self):
        self.runMatch(self.tests.pop(0))

    def hasMoreTests(self): return len(self.tests)
    
    def getMate(self, startidx, wrestler):
        files = self.wrestlerFiles.keys()
        files = files[startidx:]
        for fname in files:
            if fname in self._exceptions: continue
            mate = self.wrestlerFiles[fname]
            if mate.name != wrestler.name:
                return mate
        return self.getMate(0, wrestler)            

    def getTwoMates(self, startidx, wrestler, teamlist):
        files = self.wrestlerFiles.keys()
        files = files[startidx:]        
        for fname in files:
            if fname in self._exceptions: continue
            mate = self.wrestlerFiles[fname]
            if mate.name != wrestler.name:
                teamlist.append(mate)
                if len(teamlist) == 3:
                    return teamlist
        return self.getTwoMates(0, teamlist[-1], teamlist)            
                    
                
        
        
        

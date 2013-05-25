import os, shelve, datetime, re, glob
from lib import util
from data.globalConstants import *

class BaseDB:
    def __init__(self, path):
        self.filename = path
        self.db = None

        if not os.path.exists(path):
            self._openDB('c')
            self._closeDB()

    def save(self, records=None):
        self._openDB('w')
        if records:
            for key, value in records:
                self.db[key] = value
        self.db.sync()
        self._closeDB()

    def newRecord(self, key, record):
        self._openDB('w')
        self.db[key] = record
        self.save()
        
    def getKeys(self):
        self._openDB()
        keys = self.db.keys()
        self._closeDB()
        keys.sort()
        return keys

    def getRecord(self, key):
        self._openDB()
        record = self.db.get(key, {})
        self._closeDB()
        return record

    def getKeysNotInDB(self, keys):
        dbKeys = set(self.db.keys())
        keys = set(keys)
        return list(keys - dbKeys)

    def getNewKey(self):
        keys = self.getKeys()
        return str(int(keys[-1]) + 1)
        

    def _openDB(self, flag='r'):
        if not self.db:
            self.db = shelve.open(self.filename, flag)

    def _closeDB(self):
       self.db.close()
       self.db = None


"""
Results = {wrestlerFilename:
           {
           "NAME":wrestlerName,
           "WINS":[{"OPPONENT": wretlerFilename1, "ARB_DATA":data1},
                     {...}],
           "LOSSES":[{"OPPONENT": wretlerFilename1, "ARB_DATA":data1},
                     {...}]}}
           "DRAWS":[{"OPPONENT": wretlerFilename1, "ARB_DATA":data1},
                     {...}]}}

           data1 is a dictionary containing arbitrary data
           related to the match
"""
class ResultManager(BaseDB):
    def __init__(self, path, name):
        relpath = path
        path = os.path.normpath(os.path.join(util.JOWST_PATH, relpath))
        if not os.path.exists(path):
            try:
                util.updateDataRegistry(name, relpath, "resultsRegistry")
            except:
                raise OSError
            
        BaseDB.__init__(self, path)
        self.name = name
        self.path = path

    def getNewKey(self): pass

    def hasRecord(self, filename):
        return len(self.getRecord(filename))

    def createRecord(self, key, name):
        self.newRecord(key, {"NAME":name, "WINS":[], "LOSSES":[],
                             "DRAWS":[]})

    def getKeys(self):
        keys = BaseDB.getKeys(self)
        badkeys = []
        for key in keys:
            currKey = key
            if currKey in badkeys: continue
            for cmpkey in keys:
                if currKey != cmpkey:
                    if self.keysOutOfOrder(currKey, cmpkey):
                        print "keys out of order getKeys() %s %s\n\n"\
                              % (currKey, cmpkey)
                        badkeys.append(cmpkey)
        for key in badkeys:
            keys.remove(key)
            
        return keys
    
    def getRecord(self, key):
        keys = BaseDB.getKeys(self)
        record = BaseDB.getRecord(self, key)
        for dbkey in keys:
            if key != dbkey:
                if self.keysOutOfOrder(key, dbkey):
                    print "keys out of order getRecord() %s %s\n\n" % (key,
                                                                       dbkey)
                    record = self.mergeRecords(record, dbkey)
        return record

    def keysOutOfOrder(self, key1, key2):
        k1split = key1.split(';')
        k2split = key2.split(';')
        if len(k1split) != len(k2split):
            return 0

        srcnames = self._getBaseNames(k1split)
        destnames = self._getBaseNames(k2split)
        numMatches = 0
        for name in srcnames:
            if name in destnames:
                numMatches += 1

        return numMatches == len(k1split)

    def mergeRecords(self, record, key2):
        r2 = BaseDB.getRecord(self, key2)
        record["WINS"] += r2["WINS"]
        record["LOSSES"] += r2["LOSSES"]
        record["DRAWS"] += r2["DRAWS"]
        return record
        
        
    def _getBaseNames(self, paths):
        basenames = []
        for path in paths:
            basenames.append(os.path.basename(path))
        return basenames
    
    def updateResults(self, winner_filename, winnername, loser_filename,
                      losername, data, isdraw=0):

        for key, name in [(winner_filename, winnername),
                          (loser_filename, losername)]:
            if not self.hasRecord(key):
                self.createRecord(key, name)

        records = []
        recordCol1, recordCol2 = "WINS", "LOSSES"
        if isdraw:
            recordCol1, recordCol2 = "DRAWS", "DRAWS"
        
        records.append((winner_filename,
                        self.updateResult(winner_filename, loser_filename,
                                         recordCol1, data)))
        records.append((loser_filename,
                        self.updateResult(loser_filename, winner_filename,
                                         recordCol2, data)))
        self.save(records)

    def updateResult(self, key, opponent, resulttype, data):
        record = self.getRecord(key)
        record[resulttype].append({"OPPONENT":opponent, "ARB_DATA":data})
        return record
    
    def getNumLosses(self, filename):
        return len(self.getRecord(filename)["LOSSES"])

    def getNumWins(self, filename):
        return len(self.getRecord(filename)["WINS"])

    def getNumDraws(self, filename):
        return len(self.getRecord(filename)["DRAWS"])

    def getResults(self, filename, columns, sortby="DATE"):
        """Put all result data into a tabular format"""
        if sortby not in columns: sortby=""
        record = self.getRecord(filename)

        rows = []
        sortidx = -1
        for key, result in (("WINS", "WIN"), ("LOSSES", "LOSS"),
                       ("DRAWS", "DRAW")):
            data = record[key]
            for item in data:
                row = []
                colidx = 0
                for col in columns:
                    if col == sortby: sortidx = colidx
                    
                    if col == "OPPONENT":
                        opponentName = self.getRecord(item["OPPONENT"])["NAME"]
                        row.append(opponentName)
                    elif col == "RESULT":
                        row.append(result)
                    else:
                        row.append(item["ARB_DATA"][col])
                    colidx += 1
                rows.append(row)

        if sortidx > -1:
            return RecordSorter(rows, sortidx).getResult()
        else:
            return rows

    def getWrestlerDictAndList(self, teamsize=1):
        wrestlerList = []
        wrestlers = util.getWrestlerModules()
        keys = self.getKeys()
        for key in keys:
            team = key.split(';')
            if len(team) == teamsize:
                if len(team) > 1:
                    nameSet = "("
                else:
                    nameSet = ""
                for man in team:
                    wrestler = wrestlers.get(man)
                    if not wrestler:
                        nameSet += "DELETED"
                        if len(team) > 1:
                            nameSet += ", "
                        continue
                    if hasattr(wrestler, "nameSet"):
                        nameSet += wrestler.nameSet
                        if len(team) > 1:
                            nameSet += ", "
                if len(team) > 1:
                    nameSet = "%s)" % nameSet[:-2]
                name = self.getRecord(key)["NAME"]
                wrestlerList.append((name, nameSet, key))
        return wrestlers, wrestlerList
                
class RecordSorter:
    def __init__(self, records, sortindex):
        self.sortindex = sortindex
        self.dateFormat = re.compile("(\d+)/(\d+)/(\d+)")
        records.sort(self._sorter)
        self.result = records

    def getResult(self): return self.result
    
    def _sorter(self, rec1, rec2):
        item1 = rec1[self.sortindex]
        item2 = rec2[self.sortindex]

        dateMatch1 = self.dateFormat.match(str(item1))
        dateMatch2 = self.dateFormat.match(str(item2))
        if dateMatch1 and dateMatch2:
            item1 = datetime.date(int(dateMatch1.group(3)),
                                  int(dateMatch1.group(1)),
                                  int(dateMatch1.group(2)))
            item2 = datetime.date(int(dateMatch2.group(3)),
                                  int(dateMatch2.group(1)),
                                  int(dateMatch2.group(2)))
        return cmp(item1, item2)


def getNewDb(name):
    return ResultManager(getNewDbPath(name), name)

def getNewDbPath(name):
    datapath = os.path.join(util.JOWST_PATH, "db")
    resultDBs = glob.glob(os.path.join(datapath, "result*.db"))
    dbPattern = re.compile(".*result(\d+)\.db$")
    dbnum = 0
    for db in resultDBs:
        dbmatch = dbPattern.match(db)
        if dbmatch:
            if int(dbmatch.group(1)) > dbnum:
                dbnum = int(dbmatch.group(1))
    return os.path.join("db", "result%d.db" % (dbnum + 1))

def getDb(path, name):
    if not path:
        return getNewDb(name)
    return ResultManager(path, name)

def joinWrestlerDir(filename):
    return os.path.join(util.JOWST_PATH, "Wrestlers", filename)

class WrestlerDB(BaseDB):
    def __init__(self):
        BaseDB.__init__(self, joinWrestlerDir("wrestlers.db"))
        wrestlerFiles = glob.glob(joinWrestlerDir("*.py"))
        basenames = [os.path.basename(f) for f in wrestlerFiles]
        
        self._openDB('c')

        # If there were new wrestlers added to the "Wrestlers" directory
        # since the last time we opened the db, add them to the db here.
        newFiles = self.getKeysNotInDB(basenames)
        mods = {}
        for newFile in newFiles:
            mod = util.getWrestlerModule(newFile)
            if mod:
                   self.db[newFile] = {
                       "NAME": mod.name,
                       "NAMESET": getattr(mod, "nameSet", ""),
                       "MTIME": os.stat(joinWrestlerDir(newFile)).st_mtime
                   }
                
        # If any of the wrestlers have been modified since the last time
        # we opened the db then update the wrestlers' records in the db.
        for filename in self.db:
            record = self.db.get(filename, {})
            fileMtime = os.stat(joinWrestlerDir(filename)).st_mtime
            if record and record.get("MTIME", -1) < fileMtime:
                mod = util.getWrestlerModule(filename)
                if mod:
                    # Wrestler may have changed since the last time we
                    # opened the db so we reload the wrestler module.
                    reload(mod)
                    record["NAME"] = mod.name
                    record["NAMESET"] = getattr(mod, "nameSet", "")
                    record["MTIME"] = fileMtime
                    self.db[filename] = record

        self.save()

def getWrestlerData():
    db = WrestlerDB()

    class WrestlerData:
        def __init__(self, name, nameSet, path):
            self.name = name
            self.nameSet = nameSet
            self.path = joinWrestlerDir(path)
            
    data = {}
    for filename in db.getKeys():
        record = db.getRecord(filename)
        data[filename] = WrestlerData(record["NAME"],
                                      record["NAMESET"],
                                      filename)

    return data

def getWrestlerDictAndList(filenames=1):
    wrestlerInfo = []
    idx = 0
    wrestlerDict = getWrestlerData()
    for wrestlerFilename in wrestlerDict:
        wrestler = wrestlerDict[wrestlerFilename]
        if not hasattr(wrestler, "nameSet"):
            nameSet = ""
        else:
            nameSet = wrestler.nameSet
        key = wrestlerFilename
        if not filenames:
            key = str(idx)            
        wrestlerInfo.append((wrestler.name, nameSet, key))
        idx += 1

    return wrestlerDict, wrestlerInfo

                    
if __name__ == '__main__':
    path = "test.db"
    if os.path.exists(path): os.unlink(path)
    db = ResultManager(path)

    winnerkey = "TheWinnerKey"
    winner = "The Winner"

    loserkey = "TheLoserKey"
    loser = "The Loser"

    data = {"DATE":"4/1/2004"}
    db.updateResults(winnerkey, winner, loserkey, loser, data)
    data = {"DATE":"1/1/2000"}
    db.updateResults(loserkey, loser, winnerkey, winner, data)
    data = {"DATE":"12/31/2005"}
    db.updateResults(loserkey, loser, winnerkey, winner, data, isdraw=1)
    print db.getResults(winnerkey, ["DATE", "OPPONENT", "RESULT"])
    print db.getResults(loserkey, ["DATE", "OPPONENT", "RESULT"])
  
  
        
        
        
        
        
        
        
    
    
        
        

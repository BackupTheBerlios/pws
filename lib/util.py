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

import math, random, glob, os, sys, pprint, shutil

from data.globalConstants import *
import pwsconfig

if hasattr("pwsconfig", "JOWST_PATH"):
    JOWST_PATH = pwsconfig.JOWST_PATH
else:
    JOWST_PATH = os.path.normpath(os.path.dirname(pwsconfig.__file__))

def convertFromString(cardStr):
    strMap = {
        "A":A,
        "B":B,
        "C":C,
        "REVERSE":REVERSE,
        "OC":OC,
        "DC":DC,
        "OC/TT":OCTT,
        "P/A":PA,
        "*":SUBMISSION,
        "(DQ)":DQ,
        "(XX)":XX,
        "(S)":SPECIALTY}

    if cardStr in strMap.keys():
        retval = strMap[cardStr]
    else:
        retval = None

    return retval
    
def convertToString(cardVal):
    strMap = {
        A:"A",
        B:"B",
        C:"C",
        REVERSE:"REVERSE",
        OC:"OC",
        DC:"DC",
        OCTT:"OC/TT",
        PA:"P/A",
        SUBMISSION:'*',
        DQ:"(DQ)",
        XX:"(XX)",
        SPECIALTY:"(S)"}

    if cardVal in strMap.keys():
        retStr = strMap[cardVal]
    else:
        retStr = ""

    return retStr

def convertRangeTupleToString(t):
    if len(t) < 2:
        rngStr = str(t[0])
    else:
        rngStr = "%s - %s" % (str(t[0]), str(t[-1]))

    return rngStr

def convertPriorityToString(pri):
    if pri % 1 > 0:
        priStr = "%s+" % int(pri)
    else:
        priStr = str(pri)

    return priStr

def convertMoveToString(m):
    strMoves = getMoveStringDict(m)
    moveName = strMoves.get("MOVE_NAME", "")
    moveType = strMoves.get("MOVE_TYPE", "")
    movePoints = strMoves.get("MOVE_POINTS", "")

    return "%s %s %s" % (moveName, movePoints, moveType)

def getMoveStringDict(m):
    moveName = m["MOVE_NAME"]
    moveType = convertToString(m["MOVE_TYPE"])
    movePoints = str(m.get("MOVE_POINTS", ""))

    if moveType == "(S)":
        moveDict = {"MOVE_NAME":moveName, "MOVE_TYPE":moveType}
        if movePoints:
            moveDict["MOVE_POINTS"] = movePoints
    elif moveName == "ROPES":
        moveDict = {"MOVE_NAME":"ROPES"}
    elif moveName == "NA":
        moveDict = {"MOVE_NAME":"NA"}
    elif moveType == "(DQ)":
        moveDict = {"MOVE_NAME":moveName, "MOVE_TYPE":moveType}
    else:
        movePoints = str(m["MOVE_POINTS"])
        moveDict = {"MOVE_NAME":moveName, "MOVE_POINTS":movePoints,
                    "MOVE_TYPE":moveType}
    return moveDict

def isNonMoveString(strVal):
    validNonMoves = ("OC", "DC", "OC/TT", "A", "B", "C", "REVERSE")
    return (strVal in validNonMoves) 

def stringifyModifier(val):
    if val > 0: modstr = "+%d" % val
    else: modstr = str(val)
    return modstr

def layoutPinAttemptDialog(prompt, datatable, pinner):
    layout = []
    layout.append((prompt, HEADING, 3))
    pinnerScore = str(datatable.pop("ELIGIBLE_MAN_SCORE"))
    layout.append(("<FONT SIZE=+1>", LINE, None))
    layout.append(("%s's Score: %s<BR>" %(pinner, pinnerScore),
                   LINE, 0))
    layout.append(("Opponent's Score: %s<BR>" % \
                   str(datatable.pop("VICTIM_SCORE")), LINE, 0))    
    refmod = stringifyModifier(datatable.pop("REF_MODIFIER"))
    layout.append(("Referee Modifier: %s<BR>" % refmod, LINE, 0))
    pinmod = stringifyModifier(datatable.pop("PIN_MODIFIER"))
    layout.append(("Pin Modifier: %s<BR>" % pinmod, LINE, 0))
    layout.append(("</FONT><BR>", LINE, 0))

    pinprob = datatable.pop("PIN_PROBABILITY")

    tableCols = ["Result", "Probability"]
    tableRows = []

    # Reverse probabilities
    rstar = datatable.pop("REVERSE*_PROBABILITY", None)
    if rstar:
        tableRows.append(("REVERSE*", "%.1f%%" % rstar))
    rprob = datatable.pop("REVERSE_PROBABILITY", None)
    if rprob:
        tableRows.append(("REVERSE", "%.1f%%" % rprob))

    # Numeric result probabilities - these are all that should be left in the
    # datatable
    numericProbs = datatable.items()
    numericProbs.sort()
    for item in numericProbs:
        tableRows.append((stringifyModifier(item[0]), "%.1f%%" % item[1]))

    # Pin Probability
    tableRows.append(("PIN", "%.1f%%" % pinprob))

    layout.append({"COLUMNS":tableCols, "ROWS":tableRows})
    layout.append(("<BR><BR>", LINE, None))

    return layout                         
    
def formatTeamKey(team):
    teamKeys = []
    for member in team:
        teamKeys.append("%s" % member.getFileName())
    teamKeys.sort()
    
    return ";".join(teamKeys)

def updateDataRegistry(key, value, dictname, removeitem=0):
    from db import dataRegistry
    dicts = []
    pp = pprint.PrettyPrinter(indent=4)

    for attr in ["resultsRegistry", "championsRegistry"]:
        attrVal = getattr(dataRegistry, attr)
        if attr == dictname:
            if removeitem:
                attrVal.pop(key)
            else:
                attrVal[key] = value
        dicts.append("%s = %s\n" % (attr, pp.pformat(attrVal)))
    filepath = os.path.join(JOWST_PATH, "db", "dataRegistry.py")
    shutil.copyfile(filepath, "%s.bak" % filepath)

    try:
        datafile = open(filepath, 'w')
        filestr = ""
        for attrStr in dicts:
            filestr += attrStr

        datafile.write(filestr)

        datafile.close()
        os.unlink("%s.bak" % filepath)        
    except:
        shutil.copyfile("%s.bak" % filepath, filepath)
        raise 


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

def getWrestlerModule(path):
    try:
        filename = os.path.splitext(os.path.basename(path))[0]
        mods = __import__("Wrestlers", globals(), locals(), [filename])
        mod = getattr(mods, filename)
        name = getattr(mod, "name", None)
        if name:
            return mod
    except:
        print "Could not load", filename

    return None

def getMatchModules(): return getModules("Matches")
def getWrestlerModules(): return getModules("Wrestlers")

def getModules(pkgName):
    modmap = {}
    jpath = os.path.normpath(JOWST_PATH)
    dirFiles = glob.glob(os.path.join(jpath, pkgName, "*.py"))
    filenames = []
    for dirFile in dirFiles:
        filenames.append(os.path.splitext(os.path.basename(dirFile))[0])

    pkgMods = {}
    for filename in filenames:
        try:
            mod = __import__(pkgName, globals(), locals(), [filename])
            pkgMods[filename] = getattr(mod, filename)
        except:
            print "Could not load", filename
    
    for mod in pkgMods.keys():
        modObj = pkgMods[mod]
        if hasattr(modObj, "name"):
            reload(modObj)
            filename = "%s.py" % os.path.splitext(modObj.__file__)[0]
            filename = os.path.normpath(os.path.abspath(filename))
            modmap[filename] = modObj
    return modmap

def makeGoodFilename(filename):
    return os.path.normpath(os.path.abspath("%s.py" % os.path.splitext(filename)[0]))

def generateRandomPassword():
    """Original Author: Will Ware (wware@alum.mit.edu)
       See: http://groups.google.com/groups?hl=en&lr=&ie=UTF-8&oe=UTF-8&selm=3B8B0698.5070703%40alum.mit.edu"""
    
    units = "ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"
    units = units + """!@#$%^&*+=;:,.""" # Compensate with punctuation.
    separator = ""
    pw = ""
    
    for i in range(10):
        pw = pw + random.choice(units) + separator

    return pw

from wxPython.wx import wxIcon, wxBITMAP_TYPE_ICO
def setIcon(frame):
    if sys.platform == "win32":
        frame.SetIcon(wxIcon("resources/pws.ico", wxBITMAP_TYPE_ICO))
        
def cmpNames(w1, w2): return cmp(w1.name, w2.name)

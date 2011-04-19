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

import pprint
from lib.util import *
from data.globalConstants import *


class WrestlerBuilder:
    def __init__(self):
        self.name          = ''
        self.generalCard   = [OC] * 11
        self.gcDefs = (("1000","OC"), ("1001", "OC/TT"), ("1002", "DC"))

        self.offensiveCard = self._listOfDicts(11)
        self.ocDefs = (("1003", "Pin attempt move (P/A)"),
                       ("1004", "Submission Move (*)"),
                       ("1005", "Specialty Move (S)"),
                       ("1006", "Disqualification Move (DQ)"),
                       ("1008", "Regular Offensive Move"),
                       ("1009", "Grudge Match Move (XX)"),
                       ("1010", "Ropes Move (ROPES)"))

        self.defensiveCard = [A] * 11
        self.dcDefs = (("0", "B - No points on defense"),
                       ("2", "A - 2 points on defense"),
                       ("4", "C - 4 points on defense and neutralize offensive move"),
                       ("5", "Reverse - Reverse offensive move"))

        self.specialtyCard = {}
        self.specDefs = (("1003", "Pin attempt move (P/A)"),
                         ("1004", "Submission Move (*)"),
                         ("1005", "Specialty Move (S)"),
                         ("1006", "Disqualification Move (DQ)"))

        self.ropesCard = self._listOfDicts(11)
        self.ropesDefs = (("1003", "Pin attempt move (P/A)"),
                          ("1004", "Submission Move (*)"),
                          ("1005", "Specialty Move (S)"),
                          ("1006", "Disqualification Move (DQ)"),
                          ("1008", "Regular Offensive Move"),
                          ("1009", "Grudge Match Move (XX)"),
                          ("1010", "Ropes Move (ROPES)"), ("1014", "No Action (NA)"))
        
        self.subMin        = '2'
        self.subMax        = '2'
        self.tagTeamMin    = '2'
        self.tagTeamMax    = '2'
        self.priSingles    = '1'
        self.priTagTeam    = '1'
        self.nameSet       = ""
        self.comments      = ""
        
        self.pp = pprint.PrettyPrinter(indent=4)

        # Build set/get attribute functions
        wbAttrs = ("name", "subMin", "subMax", "tagTeamMin", "tagTeamMax",
                   "priSingles", "priTagTeam", "nameSet", "comments")
        for attr in wbAttrs:
            newattr = attr[0].upper() + attr[1:] # Make first letter of attr uppercase
            setattr(self, "set"+newattr, lambda x, y=attr: setattr(self, y, x))
            setattr(self, "get"+newattr, lambda y=attr: getattr(self, y))

    # When init'ing a list of empty dictionaries, the dicts are all pointing
    #  to the same memory address.  This function returns a list of empty
    #  dictionaries.
    def _listOfDicts(self, numDicts):
        dictList = []
        for n in range(numDicts):
            dictList.append({})

        return dictList
    
    def addToGeneralCard(self, idx, gcitem):
        val = convertFromString(gcitem)
        if val not in (OC, OCTT, DC): return 0
        self.generalCard[idx] = val
        return 1

    def addToOffensiveCard(self, idx, moveName, movePoints='', moveType=''):
        moveTypeVal = convertFromString(moveType)
        if not moveTypeVal:
            if moveName == "ROPES": moveTypeVal = ROPES
            else: moveTypeVal = OFFENSIVE
        
        self.offensiveCard[idx]["MOVE_NAME"] = moveName
        if movePoints:
            self.offensiveCard[idx]["MOVE_POINTS"] = int(movePoints)

        self.offensiveCard[idx]["MOVE_TYPE"] = moveTypeVal

    def addToDefensiveCard(self, idx, dcItem):
        val = convertFromString(dcItem)
        if val not in (A, B, C, REVERSE): return 0
        self.defensiveCard[idx] = val

    def setSpecialty(self, name):
        self.specialtyCard[name] = self._listOfDicts(6)
        
    def addToSpecialtyCard(self, idx, movePoints='', moveType=''):
        moveTypeVal = convertFromString(moveType)
        if not moveTypeVal: moveTypeVal = SPECIALTY
        specName = self.specialtyCard.keys()[0]
        if movePoints:
            self.specialtyCard[specName][idx]["MOVE_POINTS"] = int(movePoints)
        self.specialtyCard[specName][idx]["MOVE_TYPE"] = moveTypeVal

    def addToRopesCard(self, idx, moveName, movePoints='', moveType=''):
        moveTypeVal = convertFromString(moveType)
        if not moveTypeVal:
            if moveName == "NA": moveTypeVal = NA
            else: moveTypeVal = OFFENSIVE

        self.ropesCard[idx]["MOVE_NAME"] = moveName
        if movePoints:
            self.ropesCard[idx]["MOVE_POINTS"] = int(movePoints)

        self.ropesCard[idx]["MOVE_TYPE"] = moveTypeVal

    def writeToFile(self, filename):
        """This function will write out the wrestler module to the
           location specified by filename."""
        fileModule = open(filename, 'w')
        fileModule.write(self._buildFile())
        fileModule.close()
    
    def dump(self):
        print self._buildFile()
        
    def _buildFile(self):
        fileStr = "from data.globalConstants import *\n# %s\n" % self.name
        fileStr += "name = %s\n" % self.pp.pformat(self.name)
        fileStr += "\n# General Card Definitions: \n%s" % \
                   self._processDefs(self.gcDefs)
        fileStr += "GeneralCard = %s\n\n" % self.pp.pformat(self.generalCard)
        fileStr += "# Offensive Card Definitions:\n%s" % \
                   self._processDefs(self.ocDefs)
        fileStr += "OffensiveCard = \\\n%s\n\n" % \
                   self.pp.pformat(self.offensiveCard)
        fileStr += "# Defensive Card Definitions:\n%s" % \
                   self._processDefs(self.dcDefs)
        fileStr += "DefensiveCard = %s\n\n" % \
                   self.pp.pformat(self.defensiveCard)
        fileStr += "# Specialty Card Definitions:\n%s" % \
                   self._processDefs(self.specDefs)
        fileStr += "Specialty = %s\n\n" % self.pp.pformat(self.specialtyCard)
        fileStr += "# Ropes Card Definitions:\n%s" % \
                   self._processDefs(self.ropesDefs)
        fileStr += "Ropes = \\\n%s\n\n" % self.pp.pformat(self.ropesCard)

        fileStr += "Sub = %s\n" % self._getStrTuple(self.subMin,
                                                    self.subMax)
        fileStr += "TagTeam = %s\n" % self._getStrTuple(self.tagTeamMin,
                                                        self.tagTeamMax)
        fileStr += "Priority = (%s, %s)\n" % (self.priSingles,
                                              self.priTagTeam)
        fileStr += "nameSet = %s\n" % self.pp.pformat(self.nameSet)

        return fileStr

    def _getStrTuple(self, str_minval, str_maxval):
        try:
            if int(str_minval) < int(str_maxval):
                strTuple = "(%s, %s)" % (str_minval, str_maxval)
            else:
                strTuple = "(%s, )" % str_minval
        except ValueError:
            strTuple = "(0, )"

        return strTuple
        
    def _processDefs(self, cardDefs):
        defStr = ""
        for val, definition in cardDefs:
            defStr += "#    %s = %s\n" % (val, definition)

        return defStr
            
if __name__ == '__main__':
    """The following is a script to build a wrestler"""
    idx = 0
    wb = WrestlerBuilder()
    wb.setName("Joe Jobber")

    for gcItem in ("OC", "OC", "DC", "DC", "DC", "DC", "DC", "OC", "OC", "OC", "OC/TT"):
        wb.addToGeneralCard(idx, gcItem)
        idx += 1

    oMoves = (("Punch", '4', ''),  ("Kick", '5', ''),
              ("Chop", '4', ''), ("Clothesline", '7', ''),
              ("Dropkick", '7', ''), ("Stomp", '6', ''),
              ("Elbow Smash", '5', ''), ("Forearm Smash", '5', ''),
              ("Back Drop", '8', 'XX'), ("ROPES", '', ''),
              ("Big Splash", '', '(S)'))

    idx = 0
    for moveName, movePoints, moveType in oMoves:
        wb.addToOffensiveCard(idx, moveName, movePoints, moveType)
        idx += 1

    idx = 0
    for dcItem in ("REVERSE", "A", "A", "A", "B", "B", "B", "B", "A", "B", "C"):
        wb.addToDefensiveCard(idx, dcItem)
        idx += 1

    wb.setSpecialty("Big Splash")
    specMoves = (('6', 'P/A'), ('6', ''), ('7', ''),
                 ('8', ''), ('8', ''), ('8', 'P/A'))

    idx = 0
    for movePoints, moveType in specMoves:
        wb.addToSpecialtyCard(idx, movePoints, moveType)
        idx += 1

    rMoves = (("NA", '0', ''),  ("Kick", '5', ''),
              ("NA", '0', ''), ("Clothesline", '7', ''),
              ("Dropkick", '7', ''), ("NA", '0', ''),
              ("NA", '0', ''), ("Body Slam", '5', ''),
              ("NA", '0', ''), ("NA", '0', ''),
              ("Big Splash", '', '(S)'))
    
    idx = 0
    for moveName, movePoints, moveType in rMoves:
        wb.addToRopesCard(idx, moveName, movePoints, moveType)
        idx += 1

    wb.setSubMin(2)
    wb.setSubMax(6)
    wb.setTagTeamMin(2)
    wb.setTagTeamMax(2)
    wb.setPriSingles(1)
    wb.setPriTagTeam(1)

    wb.dump()
    wb.writeToFile("E:\\pws\\Wrestlers\JoeJobber.py")
    

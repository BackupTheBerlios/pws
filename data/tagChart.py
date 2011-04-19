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

from data.globalConstants import *

class TagChart:

    def __init__(self, teamSize):
        twoManTable = ({"ROUND_COUNT":1, "MAX_DT":ALL},
                       {"ROUND_COUNT":1, "MAX_DT":ALL},
                       {"ROUND_COUNT":1, "MAX_DT":2},
                       {"ROUND_COUNT":1, "MAX_DT":2},
                       {"ROUND_COUNT":1, "MAX_DT":2},
                       {"ROUND_COUNT":2, "MAX_DT":2},
                       {"ROUND_COUNT":2, "MAX_DT":2},
                       {"ROUND_COUNT":2, "MAX_DT":2},
                       {"ROUND_COUNT":3, "MAX_DT":2},
                       {"ROUND_COUNT":3, "MAX_DT":2},
                       {"ROUND_COUNT":INJURED, "MAX_DT":INJURED})

        threeManTable = ({"ROUND_COUNT":1, "MAX_DT":ALL},
                         {"ROUND_COUNT":1, "MAX_DT":ALL},
                         {"ROUND_COUNT":1, "MAX_DT":2},
                         {"ROUND_COUNT":1, "MAX_DT":2},
                         {"ROUND_COUNT":1, "MAX_DT":2},
                         {"ROUND_COUNT":1, "MAX_DT":3},
                         {"ROUND_COUNT":1, "MAX_DT":3},
                         {"ROUND_COUNT":1, "MAX_DT":3},
                         {"ROUND_COUNT":2, "MAX_DT":3},
                         {"ROUND_COUNT":2, "MAX_DT":3},
                         {"ROUND_COUNT":INJURED, "MAX_DT":INJURED})

        if teamSize == 2: self._tagTable = twoManTable
        else: self._tagTable = threeManTable
       
        self._injuryTable = ({"ROUND_COUNT":5,  "INJURED": ("MAN-OUT", )},
                             {"ROUND_COUNT":5,  "INJURED": ("MAN-IN", )},
                             {"ROUND_COUNT":10, "INJURED": ("MAN-OUT", )},
                             {"ROUND_COUNT":10, "INJURED": ("MAN-IN", )},
                             {"ROUND_COUNT":2,  "INJURED": ("MAN-IN", "MAN-OUT")},
                             {"ROUND_COUNT":3,  "INJURED": ("MAN-IN", "MAN-OUT")})

    def getTagChartResults(self, rollVal):
        return self._tagTable[rollVal]
        
    def getInjuryResults(self, rollVal):
        return self._injuryTable[rollVal]
        

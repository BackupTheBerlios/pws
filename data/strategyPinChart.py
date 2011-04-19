"""
Copyright 2004 John LeGrande

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
from globalConstants import *

class PinChart:
    chart = [[RSTAR, RSTAR, R, R, R, -4, -3, -2, -2, -2, PIN],
             [R, RSTAR, R, R, -5, -4, -3, -2, -2, -2, PIN],
             [RSTAR, RSTAR, RSTAR, RSTAR, -6, -5, -5, -4, -3, PIN, PIN],
             [RSTAR, RSTAR, RSTAR, -7, -6, -6, -5, -4, PIN, PIN, PIN],
             [RSTAR, RSTAR, -10, -10, -7, -7, 0, 0, PIN, PIN, PIN],
             [RSTAR, R, -10, -10, -7, -7, 0, 5, PIN, PIN, PIN],
             [R, -10, -7, -5, 0, 5, 6, PIN, PIN, PIN, PIN],
             [-2, 5, 6, 7, 7, 8, PIN, PIN, PIN, PIN, PIN],
             [6, 7, 8, 9, 9, 10, PIN, PIN, PIN, PIN, PIN],
             [9, 10, 10, 10, 15, PIN, PIN, PIN, PIN, PIN, PIN]]

    num2stringMap = {RSTAR:"REVERSE*", R:"REVERSE", PIN:"PIN"}
                      
    def getPinChartResult(self, score, rollval):
        if rollval > 10:
            rollval = 10
        elif rollval < 0:
            rollval = 0
        return self.chart[self.getPinGroup(score)][rollval]
    
    def getProbabilities(self, score, refmodifier=0, pinmodifier=0):
        col = self.chart[self.getPinGroup(score)]
        twoD6Probs = TWOD6_PROBABILITIES
        probDict = {"REVERSE_PROBABILITY":0, "REVERSE*_PROBABILITY":0,
                    "PIN_PROBABILITY":0, "REF_MODIFIER":refmodifier,
                    "PIN_MODIFIER":pinmodifier}

        modifierTotal = refmodifier + pinmodifier
        if modifierTotal < 0:
            col = col[:modifierTotal]
            worstResult = col[0]
            for bonus in range(abs(modifierTotal)):
                col.insert(0, worstResult)
        elif modifierTotal > 0:
            col = col[modifierTotal:]
            for bonus in range(modifierTotal):
                col.append(PIN)

        probidx = 0            
        for item in col:
            prob = twoD6Probs[probidx]
            if item in [RSTAR, R, PIN]:
                key = "%s_PROBABILITY" % self.num2stringMap[item]
                probDict[key] += prob
            else:
                if probDict.get(item):
                    probDict[item] += prob
                else:
                    probDict[item] = prob
            probidx += 1
        return probDict
                    
    def getProbabilityString(self, score):
        probs = self.getProbabilities(score)
        probString = "\n"
        # Get the string key/value pairs first
        for key in ["REVERSE*_PROBABILITY", "REVERSE_PROBABILITY",
                     "PIN_PROBABILITY"]:
            probString += "%s (%.1f%%)\n" % (key.split('_')[0],
                                           probs.pop(key))
        numericKeys = probs.keys()
        numericKeys.sort()
        for key in numericKeys:
            plusStr = ""
            if key > 0: plusStr = "+"
            probString += "%s%d (%.1f%%)\n" % (plusStr, key, probs[key])

        return probString
        
    def getPositiveProbability(self, score, modifier):
        positives = 0
        for key, value in self.getProbabilities(score, 0, modifier).items():
            if key == "PIN_PROBABILITY" or (key > -1 and type(key) == type(1)):
                positives += value

        return positives                
            
        
    def getPinGroup(self, score):
        pinGroup = 0
        if score % 15 == 0:
            pinGroup = -1

        pinGroup += int(score / 15)

        if pinGroup > 9: pinGroup = 9

        return pinGroup

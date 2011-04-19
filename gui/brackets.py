
class BracketPageBuilder:
    def __init__(self, tourneyRounds, tourneytable, currround, tourneyname="Tournament"):
        self.tourneyRounds = tourneyRounds
        self.currTourneyRound = currround

        self.htmlString = "<TITLE>%s</TITLE>" % tourneyname
        self.htmlString += "<CENTER><H3>%s</H3></CENTER>" % tourneyname
        self.htmlString += "<TABLE WIDTH=100% CELLPADDING=0 BORDER=0><THEAD>"+\
                          "<TR>\n"
        for round in range(1, self.tourneyRounds+1):
            roundStr = "Round %d" % round
            if round == self.tourneyRounds - 2 and self.tourneyRounds > 3:
                roundStr = "Quaterfinals"
            elif round == self.tourneyRounds - 1 and self.tourneyRounds > 2:
                roundStr = "Semifinals"
            elif round == self.tourneyRounds:
                roundStr = "Finals"                
            self.htmlString += "<TH><P><B>%s</B></P></TH>\n" % roundStr

        self.htmlString +="<TH><P><B>Winner</B></P></TH></TR></THEAD><TBODY>\n"
        rows = len(tourneytable[0]) * 2 - 1
        self._rowStrings = ['' for row in range(rows)]
        roundnum = 1
        currRoundSize = len(tourneytable[0])
        for idx in range(self.tourneyRounds + 1):
            if idx + 1> len(tourneytable):
                self._setRowStrings(['<BR>' for s in range(currRoundSize)],
                                    roundnum)
            else:
                self._setRowStrings(tourneytable[idx], roundnum)
            roundnum += 1
            currRoundSize /= 2
            
        for rowStr in self._rowStrings:
            self.htmlString += "<TR>%s</TR>\n" % rowStr 
        self.htmlString += "</TBODY></TABLE>"

    def getHTML(self): return self.htmlString
    
    def saveToFile(self, filename="F:\\pws\\gui\\out.html"):
        f = open(filename, 'w')
        f.write(self.htmlString)
        f.close()

    def _setRowStrings(self, data, roundnum):
        row = pow(2, roundnum - 1) - 1
        col = roundnum - 1
        currSeed = 1
        linebreaks = ""
        for teamStr in data:
            rowStr = ""
            currTeamStr = teamStr
            numCommas = currTeamStr.count(', ')
            if numCommas > 0:
                linebreaks = "<BR>" * (numCommas + 1)

            if teamStr == "<BR>" and roundnum <= self.currTourneyRound:
                currTeamStr = "<i>(BYE)</i>"

            for round in range(self.tourneyRounds + 1):                    
                if col == round:
                    rowStr += '<TD BGCOLOR="#cccccc">%s</TD>' % currTeamStr
                else:
                    rowStr += '<TD>%s</TD>' % linebreaks
            self._rowStrings[row] = rowStr
            row += pow(2, roundnum)
                
if __name__ == '__main__':
    BracketPageBuilder(4, [["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p"]])

        
        

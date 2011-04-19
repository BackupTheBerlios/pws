from lib.util import *
from data.globalConstants import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Table, Spacer, SimpleDocTemplate
from reportlab.platypus.xpreformatted import XPreformatted
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch


class HtmlActionCard:
    def __init__(self, wrestler):
        
        self.htmlString = "<HTML><TITLE>Action Card for %s</TITLE>" \
                     % wrestler.getName()

        # First row
        row = "<BODY><TABLE BORDER=1 CELLPADDING=2>"
        row += "<THEAD><TR><TH COLSPAN=2><B>%s</B>" % wrestler.getName()
        
        leftCol = [row]
        rightCol = ["</TH><TH><B>OFFENSIVE CARD</B></TH></TR></THEAD>"]

        leftCol += self._getGenCardHTML(wrestler.getGeneralCard())
        leftCol += self._getDefensiveCardHTML(wrestler.getDefensiveCard())
        leftCol += self._getSpecialtyCardHTML(wrestler.getSpecialtyCard())
        leftCol += self._getRangeHTML("SUB", wrestler.getSubmissionRange())
        leftCol += self._getRangeHTML("TAG-TEAM", wrestler.getTagTeamRange())
        leftCol += self._getPrioritiesHTML(wrestler)    

        rightCol += self._getOffensiveCardHTML(wrestler.getOffensiveCard())
        rightCol += self._getRopesCardHTML(wrestler.getRopesCard())

        self._mergeColumns(leftCol, rightCol)

    def _getGenCardHTML(self, gcard):
        # General Card Header
        strRows = ["<TR><TD COLSPAN=2 ALIGN=CENTER ><B>GENERAL CARD</B></TD>"]
        strRows += self._getTwoColBox(gcard, 0)
        return strRows

    def _getDefensiveCardHTML(self, dcard):
        # Defensive Card Header
        strRows = ["<TR><TD COLSPAN=2 ALIGN=CENTER><B>DEFENSIVE CARD</B></TD>"]
        strRows += self._getTwoColBox(dcard, 0)
        return strRows

    def _getSpecialtyCardHTML(self, speccard):
        moveName = speccard[0]["MOVE_NAME"]
        strRows = ["<TR><TD COLSPAN=2 ALIGN=CENTER><B>SPECIALTY:</B></TD>",
                   "<TR><TD COLSPAN=2 ALIGN=CENTER>%s</TD>" % moveName]

        strRows += self._getOneColBox(speccard, 0, 1, 1)
        return strRows

    def _getRangeHTML(self, name, range_tuple):
        strTuple = convertRangeTupleToString(range_tuple)
        spaces = "&nbsp;" * (9 - len(name))
        return ["<TR><TD COLSPAN=2><B>%s</B>%s: %s</TD>" % (name, spaces,
                                                            strTuple)]

    def _getPrioritiesHTML(self, wrestler):
        spri = convertPriorityToString(wrestler.getSinglesPriority())
        ttpri = convertPriorityToString(wrestler.getTagTeamPriority())
        spaces = "&nbsp;" 
        return ["<TR><TD COLSPAN=2><B>PRIORITY</B>%s: %s/%s" % (spaces, spri,
                                                                ttpri)]
                                                 
    def _getOffensiveCardHTML(self, ocard):
        return self._getOneColBox(ocard, 1, 2)

    def _getRopesCardHTML(self, rcard):
        strRows = ["<TD ALIGN=CENTER><B>=ROPES=</B></TD></TR>"]
        strRows += self._getOneColBox(rcard, 1, 2)
        print len(strRows)
        strRows += ["<TD>Name of Set</TD></TR>", "<TD> </TD></TR>"]
        print len(strRows)
        return strRows

    def _getTwoColBox(self, card, colidx):
        idx = 0
        strRows = []
        for idx in range(5):
            dieNum = idx + 2
            spaces = "&nbsp;" * 3
            moveName = spaces + convertToString(card[idx])
            firstTag = "<TR>"
            if colidx == 1:
                firstTag = ""

            htmlStr = ("%s<TD><B>%d</B>%s</TD>\n" % (firstTag, dieNum,
                                                     moveName))

            if dieNum + 5 > 9:  # Double digit numbers
                spaces = "&nbsp;"
            moveName = spaces + convertToString(card[idx + 5])

            lastTag = "</TR>"
            if colidx == 0:
                lastTag = ""
                
            htmlStr += ("<TD><B>%d</B>%s</TD>%s\n" % (dieNum + 5, moveName,
                                                      lastTag))
            strRows.append(htmlStr)
            idx += 1

        moveName = convertToString(card[-1])
        firstTag = "<TR><TD COLSPAN=2>"
        lastTag = "</TR>"
        if colidx == 0:
            lastTag = ""
        else:
            firstTag = "<TD>"
            
        tmpStr = "%s<CENTER><B>12</B> %s" % (firstTag, moveName)
        strRows.append("%s</CENTER></TD>%s\n" % (tmpStr, lastTag))

        return strRows

    def _getOneColBox(self, card, colidx, die_start, strip_move_name=0):
        dieNum = die_start
        strRows = []
        for move in card:
            firstTag = "<TR><TD COLSPAN=2>"
            lastTag = "</TR>"
            if colidx == 1:
                firstTag = "<TD>"
            else:
                lastTag = ""
            spaces = "&nbsp;" * 3
            if dieNum > 9:
                spaces = "&nbsp;"

            moveName = spaces + convertMoveToString(move, strip_move_name)
            if move["MOVE_TYPE"] == SPECIALTY and not strip_move_name:
                moveName = moveName[:-3] + "<B>(S)</B>"
                
            strRows.append("%s<B>%d</B>%s</TD>%s\n" % (firstTag,
                                                       dieNum,
                                                       moveName,
                                                       lastTag))
            dieNum += 1

        return strRows

    def _mergeColumns(self, leftcol, rightcol):
        print len(leftcol), len(rightcol)
        for idx in range(len(leftcol)):
            self.htmlString += "%s%s" % (leftcol[idx], rightcol[idx])
        self.htmlString += "</BODY></HTML>"

    def getHTML(self):
        return self.htmlString

class PdfActionCard:
    """
           0                    1
    --------------------------------------
    | Name           |   OFFENSIVE CARD  | 0
    --------------------------------------
    |  GENERAL CARD  | 2 MOVE PTS (TYPE) | 1
    --------------------------------------
    | 2 GC |  7 GC   | 3 MOVE PTS (TYPE) | 2
    --------------------------------------
    | 3 GC |  8 GC   | 4 MOVE PTS (TYPE) | 3
    --------------------------------------
    | 4 GC |  9 GC   | 5 MOVE PTS (TYPE) | 4
    --------------------------------------
    | 5 GC |  10 GC  | 6 MOVE PTS (TYPE) | 5
    --------------------------------------
    | 6 GC |  11 GC  | 7 MOVE PTS (TYPE) | 6
    --------------------------------------
    |    12 GC       | 8 MOVE PTS (TYPE) | 7
    --------------------------------------
    |  DEFNSIVE CARD | 9 MOVE PTS (TYPE) | 8
    --------------------------------------
    | 2 DC |  7 DC   | 10 MOVE PTS (TYPE)| 9
    --------------------------------------
    | 3 DC |  8 DC   | 11 MOVE PTS (TYPE)| 10
    --------------------------------------
    | 4 DC |  9 DC   | 12 MOVE PTS (TYPE)| 11            
    --------------------------------------
    | 5 DC |  10 DC  |       ROPES       | 12
    --------------------------------------
    | 6 DC |  11 DC  | 2 MOVE PTS (TYPE) | 13
    --------------------------------------
    |    12 DC       | 3 MOVE PTS (TYPE) | 14
    --------------------------------------
    |   SPECIALTY:   | 4 MOVE PTS (TYPE) | 15
    --------------------------------------
    | SPEC MOVE NAME | 5 MOVE PTS (TYPE) | 16
    --------------------------------------
    | 1 PTS (TYPE)   | 6 MOVE PTS (TYPE) | 17
    --------------------------------------
    | 2 PTS (TYPE)   | 7 MOVE PTS (TYPE) | 18
    --------------------------------------
    | 3 PTS (TYPE)   | 8 MOVE PTS (TYPE) | 19
    --------------------------------------
    | 4 PTS (TYPE)   | 9 MOVE PTS (TYPE) | 20
    --------------------------------------
    | 5 PTS (TYPE)   | 10 MOVE PTS (TYPE)| 21
    --------------------------------------
    | 6 PTS (TYPE)   | 11 MOVE PTS (TYPE)| 22
    --------------------------------------
    | SUB: x-y       | 12 MOVE PTS (TYPE)| 23
    --------------------------------------
    | TAG-TEAM: x-y  |                   | 24
    --------------------------------------
    | PRIORITY: x/y  |                   | 25
    --------------------------------------

    Nested tables for the General Card (0, 2) - (0, 6)
    Nested tables for the Defensive Card (0, 9) - (0, 13)
    """
    
    def __init__(self, wrestler):
        self.wrestler = wrestler
        self.style = getSampleStyleSheet()['BodyText']

        pName = XPreformatted("<para align=center><font size=+3><b>%s</b>"\
                              "</para>" % wrestler.getName(),
                             self.style)
        self.leftCol = [pName]
        self.rightCol = [self._makeBoldAndCenter("OFFENSIVE CARD")]

        self.leftCol += self._getGeneralCard()
        self.leftCol += self._getDefensiveCard()
        self.leftCol += self._getSpecialtyCard()
        self.leftCol += self._getRatings()

        self.rightCol += self._getOffensiveCard()
        self.rightCol += self._getRopesCard()
        self.rightCol += [self._makeFirstItemBold(wrestler.getNameSet(), ""),
                          ""]

        self._mergeColumns()

    def _mergeColumns(self):
        self.acTable = []
        for idx in range(len(self.leftCol)):
            self.acTable.append([self.leftCol[idx], self.rightCol[idx]])

    def writePDF(self, filename="export.pdf"):
        bt = 2   # border thickness
        acTable = self.acTable
        c = Canvas(filename)
        t = Table(acTable, style=[('GRID',
                                   (0,0), (-1,-1), .25, colors.green),
                                  ('BOTTOMPADDING', (0,2), (0,6), 0),
                                  ('BOTTOMPADDING', (0,9), (0,13), 0),
                                  ('BOX', (0,0), (-1,-1), bt, colors.green),
                                  ('LINEAFTER', (0,0), (0,-1), bt,
                                   colors.green),
                                  ('BOX', (0,1), (0,1), bt, colors.green),
                                  ('BOX', (0,8), (0,8), bt, colors.green),
                                  ('BOX', (0,15), (0,15), bt, colors.green),
                                  ('BOX', (0,23), (0,-1), bt, colors.green),
                                  ('BOX', (1,0), (1,0), bt, colors.green),
                                  ('BOX', (1,12), (1,12), bt, colors.green),
                                  ('BOX', (1,-2), (1,-1), bt, colors.green)],
                  rowHeights=[20] * len(acTable))
        
        doc = SimpleDocTemplate(filename, pagesize=(8.5*inch, 11*inch))
        l = []
        l.append(t)
        l.append(Spacer(0,12))
        doc.build(l)
                                        
        
    def _getGeneralCard(self):
        rows = [self._makeBoldAndCenter("GENERAL CARD")]
        gc = self.wrestler.getGeneralCard()        
        rows += self._getTwoColTable(gc[:-1])
        rows.append(self._makeFirstItemBold("%-4d" % 12,
                                            "%s" % convertToString(gc[-1]),
                                            1))
        return rows

    def _getDefensiveCard(self):
        rows = [self._makeBoldAndCenter("DEFENSIVE CARD")]
        dc = self.wrestler.getDefensiveCard()        
        rows += self._getTwoColTable(dc[:-1])
        rows.append(self._makeFirstItemBold("%-4d" % 12,
                                            "%s" % convertToString(dc[-1]),
                                            1))
        return rows

    def _getSpecialtyCard(self):
        speccard = self.wrestler.getSpecialtyCard()
        rows = [self._makeBoldAndCenter("SPECIALTY:"),
                self._center(speccard[0]["MOVE_NAME"])]

        dieNum = 1
        for move in speccard:
            moveDict = getMoveStringDict(move)
            moveType = moveDict.get("MOVE_TYPE", "")
            if moveType == "(S)":
                moveType = ""
            specStr = "%s %s" % (moveDict["MOVE_POINTS"], moveType)
            rows.append(self._makeFirstItemBold("%-4d" % dieNum, specStr))
            dieNum += 1

        return rows
            
    def _getRatings(self):
        """Get the Sub, Tag-Team, and Priority ratings"""

        rows = []
        subTup = self.wrestler.getSubmissionRange()
        subRange = convertRangeTupleToString(subTup)
        rows.append(self._makeFirstItemBold("%-19s: " % "SUB", subRange))

        tagTup = self.wrestler.getTagTeamRange()
        tagRange = convertRangeTupleToString(tagTup)
        rows.append(self._makeFirstItemBold("%-10s: " % "TAG-TEAM", tagRange))

        spri = convertPriorityToString(self.wrestler.getSinglesPriority())
        ttpri = convertPriorityToString(self.wrestler.getTagTeamPriority())
        rows.append(self._makeFirstItemBold("%-12s: " % "PRIORITY",
                                            "%s/%s" % (spri, ttpri)))
        return rows
                    

    def _getOffensiveCard(self):
        return self._getMoveList(self.wrestler.getOffensiveCard())

    def _getRopesCard(self):
        rows = [self._makeBoldAndCenter("=ROPES=")]
        rows += self._getMoveList(self.wrestler.getRopesCard())
        return rows
        
    def _getTwoColTable(self, carddata):
        rows = []
        for idx in range(len(carddata) / 2):
            col1DieNum = idx + 2
            col1Val = convertToString(carddata[idx])
            if col1DieNum < 10:
                c1Str = self._makeFirstItemBold("%-5d" % col1DieNum, col1Val)
            else:
                c1Str = self._makeFirstItemBold("%-4d" % col1DieNum, col1Val)

            col2DieNum = idx + 7
            col2Val = convertToString(carddata[idx + 5])
            if col2DieNum < 10:
                c2Str = self._makeFirstItemBold("%-5d" % col2DieNum, col2Val)
            else:
                c2Str = self._makeFirstItemBold("%-4d" % col2DieNum, col2Val)
            
            rows.append(self._makeOneRowTable([c1Str, c2Str]))

        return rows
            
    def _getMoveList(self, moves):
        rows = []
        dieNum = 2
        for move in moves:
            moveDict = getMoveStringDict(move)
            moveName = moveDict.get("MOVE_NAME", "")
            movePoints = moveDict.get("MOVE_POINTS", "")
            moveType = moveDict.get("MOVE_TYPE", "")
            if moveType == "(S)":
                moveType = "<b>(S)</b>"
            if dieNum < 10:
                dieStr = "%-5d" % dieNum
            else:            
                dieStr = "%-4d" % dieNum
                
            moveStr = "%s  %s %s" % (moveName, movePoints, moveType)
            rows.append(self._makeFirstItemBold(dieStr, moveStr))
            dieNum += 1

        return rows                            
        
    def _getSpaces(self, dienum):
        spaces = " "
        if dienum < 10:
            spaces = "   "
        return spaces
    
    def _makeOneRowTable(self, row):
        return Table([row], rowHeights=[20],
                     style=[('INNERGRID', (0,0), (-1,-1), .25, colors.green)])
        
    def _makeFirstItemBold(self, firstitem, remain, center=0):
        retStr = "<b>%s</b>%s" % (firstitem, remain)
        if center:
            retStr = "<para align=center>%s</para>" % retStr
            
        return XPreformatted(retStr, self.style)

    def _makeBoldAndCenter(self, instr):        
        return XPreformatted("<para align=center><b>%s</b></para>" % instr,
                             self.style)

    def _center(self, instr):
        return XPreformatted("<para align=center>%s</para>" % instr,
                             self.style)
        
        
if __name__ == '__main__':
    
    from Wrestlers import Abdullah
    from lib import spw

    w = spw.Wrestler(Abdullah)
    ac = PdfActionCard(w)
    ac.writePDF("abdullah.pdf")
    #f = open("exporttest.html", 'w')
    #f.write(ac.getHTML())
    #f.close()


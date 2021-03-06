from data.globalConstants import *
# Larry Zybysco
name = 'Larry Zybysco'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1002, 1002, 1000, 1002, 1000, 1001, 1000, 1000, 1002, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'ABDOMINAL STRETCH'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BOOT TO FACE'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'PILEDRIVER'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FLYING KNEEDROP'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'QUICK LEG PICK-UP'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ARM SLAM'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'RIGHT TO JAW'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'Z-FLY SUPLEX'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'STOMP INTO CROWD'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SIDE NECKBREAKER'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 0, 4, 2, 0, 0, 2, 2, 0, 5, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'PILEDRIVER': [   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 15, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005}]}

# Ropes Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
#    1014 = No Action (NA)
Ropes = \
[   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'SUNSET FLIP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SMASH TO GUT'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'}]

Sub = (2, 4)
TagTeam = (2, 5)
Priority = (4, 3)
nameSet = "Promoter's Dream"

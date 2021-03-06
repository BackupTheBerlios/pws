from data.globalConstants import *
# David Schultz
name = 'David Schultz'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1002, 1000, 1002, 1000, 1000, 1002, 1000, 1001, 1002, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'BACKBREAKER'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'DIXIE SUPLEX'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MD-SLAM'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'HEADLOCK'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'DOUBLE BARREL SLUG'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'EYE GOUGE'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'HURL OUT OF RING'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'SLINGSHOT SMASH'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MUSCRAT YANK'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FACE SLAP'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 0, 5, 2, 2, 2, 2, 0, 4, 2, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'SLINGSHOT SMASH': [   {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 15, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003},
                           {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003}]}

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
[   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CROSS BODY BLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'KICK OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'SLINGSHOT SMASH'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO RIBS'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO RIBS'}]

Sub = (2, 3)
TagTeam = (2, 5)
Priority = (3, 2)
nameSet = "Promoter's Dream"

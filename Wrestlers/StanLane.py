from data.globalConstants import *
# Stan Lane
name = 'Stan Lane'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1002, 1002, 1000, 1000, 1000, 1001, 1002, 1002, 1002, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SUNSET FLIP'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'FIGURE FOUR LEGLOCK'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'STEP OVER TOEHOLD'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ARM DRAG TAKE-DOWN'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'VEGAS SUPLEX'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TWO-FISTED ARM SLAM'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FLYING DROPKICKS'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LEG-DIVE TAKE-DOWN'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'FABULOUS SPIN-KICK'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'LEFT TO JAW'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 0, 4, 5, 2, 2, 2, 2, 2, 0, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'FABULOUS SPIN-KICK': [   {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                              {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                              {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                              {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                              {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                              {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005}]}

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
[   {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREARM SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FLYING DROPKICK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CROSS BODY BLOCK'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'FABULOUS SPIN-KICK'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BACKDROP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO SHORT RIB'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'SUNSET FLIP'}]

Sub = (2, 5)
TagTeam = (2, 5)
Priority = (2, 3)
nameSet = "Promoter's Dream"

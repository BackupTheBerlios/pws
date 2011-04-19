from data.globalConstants import *
# Nikolai Volkoff
name = 'Nikolai Volkoff'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1000, 1000, 1002, 1002, 1000, 1001, 1002, 1000, 1000, 1000]

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
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'SIBERIAN BEARHUG'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'RUSSIAN SPINE-BUSTER'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'DOUBLE ELBOW SLAM'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREARM SMASHES'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO FACE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHOKE WITH RING ROPE'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'RUSSIAN BOOT'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'INVERTED SUPLEX'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW THRU ROPES'},
    {'MOVE_POINTS': 4, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SING RUSSIAN ANTHEM'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 5, 2, 0, 0, 0, 2, 0, 2, 4, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'RUSSIAN SPINE-BUSTER': [   {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                                {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                                {'MOVE_POINTS': 13, 'MOVE_TYPE': 1004},
                                {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                                {'MOVE_POINTS': 14, 'MOVE_TYPE': 1004},
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
[   {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'RUSSIAN SPINE-BUSTER'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODYBLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SLAM'},
    {   'MOVE_NAME': 'SLAM ONTO CEMENT FLOOR',
        'MOVE_POINTS': 9,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {   'MOVE_NAME': 'RUSSIAN BOOT TO FACE',
        'MOVE_POINTS': 10,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 4)
TagTeam = (8, 12)
Priority = (4, 3)
nameSet = "Promoter's Dream"

from data.globalConstants import *
# Road Warrior Animal
name = 'Road Warrior Animal'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1002, 1000, 1000, 1001, 1000, 1000, 1002, 1002, 1002]

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
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHINLOCK'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'CONCRETE BODY SLAM'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'POWER SMASH'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ONE-HAND TOSS'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'WILD HAYMAKER'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'RUMBLE-SLAM'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CRUSHING BACKBREAKER'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'EYE RAKE'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'CLOTHESLINE'},
    {   'MOVE_NAME': 'OUTSIDE INTERFERENCE',
        'MOVE_POINTS': 10,
        'MOVE_TYPE': 1008}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 2, 2, 4, 2, 2, 5, 2, 0, 0, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'POWER SMASH': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                       {'MOVE_POINTS': 11, 'MOVE_TYPE': 1003},
                       {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                       {'MOVE_POINTS': 15, 'MOVE_TYPE': 1005},
                       {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                       {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003}]}

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
[   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'CLOTHESLINE'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'POWER SMASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'POWER SMASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'POWER SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'KICK INTO CROWD'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CLOTHESLINE'}]

Sub = (2, 3)
TagTeam = (2, 7)
Priority = (4, 3.5)
nameSet = "Promoter's Dream"

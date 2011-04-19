from data.globalConstants import *
# Steve Kiern
name = 'Steve Kiern'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1000, 1002, 1000, 1002, 1000, 1001, 1002, 1000, 1002, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {   'MOVE_NAME': 'FLYING HEAD SCISSORS',
        'MOVE_POINTS': 10,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'REVERSE CRADLE'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'MONKEY FLIP'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'FABULOUS SPIN-KICK'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'RIGHT TO JAW'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREARM SMASHES'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SPINNING TOE HOLD'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CROSS-ANKLE PICKUP'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'HIP ROLL TO MAT'},
    {   'MOVE_NAME': 'RAM HEAD INTO TURNBUCKLE',
        'MOVE_POINTS': 8,
        'MOVE_TYPE': 1008},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 0, 2, 5, 0, 2, 2, 4, 2, 0, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'FABULOUS SPIN-KICK': [   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                              {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                              {'MOVE_POINTS': 11, 'MOVE_TYPE': 1003},
                              {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003},
                              {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
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
[   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREARM SMASHES'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREARM SMASHES'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER BLOCK'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'FABULOUS SPIN-KICK'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'RIGHT TO JAW'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TURNBUCKLE SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'SUNSET FLIP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 5)
TagTeam = (8, 12)
Priority = (2, 3)
nameSet = "Promoter's Dream"

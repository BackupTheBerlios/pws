from data.globalConstants import *
# Mr. Fuji
name = 'Mr. Fuji'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1000, 1002, 1000, 1002, 1002, 1001, 1002, 1000, 1000, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'OSAKIAN NERVE PINCH'},
    {   'MOVE_NAME': 'BODYSLAM ONTO TURNBUCKLE',
        'MOVE_POINTS': 8,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHOKE WITH RING ROPE'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'ORIENTAL CHICKEN WING'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'PRESSURE WRIST LOCK'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'JUDO CHOP TO HEART'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'ELBOW SMASH'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO GROIN'},
    {'MOVE_POINTS': 11, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MODIFIED LEG CRAB'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SALT IN EYES'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 5, 0, 4, 2, 2, 0, 0, 0, 0, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'ORIENTAL CHICKEN WING': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                                 {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                                 {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                                 {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                                 {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                                 {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005}]}

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
[   {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {   'MOVE_NAME': 'HIROSHIMA NERVE PINCH',
        'MOVE_POINTS': 7,
        'MOVE_TYPE': 1004},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHOP TO THROAT'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BACK FLIP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'ORIENTAL CHICKEN WING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO STOMACH'}]

Sub = (2, 7)
TagTeam = (2, 7)
Priority = (1, 3)
nameSet = "Promoter's Dream"

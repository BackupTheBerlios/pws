from data.globalConstants import *
# Terry Funk
name = 'Terry Funk'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1000, 1002, 1000, 1000, 1000, 1001, 1002, 1000, 1000]

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
    {   'MOVE_NAME': 'SCALD WITH BRANDING IRON',
        'MOVE_POINTS': 7,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LONGHORN CRAB'},
    {   'MOVE_NAME': 'RAM HEAD INTO STEEL POST',
        'MOVE_POINTS': 6,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'STANDING LEG LOCK'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ARMDRAG'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'SPINNING TOE HOLD'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'SLEEPER HOLD'},
    {   'MOVE_NAME': 'BELLY TO BACK SUPLEX',
        'MOVE_POINTS': 10,
        'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'STOMP HEAD INTO CANVAS',
        'MOVE_POINTS': 10,
        'MOVE_TYPE': 1008}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 0, 0, 4, 2, 2, 2, 5, 0, 0, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'SPINNING TOE HOLD': [   {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                             {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                             {'MOVE_POINTS': 15, 'MOVE_TYPE': 1003},
                             {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
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
[   {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'JUMP OFF MIDDLE ROPE'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CROSS BODY BLOCK'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'INVERTED BODYSLAM'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'SPINNING TOE HOLD'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'BODYSLAM ON CONCRETE'}]

Sub = (2, 6)
TagTeam = (2, 5)
Priority = (3, 2)
nameSet = "Promoter's Dream"

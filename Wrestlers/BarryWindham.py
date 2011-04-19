from data.globalConstants import *
# Barry Windham
name = 'Barry Windham'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1000, 1000, 1000, 1002, 1002, 1001, 1000, 1000, 1000, 1002]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'OUTSIDE ARM BAR'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'RIGHT UPPERCUT'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BULLDOG'},
    {   'MOVE_NAME': 'ATTACK DELTOID MUSCLE',
        'MOVE_POINTS': 7,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'AERIAL HIP TOSS'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FLYING DROPKICK'},
    {   'MOVE_NAME': 'ARM WHIP INTO RING POST',
        'MOVE_POINTS': 8,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TWISTING REVERSE'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ARMDRAG TAKE-DOWN'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'COWBOY LARIAT'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 0, 0, 2, 2, 2, 0, 4, 5, 2, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'BULLDOG': [   {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003},
                   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
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
[   {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FLYING BODYPRESS'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SPIN UNDER TAKE-DOWN'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FLYING DROPKICK'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'COWBOY LARIAT'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'FLYING DROP KICK'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'BACK BODY DROP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LARIAT'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 4)
TagTeam = (8, 12)
Priority = (3, 3)
nameSet = "Promoter's Dream"

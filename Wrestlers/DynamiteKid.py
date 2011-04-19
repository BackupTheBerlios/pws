from data.globalConstants import *
# Dynamite Kid
name = 'Dynamite Kid'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1002, 1000, 1000, 1001, 1002, 1002, 1000, 1000, 1002]

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
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'REVERSE NECKBREAKER'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FRONTAL LEG-TRIP'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LEG-DIVE TAKE-DOWN'},
    {   'MOVE_NAME': 'BELLY TO BELLY SUPLEX',
        'MOVE_POINTS': 8,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'OVERHEAD SMASH'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'REVERSE ARM LOCK'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'FOREARM SMASH'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BRITISH CRAB'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ABDOMINAL STRETCH'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'LONDON FOG SLEEPER'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [4, 2, 2, 2, 0, 0, 0, 0, 2, 2, 5]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'REVERSE NECKBREAKER': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                               {'MOVE_POINTS': 11, 'MOVE_TYPE': 1003},
                               {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                               {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                               {'MOVE_POINTS': 13, 'MOVE_TYPE': 1005},
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
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BACK BODYDROP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TURNBUCKLE SMASH'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'DROPKICKS'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'REVERSE CRADLE'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 6)
TagTeam = (2, 6)
Priority = (2, 3.5)
nameSet = "Promoter's Dream"

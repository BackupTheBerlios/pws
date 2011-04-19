from data.globalConstants import *
# Wahoo McDaniel
name = 'Wahoo McDaniel'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1000, 1002, 1002, 1000, 1000, 1000, 1001, 1000, 1000, 1002]

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
    {'MOVE_POINTS': 12, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'PILEDRIVER'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'TOMAHAWK CHOPS'},
    {   'MOVE_NAME': 'SLAM HEAD INTO TURNBUCKLE',
        'MOVE_POINTS': 7,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'APACHE BACKBREAKER'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODY SLAM'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'INDIAN LEGLOCK'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SUPLEX'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'INSIDE BACK CRADLE'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'WRIST LOCK TAKE-DOWN'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'TEE-PEE CRAB'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 4, 2, 0, 2, 0, 2, 0, 2, 0, 5]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'TOMAHAWK CHOPS': [   {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003},
                          {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
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
[   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'REVERSE SUNSET'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BACK DROP'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'TOMAHAWK CHOPS'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SPIN UNDER TAKE-DOWN'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'TOMAHAWK CHOPS'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'INDIAN SLEEPER'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 6)
TagTeam = (9, 12)
Priority = (2, 2)
nameSet = "Promoter's Dream"

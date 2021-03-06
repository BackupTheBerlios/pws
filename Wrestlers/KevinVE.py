from data.globalConstants import *
# Kevin Von Erich
name = 'Kevin Von Erich'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1002, 1002, 1002, 1000, 1001, 1000, 1000, 1000, 1002, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO BACKSIDE'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SNAP MARE'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BIG SPLASH'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'WINDING HEAD SMASH'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TEXAS HEADSCISSORS'},
    {   'MOVE_NAME': 'HIGH FLYING DROPKICKS',
        'MOVE_POINTS': 7,
        'MOVE_TYPE': 1009},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BRAIN CLAW'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'PINWHEEL KNEE SMASH'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'REVERSE CHINLOCK'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'TUMBLE ROLL-UP'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 2, 0, 5, 2, 2, 2, 4, 0, 2, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'BRAIN CLAW': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004},
                      {'MOVE_POINTS': 13, 'MOVE_TYPE': 1004},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004},
                      {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005}]}

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
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BRAIN CLAW'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BRAIN CLAW'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BRAIN CLAW'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BACK SMASH'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LEAP OFF TOP ROPE'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'REVERSE SUNSET'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 4)
TagTeam = (2, 6)
Priority = (3, 3.5)
nameSet = "Promoter's Dream"

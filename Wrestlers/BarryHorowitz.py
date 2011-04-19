from data.globalConstants import *
# Barry Horowitz
name = 'Barry Horowitz'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1001, 1002, 1000, 1002, 1000, 1000, 1002, 1002, 1000, 1002]

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
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'CHOKE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TURNBUCKLE SMASH'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FULL NELSON'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SNAP MARE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'HEADLOCK'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BEARHUG'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO MIDSECTION'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SIDE HEADLOCK'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'LEG DROP'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'EYE RAKE'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [5, 2, 2, 0, 0, 0, 0, 2, 2, 2, 4]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'LEG DROP': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
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
[   {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULER BLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 4, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO CHEST'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREARM BLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER BLOCK'}]

Sub = (2, 7)
TagTeam = (2, 4)
Priority = (1, 1)
nameSet = "Promoter's Dream"

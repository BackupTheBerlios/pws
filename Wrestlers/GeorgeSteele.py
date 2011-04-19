from data.globalConstants import *
# George Steele
name = 'George Steele'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1002, 1000, 1000, 1000, 1000, 1002, 1000, 1002, 1001]

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
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'STOMP LEFT ARM'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'STRANGLEHOLD'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHEW TURNBUCKLE'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'GUT THRUST'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'SMASH LEFT LEG'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'FOREIGN OBJECT'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BITE LEFT EAR'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'HAMMERLOCK'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'MANIAC SUPLEX'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 4, 2, 2, 0, 0, 0, 0, 2, 5, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'HAMMERLOCK': [   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004},
                      {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 9, 'MOVE_TYPE': 1004}]}

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
[   {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW INTO CROWD'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHEW ON TURNBUCKLE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHEW ON TURNBUCKLE'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'HAMMERLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KNEE TO GUT'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'KICK INTO CROWD'}]

Sub = (2, 4)
TagTeam = (2, 3)
Priority = (3, 1)
nameSet = "Promoter's Dream"

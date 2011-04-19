from data.globalConstants import *
# Buddy Roberts
name = 'Buddy Roberts'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1000, 1000, 1002, 1001, 1002, 1000, 1000, 1000, 1002, 1002]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'OVERHEAD SMASH'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LEG-DIVE TAKE DOWN'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'ORIENTAL SPIKE'},
    {'MOVE_POINTS': 12, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'REDNECK STOMP'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'REVERSE ARMBAR'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SIDEWINDER SUPLEX'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'HAMMERLOCK'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'PUSH OUT OF RING'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CONFEDERATE CHOP'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'KICK LIKE A DOG'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [5, 2, 2, 2, 0, 0, 0, 0, 4, 2, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'ORIENTAL SPIKE': [   {'MOVE_POINTS': 7, 'MOVE_TYPE': 1003},
                          {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 15, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                          {'MOVE_POINTS': 7, 'MOVE_TYPE': 1005}]}

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
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BOOT TO GUT'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER BLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ELBOW SMASH'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODYBLOCK'}]

Sub = (2, 5)
TagTeam = (2, 7)
Priority = (2, 3)
nameSet = "Promoter's Dream"

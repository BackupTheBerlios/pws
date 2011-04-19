from data.globalConstants import *
# Johnny Temp
name = 'Johnny Temp'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1000, 1000, 1002, 1002, 1002, 1002, 1000, 1000, 1000, 1001]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_TYPE': 1005, 'MOVE_NAME': 'WRITE CODE'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'WRITE MORE CODE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'WRITE EVEN MORE CODE'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'WRITE MORE EVEN CODE'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'WRITE CODE EVEN MORE'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CODE MORE EVEN WRITE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'EVEN MORE CODE WRITE'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CODE EVEN WRITE MORE'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'CODE WRITE'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'WRITE CODE'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [4, 2, 2, 0, 0, 0, 5, 2, 0, 4, 5]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
Specialty = {   'WRITE CODE': [   {'MOVE_TYPE': 1006},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 7, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003},
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
[   {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 4, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MAKE RELEASE DATE'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'DATE RELEASE MAKE'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'RELEASE DATE MAKE'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'FIX BUG'}]

Sub = (2, 7)
TagTeam = (2, )
Priority = (1, 1)
nameSet = ''

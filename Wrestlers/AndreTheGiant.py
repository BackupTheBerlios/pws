from data.globalConstants import *
# Andre the Giant
name = 'Andre the Giant'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1000, 1001, 1000, 1000, 1000, 1002, 1002, 1000, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'HOIST FOE ON ROPES'},
    {'MOVE_POINTS': 13, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'GIGANTIC POWERSLAM'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SIT ON OPPONENT'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'KNOGGIN KNOCKER'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BIG BOOT TO GUT'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BELLY BUMP'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'POWERSMASH'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'CLASP BEARHUG'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SQUASH'},
    {   'MOVE_NAME': 'POUNCE INTO TURNBUCKLE',
        'MOVE_POINTS': 8,
        'MOVE_TYPE': 1008},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 2, 2, 0, 4, 2, 2, 5, 0, 2, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'BIG SQUASH': [   {'MOVE_POINTS': 11, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 13, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 14, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003}]}

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
    {'MOVE_POINTS': 14, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'BEARHUG'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BELLY BUMP'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SQUASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODY BLOCK'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BELLY BUMP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SQUASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, )
TagTeam = (2, 7)
Priority = (5.5, 2)
nameSet = "Promoter's Dream"

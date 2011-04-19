from data.globalConstants import *
# Crusher Blackwell
name = 'Crusher Blackwell'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1000, 1002, 1002, 1000, 1002, 1000, 1000, 1001, 1000, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CRUSHING HEADLOCK'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'INVERTED BEARHUG'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SIT ON FOE'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SPLASH'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'POWER BODY SLAM'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'AIRPLANE SPIN'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MOUNTAIN BODYBLOCK'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'GIANT BACK BREAKER'},
    {   'MOVE_NAME': 'SHOULDER TO MIDSECTION',
        'MOVE_POINTS': 8,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'AERIAL KNEEDROP'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 2, 5, 2, 2, 0, 0, 4, 0, 2, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'BIG SPLASH': [   {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 14, 'MOVE_TYPE': 1005},
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
[   {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SPLASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SPLASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SPLASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'BIG SPLASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KNEEDROP OFF ROPES'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MOUNTAIN BODYBLOCK'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 5)
TagTeam = (2, 5)
Priority = (2, 2)
nameSet = "Promoter's Dream"

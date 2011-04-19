from data.globalConstants import *
# Ricky Steamboat
name = 'Ricky Steamboat'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1002, 1000, 1002, 1002, 1000, 1001, 1000, 1000, 1002, 1000]

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
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'HAWAIIAN DIVE'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'DROPKICKS'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'TURNAROUND SIDEKICK'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BARE FOOT KICK'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHOP TO CHEST'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'HIP ROLL'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'MARTIAL ARTS'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'BODYSLAM'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'SUGAR CANE SLEEPER'},
    {   'MOVE_NAME': 'POLYNESIAN PILEDRIVER',
        'MOVE_POINTS': 10,
        'MOVE_TYPE': 1003}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 5, 2, 2, 2, 2, 4, 0, 2, 0, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'MARTIAL ARTS': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                        {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                        {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                        {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003},
                        {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
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
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'FLYING BODYPRESS'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHOP TO CHEST'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'MARTIAL ARTS'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER BLOCK'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'MARTIAL ARTS'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'LEAP FROG'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'}]

Sub = (2, 5)
TagTeam = (2, 7)
Priority = (4, 3)
nameSet = "Promoter's Dream"

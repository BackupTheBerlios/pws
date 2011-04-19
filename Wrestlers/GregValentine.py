from data.globalConstants import *
# Greg Valentine
name = 'Greg Valentine'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1000, 1002, 1001, 1000, 1000, 1000, 1002, 1002, 1002]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ATOMIC KNEEDROP'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'ABDOMINAL STRETCH'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SLEDGEHAMMER'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'FIGURE-FOUR LEGLOCK'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO GROIN'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ELBOW TO THROAT'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'RAM INTO TURNBUCKLE'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'CHOKE ON ROPES'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODYSLAM'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'REVERSE PILEDRIVER'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 2, 0, 4, 2, 2, 5, 0, 0, 2, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'FIGURE-FOUR LEGLOCK': [   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1005},
                               {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                               {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                               {'MOVE_POINTS': 12, 'MOVE_TYPE': 1004},
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
[   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'HAMMER SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODYBLOCK'},
    {'MOVE_POINTS': 11, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'USE FOREIGN OBJECT'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODYSLAM'},
    {'MOVE_POINTS': 11, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'VERTICAL KNEE DROP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDERBLOCK'}]

Sub = (2, 3)
TagTeam = (7, 12)
Priority = (4, 3)
nameSet = "Promoter's Dream"

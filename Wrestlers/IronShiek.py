from data.globalConstants import *
# Iron Shiek
name = 'Iron Shiek'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1000, 1000, 1000, 1002, 1000, 1001, 1000, 1002, 1002, 1002]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'ARABIAN BACKBREAKER'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1004, 'MOVE_NAME': 'PERSIAN CRAB'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK WITH BOOT'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'VERTICAL SUPLEX'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'MONKEY FLIP'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'POWER FOREARM'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SLAM INTO TURNBUCKLE'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SLEDGE HAMMER'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'CAMEL BACK'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'SMASH WITH FIST'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [0, 0, 0, 2, 4, 2, 2, 5, 2, 0, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'CAMEL BACK': [   {'MOVE_POINTS': 11, 'MOVE_TYPE': 1004},
                      {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                      {'MOVE_POINTS': 10, 'MOVE_TYPE': 1004}]}

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
[   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'REVERSE CRADLE'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CROSS BODY BLOCK'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER BLOCK'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'AYATOLLAH SLAM'},
    {'MOVE_POINTS': 3, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'DENOUNCE USA'}]

Sub = (2, 4)
TagTeam = (8, 12)
Priority = (4, 3)
nameSet = "Promoter's Dream"

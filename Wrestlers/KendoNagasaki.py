from data.globalConstants import *
# Kendo Nagasaki
name = 'Kendo Nagasaki'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1002, 1002, 1000, 1002, 1000, 1000, 1000, 1001, 1002, 1000]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CHUNG DO SMASH'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'MARTIAL ARTS'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ORIENTAL SLEEPER'},
    {'MOVE_POINTS': 5, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'THROAT SIDE KICK'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'OX-JAW SMASH'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'THRUST KICK'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KARATE SMASH'},
    {'MOVE_POINTS': 10, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'MYSTIC SPIN'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1009, 'MOVE_NAME': 'BLATANT CHOKE'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'KICK OUT OF RING'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 0, 2, 5, 0, 2, 2, 0, 4, 2, 0]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'MARTIAL ARTS': [   {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                        {'MOVE_POINTS': 12, 'MOVE_TYPE': 1003},
                        {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                        {'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                        {'MOVE_POINTS': 7, 'MOVE_TYPE': 1003},
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
[   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'PEARL HARBOR DROP'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'ELBOW SMASH'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KARATE THRUST'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BODY BLOCK'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SHOULDER SMASH'},
    {'MOVE_POINTS': 12, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'PEARL HARBOR DROP'}]

Sub = (2, 5)
TagTeam = (2, 4)
Priority = (3, 2)
nameSet = "Promoter's Dream"

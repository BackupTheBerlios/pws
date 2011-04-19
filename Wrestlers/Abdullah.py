from data.globalConstants import *
# Abdullah the Butcher
name = 'Abdullah the Butcher'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1002, 1000, 1000, 1000, 1002, 1000, 1002, 1000, 1000, 1001, 1002]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW THRU ROPES'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'BLATANT CHOKE HOLD'},
    {'MOVE_TYPE': 1005, 'MOVE_NAME': 'FOREIGN OBJECTS'},
    {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'PLUNGE INTO RINGPOST'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1009, 'MOVE_NAME': "YANK FOE'S HAIR"},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'PUNCH TO FACE'},
    {'MOVE_POINTS': 9, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'EYE RAKE'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO JAW'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SIDE HEAD LOCK'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'KNEEDROP TO NECK'},
    {'MOVE_TYPE': 1010, 'MOVE_NAME': 'ROPES'}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [2, 4, 0, 0, 2, 0, 2, 2, 5, 0, 2]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
Specialty = {   'FOREIGN OBJECTS': [   {'MOVE_POINTS': 10, 'MOVE_TYPE': 1003},
                           {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 10, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 12, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 11, 'MOVE_TYPE': 1005},
                           {'MOVE_POINTS': 11, 'MOVE_TYPE': 1003}]}

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
[   {'MOVE_POINTS': 6, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'CROSS BODY BLOCK'},
    {   'MOVE_NAME': 'INJURE WITH FOREIGN OBJECT',
        'MOVE_POINTS': 9,
        'MOVE_TYPE': 1008},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'SMASH INTO RINGPOST'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'THROW OUT OF RING'},
    {'MOVE_TYPE': 1006, 'MOVE_NAME': 'HURL INTO CROWD'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 7, 'MOVE_TYPE': 1008, 'MOVE_NAME': 'KICK TO STERNUM'},
    {'MOVE_POINTS': 0, 'MOVE_TYPE': 1014, 'MOVE_NAME': 'NA'},
    {'MOVE_POINTS': 8, 'MOVE_TYPE': 1003, 'MOVE_NAME': 'ELBOW SMASH'}]

Sub = (2, 5)
TagTeam = (2, 7)
Priority = (4, 1)
nameSet = "Promoter's Dream"

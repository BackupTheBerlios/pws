from data.globalConstants import *
# Joe Jobber
name = 'Joe Jobber'

# General Card Definitions: 
#    1000 = OC
#    1001 = OC/TT
#    1002 = DC
GeneralCard = [1000, 1000, 1002, 1002, 1002, 1002, 1002, 1000, 1000, 1000, 1001]

# Offensive Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
#    1008 = Regular Offensive Move
#    1009 = Grudge Match Move (XX)
#    1010 = Ropes Move (ROPES)
OffensiveCard = \
[   {   'MOVE_NAME': 'Punch', 'MOVE_POINTS': 4, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Kick', 'MOVE_POINTS': 5, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Chop', 'MOVE_POINTS': 4, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Clothesline', 'MOVE_POINTS': 7, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Dropkick', 'MOVE_POINTS': 7, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Stomp', 'MOVE_POINTS': 6, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Elbow Smash', 'MOVE_POINTS': 5, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Forearm Smash', 'MOVE_POINTS': 5, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Back Drop', 'MOVE_POINTS': 8, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'ROPES', 'MOVE_TYPE': 1010},
    {   'MOVE_NAME': 'Big Splash', 'MOVE_TYPE': 1005}]

# Defensive Card Definitions:
#    0 = B - No points on defense
#    2 = A - 2 points on defense
#    4 = C - 4 points on defense and neutralize offensive move
#    5 = Reverse - Reverse offensive move
DefensiveCard = [5, 2, 2, 2, 0, 0, 0, 0, 2, 0, 4]

# Specialty Card Definitions:
#    1003 = Pin attempt move (P/A)
#    1004 = Submission Move (*)
#    1005 = Specialty Move (S)
#    1006 = Disqualification Move (DQ)
Specialty = {   'Big Splash': [   {   'MOVE_POINTS': 6, 'MOVE_TYPE': 1003},
                      {   'MOVE_POINTS': 6, 'MOVE_TYPE': 1005},
                      {   'MOVE_POINTS': 7, 'MOVE_TYPE': 1005},
                      {   'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                      {   'MOVE_POINTS': 8, 'MOVE_TYPE': 1005},
                      {   'MOVE_POINTS': 8, 'MOVE_TYPE': 1003}]}

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
[   {   'MOVE_NAME': 'NA', 'MOVE_POINTS': 0, 'MOVE_TYPE': 1014},
    {   'MOVE_NAME': 'Kick', 'MOVE_POINTS': 5, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'NA', 'MOVE_POINTS': 0, 'MOVE_TYPE': 1014},
    {   'MOVE_NAME': 'Clothesline', 'MOVE_POINTS': 7, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'Dropkick', 'MOVE_POINTS': 7, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'NA', 'MOVE_POINTS': 0, 'MOVE_TYPE': 1014},
    {   'MOVE_NAME': 'NA', 'MOVE_POINTS': 0, 'MOVE_TYPE': 1014},
    {   'MOVE_NAME': 'Body Slam', 'MOVE_POINTS': 5, 'MOVE_TYPE': 1008},
    {   'MOVE_NAME': 'NA', 'MOVE_POINTS': 0, 'MOVE_TYPE': 1014},
    {   'MOVE_NAME': 'NA', 'MOVE_POINTS': 0, 'MOVE_TYPE': 1014},
    {   'MOVE_NAME': 'Big Splash', 'MOVE_TYPE': 1005}]

Sub = (2, 6)
TagTeam = (2, )
Priority = (1, 1)
nameSet = ''

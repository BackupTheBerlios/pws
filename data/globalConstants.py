"""
Copyright 2003 John LeGrande

    This file is part of Pro Wrestling Superstar.

    Pro Wrestling Superstar is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Pro Wrestling Superstar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Pro Wrestling Superstar; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    A copy of the GNU GPL is included with Pro Wrestling Superstar in the file
    license.txt. 
"""

VERSION = ".95b"

A = 2
B = 0
C = 4
REVERSE = 5

GC = 1013
OC = 1000
OCTT = 1001
DC = 1002
NO_ROLL = 10014
PA = 1003
SUBMISSION = 1004
SPECIALTY  = 1005
DQ = 1006
DEFENSIVE = 1007
OFFENSIVE = 1008
XX = 1009
ROPES = 1010
INJURED = 1011
ALL = 1012
NA = 1014

GC_START_ROW = 1
DC_START_ROW = 8
SPECIALTY_START_ROW = 15
SUB_ROW = 23
TAG_TEAM_ROW = 24
PRIORITY_ROW = 25
OFFENSIVE_CARD_START_ROW = 0
ROPES_START_ROW = 12
DEFAULT_COL_SIZE = 106
DEFAULT_MOVE_COL_SIZE = 200
CARD_ENTRY_SIZE = 62
SCORECARD_CELL_WIDTHS = (18, 22, 28)

NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8
ALL   = 15
ITALIC = 16
BOLD = 32
CENTER_TEXT = 64

ROLL_DICE_BUTTON = 10

# Messages that will go into jowstgui.MainJowstWindow.msgQueue
ROLL_DICE_BUTTON_CLICKED = 11
TAG_OUT_OCCURRED = 13

ROUND_COLOR = "FOREST GREEN"
MOVE_COLOR = "BLUE"
FINISH_COLOR = "ORANGE"
INJURY_COLOR = "RED"

NO_TIME_LIMIT = 9999

DISABLED = 2000
ENABLED = 2001

SEPERATOR = 2002

PIN_GROUP_POINT_RANGES = (9, 9, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 4)
STRAT_PIN_GROUP_POINT_RANGES = (7, 7, 6, 5, 4, 4, 4, 1, 0, 0)

TOO_MANY_WRESTLERS_ERROR       = -1
WRESTLER_ALREADY_ON_TEAM_ERROR = -2

MATCH_SETUP          = 100
READY_TO_START_MATCH = 101
STARTING_MATCH       = 102
MATCH_RUNNING        = 103
DISCONNECT           = 104
SHUTTING_DOWN        = 105
CONNECTED            = 106
MATCH_STOPPED        = 107

# GUI states
AWAITING_DICE_ROLL_CLICK = 200
TAG_OUT_CHOICELIST       = 201
ROUND_START              = 202
CHOICE_LIST              = 203

NETWORK_LATENCY = 250  # 250 ms

# Advanced Pin Chart
RSTAR = -100
R     = -101
PIN   = 207

# Desperation scalers
LP_DESPERATION = 2.5    # LOWER PRIORITY DESPERATION
LHP_DESPERATION = 1.875 # LOSING HIGHER PRIORITY DESPERATION
WHP_DESPERATION = 1.125 # WINING HIGHER PRIORITY DESPERATION

TWOD6_PROBABILITIES = [2.8, 5.6, 8.3, 11.1, 13.9, 16.7, 13.9, 11.1, 8.3, 5.6,
                       2.8]

# YesOrNoDialog Constants
LINE   = 208
HEADING = 209

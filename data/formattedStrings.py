formattedStrings =\
{
    "GENERAL_CARD_PAGE_DESCRIPTION":
"""The General Card is used at the beginning of a round to determine whether
a wrestler will be on offense or defense for the round.  At the beginning of
a round a player will make a 2D6 roll on the General Card resulting in values
from 2-12.

The General Card options are defined as follows:
     OC    - The wrestler is will attempt an offensive move
     OC/TT - The wrestler attempt an offensive move.  In a tag team match,
             this will also initiate double-teaming.
     DC    - The Wrestler will be on defense for the round""",

    "SUBMISSION_RANGE_DESCRIPTION":
"""The submission range is used to determine whether a wrestler submits if he
is the victim of a submission hold.  When a wrestler is a victim of a
submission hold the program makes a submission roll (2D6) for the victim.  If
the roll falls within the range specicified, the wrestler will submit.""",

    "TAG_TEAM_RANGE_DESCRIPTION":
"""The tag team range is used during a tag team match when a wrestler is in a
dire pinning predicament.  When a wrestler is in a threatening pinning
predicament, the program will make a saving roll (2D6) for the victim.  If the
roll falls within the range specified, the wrestler's teammate will make the
save.""",

    "PRIORITIES_DESCRIPTION":
"""Priorities indicate the rating of a wrestler in singles and tag team
matches.  The ratings are broken down as follows:

SINGLES:                                      TAG TEAM:

Rating      Ability                           Rating     Ability
=======     =======                           ======     =======
  1         Preliminary-Poor                     1        Poor   
  2         Average                              2        Average-Good 
  3         Good                                 3        Top Contender
  4         Very Good                            3+       Championship Caliber
  5         Top Contender
  5+        Championship Caliber

For the ratings with a '+', enter a .5 to represent the '+'.  So a 5+
wrestler's entry should be entered as 5.5""",

    "DEFENSIVE_CARD_PAGE_DESCRIPTION":
"""When a wrestler is on defense during a round, the player makes a roll on
the Defensive Card.  There are four potential results from a Defensive Card
roll (2D6) and they are defined as follows:

    A - Defensive wrestler attempts to break the hold and receives 2 points
        for the round
    B - Defensive Wrestler absorbs the punishment and gets 0 points for the
        round.
    C - Defensive Wrestler neutralizes offensive move and receives 4 points
        for the round while the offensive wrestler receives 0 points for the
        round
    REVERSE - Defensive wrestler reverses the offensive move and immdediately
              becomes the offensive wrestler.  The formerly defensive wrestler
              now rolls on his offensive card.
""",

    "OFFENSIVE_CARD_PAGE_DESCRIPTION":
"""If a wrestler is on offense for the round, the player will make an Offensive
Card roll.  The first column in the Offensive Card is the move name
The second column is the point total of the move (if necessary), and the third
column is the move type.  The various move types are defined
as follows:

    P/A - Pin attempt move.  The wrestler will attempt a pin at the end of the
          round.
    *   - Submission move.  At the end of the round, a submission check will be
          made for the 'victim' of the submission hold.
    (S) - Specialty move.  This is the wrestler's finishing move.  No point
          total is required for the Specialty move since the point totals
          for the specialty move are defined on the Specialty Card.
    (XX) - Grudge Match move.  This feature is currently not implemented.
    (DQ) - Disqualification Move.  The wrestler throws the oppopnent out of the
           ring.  At the end of the round, a countout roll will be made for
           the 'victim' of a disqualification roll.  There is no point total
           required for this move, since the points will come from the
           countout roll at the end of the round.
    ROPES - Ropes move.  The wrestler will need to make a roll on the ROPES
            card to determine what offensive move they execute.

For a regular offensive move, do not select anything in the move type column
for the move.
""",
    "ROPES_CARD_PAGE_DESCRIPTION":
"""If player rolls ROPES on the Offensive Card, then the player will need to
make a ROPES card roll.  Just like the Offensive Card, the first column of the
ROPES card is the move name, the second column is the point total for the move
(if necessary), and the third column is the move type.  The move types
available on the Ropes Card are below:

    P/A - Pin attempt move.  The wrestler will attempt a pin at the end of the
          round.
    *   - Submission move.  At the end of the round, a submission check will be
          made for the 'victim' of the submission hold.
    (S) - Specialty move.  This is the wrestler's finishing move.  No point
          total is required for the Specialty move since the point totals
          for the specialty move are defined on the Specialty Card.
    (XX) - Grudge Match move.  This feature is currently not implemented.
    (DQ) - Disqualification Move.  The wrestler throws the oppopnent out of the
           ring.  At the end of the round, a countout roll will be made for
           the 'victim' of a disqualification roll.  There is no point total
           required for this move, since the points will come from the
           countout roll at the end of the round.
    NA - There was NO ACTION at the ropes.  The offensive player gets 0 points.

For a regular offensive move, do not select anything in the move type column
for the move.""",

    "SPECIALTY_CARD_PAGE_DESCRIPTION":
"""If the offensive player rolls a specialty move (a move followed by an (S))
on their Offensive Card or their ROPES Card, the player will need to make a
Specialty Card roll.  The first column ot the Specialty Card is the point total
for the Specialty Move.  The second column is the move type.  The move types
available on the Specialty Card are below:

    P/A - Pin attempt move.  The wrestler will attempt a pin at the end of the
          round.
    *   - Submission move.  At the end of the round, a submission check will be
          made for the 'victim' of the submission hold.

If no pin attempt or submission attempt should be made, do not select anything
in the move type column.""",
    "WRESTLER_SAVE_ERROR":
"""There was a problem with the %s. %s was not saved.""",
    "BUILDER_IS_DIRTY_MSG":
"""Any existing data in the builder will be lost if a new wrestler is loaded.  Do you wish to continue?""",
    "CLEAR_BUILDER_MSG":
"""Any existing data in the builder will be lost when clearing.  Do you wish to
continue?""",
    """BUILDER_CLOSE_MSG""":
"""Are you sure you want to close the Wrestler Builder?"""
}

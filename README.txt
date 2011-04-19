Pro Wrestling Superstar v .95

PWS-BETA RELEASE .95 README 
===========================

This version of Pro Wrestling Superstar provides some significant features and 
enahncements.  Keep in mind that this is still Beta code, so there will 
probably be bugs.  I believe I've fixed most of the showstoppers, but there 
is a possibility that I may have missed some things.  Please bare with me and 
if you find a bug, please report it.

What's New?
===========

New Matches:

    * Dog Collar
    * Boot Camp

Tournament Mode:

    * PWS now provides the ability to run single-elimination tournaments for 
      singles, tag team, and six man matchups.
    * Export tournament brackets as HTML files or print brackets directly from
      PWS.  This is very basic at this point, but the format of the brackets
      will be improved in future releases.
    * Save Tournaments in progress, so you can continue later.

Wrestler Builder/Editor:

    * Removed Offensive Card Specialty (S) restrictions.
    * Removed Defensive Card "REVERSE" and "C" restrictions.

Data Management:

   * Win/Loss Record tracking
   * Win/Loss Record export to HTML or print win/loss record directly from
     PWS
   * Rankings (currently by win percentage) can be exported to HTML or
     printed directly from PWS.  Other ranking systems will be available in
     future releases.

Wrestler Management:

    * Ability to export wrestler ActionCards to PDF files
    * Ability to delete wrestlers 

Match Engine:

    * Option to use Strategy Pin Chart 
    * Option to have pins only occur on Pin Attempt (P/A) rolls
    * Finer grain drama events.  The options are dramatic pause, Real Time Pin
      Counts, Real Time Countouts, and Submission Drama

Other:

    * In the match wrestler selection dialog, double clicking on a wrestler
      will display that wrestler's ActionCard
    * Various performance enhancements.
    * Numerous bug fixes



Boot Camp Match & Dog Collar Match
==================================

More grudge match action!  To start a boot camp or dog collar match, select 
Run -> Run Match from the Menu.  On the Match Setup window in the "Match Type" 
selector, choose "Boot Camp" or "Dog Collar".  DQs will be disabled and DQ 
moves will be for points only. EXCEPTION: In the boot camp match, there are 
moves which, when executed, require the victim to answer the count.  If the
victim does not answer the count, he is counted out.

In either singles or a tag Boot Camp or Dog Coallar match, the winner is the 
first to score a pinfall or submission


Tournament Mode
===============

To start a single elimination tournament, select Run -> Run New Tournament
from the menu.  A tournament cofiguration dialog will be displayed with the 
following options:

    * Number of competitors (or teams) - This is the number of indiviual
      wrestlers or teams in the tournament
    * Team Size - the number of wrestlers on a team (enter 1 for a singles
      tournament)
    * Tournament Name - Enter a name to describe tournament.  If no name is
      provided, the description "Tournament" will be used.

Click OK once you've entered the configuration.  The Tournament Selection 
window will be displayed.  To add a wrestler to the tournament, simply click on
the checkbox next to th wrestler's name.  To remove a wrestler, just uncheck 
the wrestler.  To set a wrestler at a specific seed position, select the seed
postion in the seed list and then check the wrestler's checkbox.

Click the "Start Tournament" button once you've made your selections.  The
Tournament Control Panel will be displayed.

The Tourney Control Panel consists of the Matches tab and the Brackets tab.  
To switch between these two tabs, click on the appropriate tab near the upper 
left corner of the control panel.  The Matches tab contains the match selection
list and the match setup options, while the Brackets tab is a graphical
representation of the tournament tree.

To start a match, select a match in the match selection list and click the 
"Start Match" button.  The Tourney Control Panel will "disappear" and the match
will start.  When the match is finished or if the match is stopped, the 
Tourney Control Panel will displayed again showing the remaining matches for
the round and updated brackets.

To export or print the tournament tree, select the Brackets tab and then select
File -> Export Bracket or File -> Print Bracket from the menu.

To save a tournament, select File -> Save Tournament 
(or File -> Save Tournament As...) from the Tournament Control Panel menu.

To load a previously saved tournament, select File -> Open Tournament from the
MAIN PWS Window.


Win/Loss Tracking
=================

After each match a player will be prompted to update a results database with 
the match results.  In this prompt, players will have the option to update a
results database with the match time, the winner and loser, the match date,
the event at which the match took place, and the location (city, arena) of 
the match.  The player can change the following information before updating the
database:  Match Date, Event, and Location.

Once you are satisfied with the results data, you can select a results database
to update in the database selector.  If there are no existing results
databases, select "Create a new results database" which will ask players to
enter a name for the new results database.  After a database has been selected,
click the OK button.  A message box will appear informing the player that the
database has been updated.

To view win/loss records and rankings, select File -> Open Results Database 
from the menu in the main PWS window.  Select the database to open and click 
OK.  The Results Manager will be displayed.  The View menu contains the various
"reports" for wins/losses and rankings.  Select the item you wish to view.

To Export or Print a win/loss record or rankings, select the tab you want to
export or print, and then select File -> Export... or File -> Print...


Wrestler Management
===================

To export a wrestler's ActionCard to PDF, select File -> Export Wrestler from 
the menu in the main PWS window.  Select the wrestler you wish to export and
click OK.  You will then be asked where the action card should be saved.

You can also export ActionCards from any ActionCard "viewer" window by 
selecting File -> Export... from the viewer window's menu.

To delete wrestlers from PWS, select File -> Delete Wrestlers from the menu in
the PWS main window.  The selection dialog will appear.  Select the wrestlers
you wish to delete and then click OK.  A confirmation box will appear listing
the wrestlers slated for deletion.  Clicking OK will delete the wrestlers who
were slated for deletion.


Strategy Pin Chart
==================

The Strategy Pin Chart adds some interesting tactical options to PWS.  Going
for a pin is now a much riskier proposition since a pin attempt can be 
REVERSED or a wrestler can receive negative points for the pin attempt!  The 
less damage a wrestler has done to his opponent, the more likely it is that 
the pin attempt will be reversed or he'll receive negative points for the pin 
attempt!

When a wrestler is eligible for a pin or rolls a P/A move, players will be 
asked if they want to go for the pin (if the wrestler is CPU controlled the
player will not be prompted).  The probabilities of the various results will 
be displayed in the prompt.  Click OK to attempt a pin and cross your fingers!

To enable the strategy pin chart in the match setup, simply check the
"Strategy Pin Chart" checkbox.


System Requirements
===================

System Requirements for a Windows PC:
  Windows 98 or later
  32 MB of RAM  (64 MB or more if you are going to run a server)
  12 MB of disk space (plus whatever disk space is needed for any additional 
   wrestlers you add)


Miscellany
==========
To change your defalut player name for multiplayer, open the file in the root
pws directory named pwsconfig.py.  In this file there is a line that reads:

playerName = "player1"

Change player1 to whatever you want the name to be (make sure the quotes 
surround the new name) and save the file.  That should do it!


Contact and Troubleshooting
===========================
If you have any questions feel free to send mail to zaxxon@mail.berlios.de

  - The Homepage is at http://pws.berlios.de
  - The Discussion Forums are at http://pwsgame.proboards18.com
  - The Bug Tracker is at http://developer.berlios.de/bugs/?group_id=1098

Enjoy!

John
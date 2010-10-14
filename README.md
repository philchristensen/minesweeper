Flash <-> Python minesweeper clone
==================================

12 October 2010

by Phil Christensen

mailto:phil@bubblehouse.org

10/12/2010
-------------
* Created AppEngine-powered model to represent minefield, handle state changes
    - current minefield is tied to the Google ID of the user
    - if clicking on a cell with no adjacent mines, additional cells are not (yet) uncovered
* Created basic text frontend to test minefield
    - **mine=x,y** GET argument adds mine
    - **reveal=x,y** GET argument indicates a 'click'
    - **hide=x,y** GET argument re-hides an reveald cell
    - **finished=(0|1)** GET argument toggles finished state
* Created preliminary AMF resource
* Created test AMF client script

10/13/2010
----------
* Created CS5-based Flash movie, external ActionScript definition
    - Not yet connecting to server, for some reason.
* Other changes and revisions

10/14/2010
----------
* Switched to using Flex with FlashBuilder for front-end
* Implemented clicking for reveal, option-clicking for set mine
* Added buttons to reset the game (but not the mines), and give up (display the whole board)
	- Reset button doesn't seem to work until manual refresh
Flash <-> Python minesweeper clone
==================================

12 October 2010

by Phil Christensen

mailto:phil@bubblehouse.org

A Minesweeper clone written in Flex with a Google AppEngine back-end.

Usage
-----

On first connect, you'll need to log in to your Google account. Your minefield
is assosicated with that account.

Option (alt) click to set mines in your initially empty minefield. Since the
field is covered, you won't see anything appear. To make creating an initial
minefield easier, click "Reveal Minefield".

When you're done, click "Replay Game" to hide your minefield again. Clicking
field squares will expose either the mine or the number of adjacent mines,
like the original game.

To start over, click "Reset Mines" to reset to an empty minefield.

Notes
-----

Due to time constraints, I didn't finish the following items:

* Unlike the original, this version doesn't reveal the rest of the empty cells when you click on a cell with no adjacent cells.
* Minefield data is saved directly in the Google datastore without caching, so things can be a little slow.
* Game interface is implemented in standard Flex components, not PushButtonEngine sprites.
# Teeko Bot

### Teeko
It is a game between two players on a 5x5 board. Each player has four markers of either red or black. Beginning with black, they take turns placing markers (the "drop phase") until all markers are on the board, with the goal of getting four in a row horizontally, vertically, or diagonally, or in a 2x2 box as shown above. If after the drop phase neither player has won, they continue taking turns moving one marker at a time -- to an adjacent space only

### How to play Teeko2
The Teeko2 rules are almost identical to those of Teeko with one rule exchaned. Specifically, removing the 2x2 box winning condition and replacing it with a diamond winning condition -- the same colored markers at the four corners of a diamond. A diamond is defined by an empty center position surrounded by 4 markers on the spaces above, below, to the right, and to the left of the center.

### Win conditions for Teeko2:
1) Four same colored markers in a row horizontally, vertically, or diagonally.
2) Four same colored markers form a diamond shape as described above.

Using the minimax algorithm, I have developed an AI bot which makes its move in under 5 seconds and beats a random player with about 95% accuracy.

<img src="https://github.com/Kedar-Bhide/Teeko/blob/main/Teeko_board.jpeg" width="200" height="200" />

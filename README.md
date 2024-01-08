# Connect4_Bot
A program that plays Connect 4 as well as I can program it to do

## Game Representation
I wanted to store the data of the game that would make frequent tasks (checking for connect 4, making a turn, etc) as efficient as possible. I landed on using bitboards. A bitboard is a binary string where each bit represents something. For this bot, each bit represents a position on the board:
```
5 12 19 26 33 40 47
4 11 18 25 32 39 46
3 10 17 24 31 38 45
2  9 16 23 30 37 44
1  8 15 22 29 36 43
0  7 14 21 28 35 42
-------------------
0  1  2  3  4  5  6
```
The game is represented by two bitboards (one for each player). If a bit is set, then the player has a token at that position on the board. The full board can be easily accessed by orring the two players boards together:
```
full_board = board[0] | board[1]
```
Additionally, connect fours can be efficiently detected by shifting the board 4 times in the 4 directions (vertical, horizontal, positive diagonal, and negative diagonal) and anding the results. Horizontal example:
```
full_board & full_board << 7 & full_board << 14 & full_board << 21
```
Note: You might have noticed our board representation ignores 6, 13, 20, 27, 34, 41, and 48. We leave these bits permantently unset to prevent a false positive when detecting vertical connect fours

Finally, we also track the turn number, height of each column, and a list of moves to allow for some functions to be simpler and more efficient. For example, tracking the heights of each column allows us to know which bit to set when we make a move, rather than starting from the bottom of the column and looping up until we find an unset bit. 


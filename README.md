# Connect4_Bot
A program that plays Connect 4 as well as I can program it to do

## Game Representation
### The Board
I wanted to store the data of the game that would make frequent tasks (checking for connect 4, making a turn, etc) as efficient as possible. I landed on using bitboards. A bitboard is a binary string where each bit represents something. For this bot, each bit represents a position on the board
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
The game is represented by two bitboards (one for each player). If a bit is set, then the player has a token at that position on the board. The full board can be easily accessed by orring the two players boards together
```
full_board = board[0] | board[1]
```
Additionally, connect fours can be efficiently detected by shifting the board 4 times in the 4 directions (vertical, horizontal, positive diagonal, and negative diagonal) and anding the results. For example, here's the check for a horizontal connect 4
```
full_board & full_board << 7 & full_board << 14 & full_board << 21
```
Note: You might have noticed our board representation ignores 6, 13, 20, 27, 34, 41, and 48. We leave these bits permantently unset to prevent a false positive when detecting vertical connect fours

### Other Data
We also track a few other pieces of data for various reasons.
1. Turn number: Allows easy access to the current player's bitboard and the opponent's bitboard
```
my_board = self.board[self.turn % 2]
opponent_board = self.board[(self.turn + 1) % 2]
```
2. Heights of each column: Allows for moves to be made without finding which bit in the column is the first unset bit
```
.  .  .  .  .  .  .
.  .  .  .  .  .  .
.  .  .  O  .  .  .
.  X  .  X  .  .  .
.  X  O  O  O  .  .
X  O  X  X  X  O  .
--------------------
0  1  2  3  4  5  6

heights = [1, 3, 2, 4, 2, 1, 0]
``` 
3. List of moves: Allows undo move function to know what the previous move was
```
self.undo_move()
```
## Search
Computers are able to process, track, and store data much more efficiently than humans. In order to take advantage of this, we want to implement a function that allows us to calculate every outcome, and pick the move that results in the outcome best for us.

### Scoring an Outcome
We'll use an number to represent how good an outcome is for us. The higher the number, the better for the current player. The lower the number, the worse for the current player.

### Minimax
Since the current player wants to **maximize** their score, they can be descibed as the **maximizer**, while the opponent can be described as the **minimizer**, since they want to **minimize** their score. Thus when searching, we use the **minimax** algorithm. Here is the pseudocode for the minimax algorithm.
```
def minimax(game, maximizer: bool):
  if end of game:
    return score
  else if maximizer:
    best score = -infinity
    for move in possible moves:
      make_move()
      best score = max(best score, minimax(board, false))
      undo_move()
    return best score
  else:
    best score = infinity
    for move in possible moves:
      make_move()
      best score = min(best score, minimax(board, true))
      undo_move()
    return best score
```
### Alpha Beta Pruning
Consider the maximizing player in the middle of a search trying to choose between two moves. All of the possibilities of the first move have been explored, and with perfect play from both sides, the minimizing player can guarentee a score of 5. The second move is currently being explored, and the minimizing player currently knows it can get a score of 3. This means when the search is complete, the second move will give the minimizing player of 3 or less. However, the result of the search is already known without exploring the rest of the second move, since the maximizing player will pick a move that gives score 5 rather than a score that give 3 or less. This concept is known as **alpha beta pruning** and it allows our search to be faster by not exploring useless parts of the game. 

```
def minimax(game, maximizer: bool, alpha=-infinity, beta=infinity):
  if end of game:
    return score
  else if maximizer:
    best score = -infinity
    for move in possible moves:
      make_move()
      best score = max(best score, minimax(board, false), alpha, beta)
      undo_move()
      if best score > beta:
        break
      alpha = max(alpha, best score)
    return best score
  else:
    best score = infinity
    for move in possible moves:
      make_move()
      best score = min(best score, minimax(board, true, alpha, beta))
      undo_move()
      if best score < alpha:
        break
      beta = min(best score, beta)
    return best score
```

### Negamax
Since a good move for the current player is an equally bad move for their opponent, we can simplify our minimax algorithm such that the score is the opposite of the recursive call. This algoritm is called **negamax**, since we negate the opponents score.
```
def negamax(game, alpha=-infinity, beta=infinity):
  if end of game:
    return score
  else:
    best score = -infinity
    for move in possible moves:
      make_move()
      best score = max(best score, -negamax(game, -beta, -alpha))
      undo_move()
      alpha = max(alpha, best score)
      if alpha > beta:
        break
  return best score
```

### Depth
Although computers can compute thousands of calculations in a moment, they are not quick enough to explore the 4.5 trillion possible games of connect four in any reasonable amount of time. Because of this, we need to stop our search at some **depth** 
```
def negamax(game, depth):
  if end of game:
    return score
  elif depth == 0:
    return heuristic evalution
  else:
    best score = -infinity
    for move in possible moves:
      make_move()
      best score = max(best score, -negamax(game, depth - 1))
      undo_move()
  return best score
```
Note because of the addition of depth, we have a base case that is not guarenteed to be a win/loss/tie. Since it is no longer obvious who is winning, we need to create an evalution function to evaluate these mid game positions.

## Heuristic Evaluation
Because we can't search until the end of the game, we need to be able to tell who is winning in the middle of the game. We choose to evaluate from the perspective of the current player.

### Live Threats
Starting with more certain positions, lets look at live threats. A threat is 3 tokens in a row that still has the potential to become 4 in a row, and win the game. A live threat is one of these threats that can be fulfilled by the current player. If the current player has a live threat, we can evaluate the position as a win. If the opponent has 1 live threat, the current player can block it. However, if the opponent has 2+ live threats then we evaluate the position as a loss, since we cannot prevent both in one move.

### Stacked Threats
A stacked threat is two threats on top of each other. They are very advantageous since the player with the stacked threat can play in the column until the opponent is forced to respond to the bottom threat, allowing the player with the stacked threat to win on the top threat. Here is an example of this in a game:
```
.  .  .  .  .  .  .
.  .  .  .  .  .  .
.  .  .  O  .  .  .
.  .  X  X  X  .  .
.  O  O  X  O  .  .
.  O  X  O  O  O  X
--------------------
0  1  2  3  4  5  6
```
In this position, assuming it is player X's turn, they can play in column 5, forcing the opponent to block the horizontal threat, then allowing themself to win on the diagonal threat.

An interesting thing to note about stacked threats is that any threats above them can never be reached (given optimal play), so we do not consider the above threats as valid threats when calculating them.

### Threats
Having more threats than the opponent is generally advantageous, so we add the number of threats to our score, then subtract our opponent's number of threats.

### Center Positions
It is generally a good strategy to occupy the middle of the board when playing connect 4, so we reward our program for making moves in the center. Each position on the board is given a weight. The weight is calculated from the number of possible connect fours through that spot / 10.
```
[
    [.3, .4, .5, .7, .5, .4, .3],
    [.4, .6, .8, 1, .8, .6, .4],
    [.5, .8, 1.1, 1.3, 1.1, .8, .5],
    [.5, .8, 1.1, 1.3, 1.1, .8, .5],
    [.4, .6, .8, 1, .8, .6, .4],
    [.3, .4, .5, .7, .5, .4, .3]
]
```
## Tracking Progress
Throughout the development of this project (and during future development), I have been tracking the progress of the bot by making it by many games against different versions of itself. While these tests do not have massive sample sizes, they show some insight as to how much an additional feature improved the skill of the bot. I did not track every small addition, but I tried to track major ones.

The tests consisted of hundreds/thousands of games and the scores are recorded in this format: 

**opponent1 [WINS, TIES, LOSSES] opponent2 (TOTAL GAMES)**
```
*RANDOM [55411, 254, 44335] RANDOM (100,000)

*NEGAMAX: depth 1, no heuristic [840, 0, 160] RANDOM (1000)
*NEGAMAX: depth 2, no heuristic [964, 1, 35] RANDOM (1000)
*NEGAMAX: depth 3, no heuristic [953, 1, 46] RANDOM (1000)
*NEGAMAX: depth 4, no heuristic [980, 0, 20] RANDOM (1000)

NEGAMAX: depth 4, number threats eval [719, 144, 137] NEGAMAX: depth 4, no heuristic (1000)
NEGAMAX: depth 4, positional eval [879, 42, 79] NEGAMAX: depth 4, no heuristic (1000)
NEGAMAX: depth 4, positional eval, number threats eval [933, 24, 43] NEGAMAX: depth 4, no heuristic (1000)

NEGAMAX: depth 4, live threats, stacked threats, number threats, positional eval [399, 244, 357] NEGAMAX: depth 4, positional eval, number threats eval (1000)

*the first player listed always went first. all other tests had each player play first an equal amount*
```



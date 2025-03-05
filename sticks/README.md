# Sticks game
***Sticks***, also known as ***Chopsticks*** is a simple hand game played with two people. In the variant implemented, each player starts with 1 finger up on each hand. Both players take turns *Attacking* the other players' hands by tapping them, adding the attackers finger count to the opponents. If a hand collects 5 or more points it is considered dead. A dead hand can be "revived" by *Splitting* an even number of fingers between an alive hand and a dead hand. 

[Chopsticks Wikipedia](https://en.wikipedia.org/wiki/Chopsticks_(hand_game))

# Related Prompts
## Rules Prompt
```plaintext
Game Rules:
Two players, Player 1 and Player 2, take turns making one move per turn. Each player has two counters that cannot count exceed 4; if a counter is greater than or equal to 5 then that counter is reset to 0.
On a turn a player can choose one of two actions:
- Attack: Select one of your counters and add its value to an opponent’s counter. You cannot attack with a 0 counter or target a 0 counter. Example: If your counter is 2 and you attack an opponent’s counter with 1, their counter becomes 3, and your counter remains 2.
- Split: Revive a 0 counter by moving half the value of your non-zero, even counter to the 0 counter. You can only split if one counter is 0 and the other is even. Example: If your counters are 0 and 4, after splitting, they become 2 and 2.
The game is over when both of a player's counters are 0, and thus cannot continue to play. The player that does not have both counters at 0 wins the game.

Game State Format:
Game states are represented as [ABCD], where AB are the counters of the player about to move. After a move, AB and CD swap to reflect the opposing player’s counters.

Move Format:
- Attack: "A:Y Z", where A=Attack, Y=your counter letter (A or B), Z=opponent's counter letter (C or D).
- Split: "S:Y", where S=Split, Y=your non-zero, even counter letter (A or B).
```

Using this rules prompt combined with the game state prompt contributed to a significant jump in correct responses from the LLMs tested (ChatGPT 4o, Gemini 2.0 Flash, Claude 3.5 Haiku).

## Game Aware Prompt
```plaintext
You are playing the cutoff and splits variant of the hand game Chopsticks (AKA Splits, Calculator, Sticks).

Game State Format:
Game states are represented as [ABCD], where AB are the counters of the player about to move. After a move, AB and CD swap to reflect the opposing player’s counters.

Move Format:
- Attack: "A:Y Z", where A=Attack, Y=your counter letter (A or B), Z=opponent's counter letter (C or D).
- Split: "S:Y", where S=Split, Y=your non-zero, even counter letter (A or B).
```

All the previous prompts are written in a way that try not to directly or indirectly tell the LLM that it is playing
a well known game. This is to make the LLM rely more on its CoT (Chain of Thought) reasoning abilities more than general knowledge. This prompts can be combined with others and may be helpful for LLMs to further understand the game. While the LLM now knows that the game is Sticks, because there is no standard move/game state format it was provided. Without this format, the prompt produces moves as natural language that cannot be analyzed easily or consistently.

## One-Step Game State Prompt
```plaintext
You are Player 1.  
It’s your turn.  
The current game state is [3401].
What is the best move?
```

This is the game state used in testing becuase it only has 1 best move, that immediately wins the game.

### Correct Response
```plaintext
Move: `A:B D`
Resulting State: `0034` (game over)
```
The move 'A:B D' is the best move in the game state \[3401].
This is the best move as it wins the game for the current player.

## Two-Step Game State Prompt
```plaintext
You are Player 1.  
It’s your turn.  
The current game state is [3321].
What is the best move?
```

This is the game state used in testing becuase it only has 2 best move, that forces the opponents next move. Optimal play will result in a victory for Player 1.

### Correct Response
```plaintext
Move: `A:A C` or `A:B C`
Resulting State: `0133` (opponents next move is forced)
```
The move 'A:A C' and 'A:B C' are the best move in the game state \[3321].

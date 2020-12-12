# Animal Shogi with Reinforcement Learning

Animal Shogi implementation by Gang, Woohyun.

## Differences from official rules

The player who made 1000-days-moves(threefold repetition) loses.
Games are drawn after certain number of turns have passed. We had to implement this rule because of piece reusing system, a game can get indefinitely(but not infinitely) long without repetitions.

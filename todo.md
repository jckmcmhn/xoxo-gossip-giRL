# TODOS

## Key Functionality
- check_for_winner should identify stalemates
    - if X wins -1 (?)
    - if O wins 1
    - if no winner 0 (zero, not "oh", really made a rod for my own back with that one)
    - if stalemate 2
- pass turns_taken into check_for_winner
    - if turns_taken <5 then there can't be a winner yet
    - if turns_taken == 9 and there is no winner that's a stalemate
- script to allow two computer players to play against each other
    - whether either are RL-model based or just pick moves at random should be configurable
- baseline: run two computer players who pick moves at random against eachother. They should be evenly matched

## Documentation
- "user manual" for running the training from scratch

## Nice-To-Haves
- rename "status" to something more descriptive
- check_for_winner should highlight what type of victory it was
    - maybe make a separate version for the training process that doesn't do this
    - prettify_board should display the winning line somehow also
- train a "loser model" where the weights *only* reward losing a match
- train a "winner model" where the weights *only* reward winning a match
    - compare this performance to the model which is rewarded for winning or stalemates
- second baseline: computer player that has some pre-written rules but otherwise chooses at random
    - always pick the middle square if it is available
    - if you have a winning move, always take it
- look into setting up a linter to tidy the code
- apparently the accepted naming convention for git repos uses hyphens
- can probably predict stalemates a turn or two, before they happen, but let's not get ahead of ourselves
- separate file to track model metadata (esp number of episodes)
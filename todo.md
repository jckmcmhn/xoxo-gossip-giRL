# TODOS

## Key Functionality
- check_for_winner should identify stalemates
    - if X wins -1 (?)
    - if O wins 1
    - if no winner 0 (zero, not "oh", really made a rod for my own back with that one)
    - if stalemate 2
- ~~pass turns_taken into check_for_winner~~
    - ~~if turns_taken <5 then there can't be a winner yet~~
    - ~~if turns_taken == 9 and there is no winner that's a stalemate~~
- ~~script to allow two computer players to play against each other~~
    - ~~whether either are RL-model based or just pick moves at random should be configurable~~
- ~~baseline: run two computer players who pick moves at random against eachother. They should be evenly matched~~
- ~~the qmap has duplicates eg [[0, -1, 0], [0, 0, 0], [1, 0, -1]] must remove. many for [[-1, 1, 0], [0, 0, 0], [1, -1, -1]]~~
- ~~it's missing some states? [[0, 1, -1], [1, 0, -1], [-1, 1, -1]] # WRONG, that's a state were -1 already won~~
- Xs and Os is a "solved game". Does the model learn how to play a "perfect" game?

## Documentation
- "user manual" for running the training from scratch

## Nice-To-Haves
- rename "status" to something more descriptive
- change board to state where possible
- check_for_winner should highlight what type of victory it was
    - maybe make a separate version for the training process that doesn't do this
    - prettify_board should display the winning line somehow also
- train a "loser model" where the weights *only* reward losing a match
- train a "winner model" where the weights *only* reward winning a match
    - compare this performance to the model which is rewarded for winning or stalemates
- second baseline: computer player that has some pre-written rules but otherwise chooses at random
    - ~~if you have a winning move, always take it~~
    - if there is a space beside one of your markers and also space beside that, take that
- look into setting up a linter to tidy the code
- ~~apparently the accepted naming convention for git repos uses hyphens~~
- can probably predict stalemates a turn or two before they happen, but let's not get ahead of ourselves
- separate file to track model metadata (esp number of episodes)
- add separate arguments for player 2 model
- log when a player claims the middle square and wins
- get the board to print in same part of screen each time
- implement a version of run_game.py script where the model is not allowed to choose 1,1 as it's first move, for variety
- ~~allow players to use the more intuitive a1, b2, c1 etc for "0,0", "1,1" and "2,0" respectively~~
- Mode to allow p1 and p2 to play against eachother, but sharing the same model dataframe (meaning the model could learn from both sides of the game)
- It is probably not necessary to "build" the empty q-learning table at all. New rows could just be added during training.
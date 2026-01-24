# TODOS

## Key Functionality
- check_for_winner should identify stalemates
    - if X wins -1
    - if O wins 1
    - if no winner 0 (zero, not "oh", really made a rod for my own back with that one)
    - if stalemate 2
- pass turns_taken into check_for_winner
    - if turns_taken <5 then there can't be a winner yet
    - if turns_taken == 9 and there is no winner that's a stalemate

## Nice-To-Haves
- rename "status" to something more descriptive
- check_for_winner should highlight what type of victory it was
    - maybe make a separate version for the training process that doesn't do this
    - prettify_board should display the winning line somehow also
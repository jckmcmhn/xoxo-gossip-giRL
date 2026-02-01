# xoxo-gossip-giRL
My goal with this project is to create and train a simple Reinforcement Learning Model from scratch that is able to play the classic pencil-and-paper game "Xs and Os" (which you may know by the name "Tic-Tac-Toe" or "Noughts and Crosses").

I did this to learn about Reinforcement Learning. That learning is still an ongoing process for me, in RL terms I have many more training episodes to go, so some of the jargon or details may not be entirely correct or "best-in-class". That being said, I am fairly sure that what I've created here is a "model-free" "Q-learning" approach that builds a "policy"<sup>1</sup> using an "Epsilon-Greedy" algorithm. If I've got these terms wrong, please write in.

My interest in this topic was sparked by a [conference](https://www.aiandgamesconference.com/) I attended last year and a great book called ["Artificial Intelligence: A Guide for Thinking Humans"](https://melaniemitchell.me/aibook/) by Melanie Mitchell, I would recommend checking both of them out!

## Try It Out!
### Play Against the Agent
To play against the agent, just run

``python play_against_computer.py``

There is an --opponent (-o) argument for determing which "agent" you play against.
- best: "THE CHAMP!". This is currently best performing agent
- rlhf: This is a copy of THE CHAMP. Your game against it will be used to update its game playing policy through a basic Reinforcement Learning Human Feedback script.
- loser: "LOSER MODE". This agent was trained with the same intensity as THE CHAMP, but was rewarded for losing games and punished for winning them
- rlhf_loser: This is a copy of the LOSER MODE agent. Your game against it will be used to update its game playing policy so that it will start to play better. Could take years though, so not for the faint of heart...
- rules: This agent plays using an incomplete set of rules for playing the game. It doesn't play a perfect game, but it will, for example, always take a winning move if it can. No reinforcement learning was involved in creating this one.
- random: The computer picks (valid) moves at random
- weakly_trained: This agent was very lightly trained. It plays well and outperforms all the other agents except THE CHAMP. This is a work-in-progress to try and identify the configuration of hyperparameters that yields THE CHAMP level performance with the fewest training episodes

If no opponent argument is given, you will play against THE CHAMP.

### Training the Agent
WIP: The script I have for this works but is a little too noisy and involves too many parameters to easily explain at the moment.

### System Requirements
To acknowledge the name for a second... if you ain't got no money your broke-ass can stay right where it is as a matter of fact, because I don't think any of this is particularly taxing on your computer's hardware.
I developed all of this on what I'd say is an entry-level pre-built gaming PC from a few years ago and had no issues running anything.

## The Algorithm

The way this learning algorithm works is as follows:
- Players play until the game ends, either p1 wins, p2 wins or 9 moves are made without anyone winning<sup>2</sup>.
- If one or both players are set as learning agents:
 - If a reward has been configured for winning, the script takes the winning player's actions and works backwards through them. The last action gets the full reward value, the one before that gets slightly less of the reward value and so on
 - If a reward has been configured for losing or draws, the same process is carried out.
 - This should mean that moves that win the game have very high values and the moves that led up to that position should have relatively high values also
  - For example, while I could not always get the policies to take a corner piece on the first turn (which is apparently the 'correct' move) they did consistently favour the middle square on the first move
 - Moves taken right before an opponent made a winning move should have very low values and the moves that led up to that position such have relatively low values
 - Moves that lead to draws (which I have tended to reward slightly less than winning) should have values in the middle

## Corrections and Know Issues
### Theory
I realised a little too late into the project that I'd slightly misunderstood some of the theory.

From my reading, it seems that the usual thing to do is to update the q-table per iteration (at the end of each turn), not per episode which is what I'm doing here.
On the other hand:
 - Xs and Os is strictly linear. Within a single game, there is no way to find yourself back at a position you were in previously, so I would argue there's no need to update the policy before a game is over
 - Players can make at max 5 or 4 moves per game, so it is not as if a lot of iterations pass before each update anyway

The process I have for updating the values, at the moment, is just halving the reward at each step and adding it to the current value, none of that fancy "big city" _temporal distance learning_ for me, thanks.

### Clever Maths Stuff
- I suspect there's probably some clever mathematical nuances in the difference between a reward and value that I've kind of lost here.
- I'm sure there's a clever mathematical way to represent an Xs and Os board or at least to compress down the list of possible states.

### Why does THE CHAMP always pick the middle square
This bothers me as well. According to the XOXOlogists out there, the "perfect" first move is a corner square. Previous policies have picked up on that but otherwise played badly. More training, hyperparameter tuning and maybe even changes to the algorithm will be needed to figure this one out.
There is maybe an argument to be made that the middle sqaure is the best first square for X _unless_ you're playing against someone who always plays a perfect game as O, but that's a whole other thing.


<sup>1</sup>: Which at time of writing I believe I have wrongly referred to as a "model" in numerous places, that's on the to-do list to fix.
<sup>2</sup>: I realise it's possible to identify if a draw will happen sooner than this, that's also on the to-do list

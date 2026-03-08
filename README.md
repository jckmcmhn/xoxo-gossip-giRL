# xoxo-gossip-giRL
My goal with this project is to create and train a simple Reinforcement Learning Model from scratch that is able to play the classic pencil-and-paper game "Xs and Os" (which you may know by the name "Tic-Tac-Toe" or "Noughts and Crosses").

I did this to learn about Reinforcement Learning. That learning is still an ongoing process for me, in RL terms I have many more training episodes to go, so some of the jargon or details may not be entirely correct or "best-in-class". That being said, I am fairly sure that what I've created here is a "model-free" approach which uses an "Epsilon-Greedy" algorithm. If I've got these terms wrong, please write in.

My recent interest in this topic was sparked by attending the [2025 AI and Games Conference](https://www.aiandgamesconference.com/) where I saw a lot of really interesting talks on Reinforcement Learning and by reading a great book called ["Artificial Intelligence: A Guide for Thinking Humans"](https://melaniemitchell.me/aibook/) by Melanie Mitchell. I would recommend checking both of them out!

I've since made another, more streamlined, less hubristic, attempt at this idea, [here it is](https://github.com/jckmcmhn/xo-gymnasium).

## Try It Out!
### Play Against the Agent
To play against the agent, just run

``python play_against_computer.py``

There is an --opponent (-o) argument for determing which "agent" you play against.
- best: **"THE CHAMP!"**. This is the currently best performing agent
- rlhf: This is a copy of **THE CHAMP**. Your game against it will be used to update its game playing policy.
- loser: **"LOSER MODE"**. This agent was trained with the same intensity as **THE CHAMP**, but was rewarded for losing games and punished for winning them
- rlhf_loser: This is a copy of the **LOSER MODE** agent. Your game against it will be used to update its game playing policy so that it will start to play better. Could take years though, so not for the faint of heart...
- rules: This agent plays using an incomplete set of rules for playing the game. It doesn't play a perfect game, but it will, for example, always take a winning move if it can. No reinforcement learning was involved in creating this one.
- random: The computer picks (valid) moves at random
- weakly_trained: This agent was very lightly trained. It plays well and outperforms all the other agents except **THE CHAMP**. This is a work-in-progress to try and identify the configuration of hyperparameters that yields **THE CHAMP** level performance with the fewest training episodes

If no opponent argument is given, you will play against **THE CHAMP**.

### Training the Agent
WIP: The script I have for this works but is a little too noisy and involves too many parameters to easily explain at the moment.

### System Requirements
To acknowledge the name for a second... if you ain't got no money your broke-ass can stay right where it is as a matter of fact, because I don't think any of this is particularly taxing on your computer's hardware.
I developed all of this on what I'd say is an entry-level pre-built gaming PC from a few years ago and had no issues running anything.

## The Algorithm

The way this learning algorithm works is as follows:
- At the start of the training process a table is initialised containing every possible state-action pair. Each state-action pair is given an initial value of 0
- Players play until the game ends, either p1 wins, p2 wins or 9 moves are made without anyone winning<sup>1</sup>.
- If one or both players are set as learning agents:
  - If a reward has been configured for winning, the script takes the winning player's state-action pairs and works backwards through them. The last state-action gets the full reward value, the one before that gets slightly less of the reward value and so on
  - If a reward has been configured for losing or draws, the same process is carried out.
  - This should mean that moves that win the game have very high values and the moves that led up to that position should have relatively high values also
    - For example, while I could not always get the policies to take a corner piece on the first turn (which is apparently the 'correct' move) they did consistently favour the middle square on the first move
  - Moves taken right before an opponent made a winning move should have very low values and the moves that led up to that position should have relatively low values
  - Moves that lead to draws (which I have tended to reward slightly less than winning) should have values in the middle
- The training process follows an epsilon-greedy algorithm: the learning agent makes most of its moves at random at the start of the process, but overtime it uses the currently best rated action in the table when making its moves

## Corrections and Know Issues
### Theory
I realised a little too late into the project that I'd oversimplified a lot of the theory.

However, in "Reinforcement Learning: An Introduction" by Richard S. Sutton and Andrew G. Barto, the authors say the following (emphasis mine):

> the basic idea \[of reinforcement learning\] is simply to capture the most important aspects of the real problem facing a learning agent interacting with its environment to achieve a goal. Clearly, such an agent must be able to sense the state of the environment to some extent and must be able to take actions that affect the state. The agent also must have a goal or goals relating to the state of the environment.... *Any method that is well suited to solving this kind of problem we consider to be a reinforcement learning method*

The script does learn how to play Xs and Os (albeit not perfectly, see below) so I'd consider this a (partial) success.

I think what I have here is a very dumbed-down Q-learning approach. But based on my reading, Q-learning usually updates the q-value a state-action pair after each step, not each episode as I've done here.
However:
- Xs and Os is strictly linear. Within a single game, there is no way to find yourself back at a position you were in previously, so I would argue there's no need to update the policy before a game is over
- Players can make at max 5 or 4 moves per game, so it is not as if a lot of iterations pass before each update anyway

The process I have for updating the values, at the moment, is just halving the reward at each step and adding it to the current value, none of that fancy "big city" _temporal distance learning_ for me, thanks.

### Clever Maths Stuff
- As mentioned I suspect there's probably some clever mathematical nuances in the difference between a reward and value that I've kind of lost here.
- I'm sure there's a clever mathematical way to represent an Xs and Os board or at least to compress down the list of possible states.

### Why does **THE** CHAMP always pick the middle square?
This bothers me as well. According to the XOXOlogists out there, the "perfect" first move is a corner square. Previous policies have picked up on that but otherwise played badly. More training, hyperparameter tuning and maybe even changes to the algorithm will be needed to figure this one out.

There is maybe an argument to be made that the middle sqaure is the best first square for X when you're playing against an average player and that a corner square is the best choice if playing against a player who always plays "perfectly", but that's a whole other thing.

<sup>1</sup>: I realise it's possible to identify if a draw will happen sooner than this, that's on the to-do list

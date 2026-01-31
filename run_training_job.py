import argparse
from xo_functions import Player
from training_functions import run_training_loop
import datetime
start = datetime.datetime.now()
print(start)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_file", help = "What file are you using to load the model weights?")
parser.add_argument("-o", "--out_file", help = "What file are you using to save the model weights?")
parser.add_argument("-n", "--number_of_episodes", help = "How many training episodes to run?")
parser.add_argument("-r", "--rewards", help = "What rewards are applied. Format: w|l|d Sample: '[20|-10|10]' ")
parser.add_argument("-e", "--epsilon", help = "todo")

# Read arguments from command line
args = parser.parse_args()


in_file = args.in_file
out_file = args.out_file
n = int(args.number_of_episodes)
epsilon = float(args.epsilon)
rewards = args.rewards.replace("[","").replace("]","").split("|")
reward_win, reward_lose, reward_draw = rewards
reward_win, reward_lose, reward_draw = float(reward_win), float(reward_lose), float(reward_draw)
rewards = [reward_win, reward_lose, reward_draw]

training = True #TODO: Make argument
if training:
    # For now, always make P1 the model player you are most interested in assesing, with p2 as the benchmark
    p1 = Player("Tom Cruise's character from Live Die Repeat / Edge Of Tomorrow (P1)","LEARNING", in_file, out_file, epsilon, rewards)
    p1.greet()
    p2 = Player("Gregg (P2)","FIXED")
    #p2 = Player("Al (P2)",file,"RULES_IMPERFECT")
    p2.greet()
    p1_wins, p2_wins, draws, training_headline = run_training_loop(p1, p2, n, "ALTERNATE", 0)

print("\n------------\n")
print("VALIDATION STEP")
print("\n------------\n")
n_validation = int(n / 10) # Hope this doesn't "nvalidate" the training approach!

#print("Introducing... the challenger!")
test = 0
p1_validation_wins = 0
p1_validation_loses = 0
validation_draws = 0
validation_headlines = []

test += 1
print("\n----------")
print(f"TEST {test}: Trained model vs untrained model")
print("----------")
p1 = Player("Tom (P1)","FIXED", out_file)
p1.greet()
p2 = Player("Gregg (P2)","FIXED")
p2.greet()
p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, int(n / 10), "ALTERNATE", 0)
p1_validation_wins += p1_wins
p1_validation_loses += p2_wins
validation_draws += draws
validation_headlines.append(headline)

test += 1
print("\n----------")
print(f"TEST {test}: Trained model vs imperfect rules")
print("----------")
p1 = Player("Tom (P1)","FIXED", out_file)
p1.greet()
p2 = Player("Al (P2)","RULES_IMPERFECT")
p2.greet()
p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, int(n / 10), "ALTERNATE", 0)
p1_validation_wins += p1_wins
p1_validation_loses += p2_wins
validation_draws += draws
validation_headlines.append(headline)

test += 1
print("\n----------")
print(f"TEST {test}: Trained model vs imperfect rules")
print("----------")
p1 = Player("Tom (P1)","FIXED", out_file)
p1.greet()
p2 = Player("Al (P2)","RULES_IMPERFECT_NOT_LOCKED_IN")
p2.greet()
p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, int(n / 10), "ALTERNATE", 0)
p1_validation_wins += p1_wins
p1_validation_loses += p2_wins
validation_draws += draws
validation_headlines.append(headline)

test += 1
print("\n----------")
print(f"TEST {test}: Trained model vs weakly trained model")
print("----------")
p1 = Player("Tom (P1)","FIXED", out_file)
p1.greet()
p2 = Player("Hennimore (P2)","FIXED", "weakly_trained.csv")
p2.greet()
p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, int(n / 10), "ALTERNATE", 0)
p1_validation_wins += p1_wins
p1_validation_loses += p2_wins
validation_draws += draws
validation_headlines.append(headline)
# python .\run_training_job.py -i blank_q_learning_table.csv -o weakly_trained.csv --reward '[10|0|5]' -e 70 -n 100

print(f"\nFor this experiment, there were {n} training episodes and {n_validation} validation episodes, epsilon was {epsilon}, the win reward was {reward_win}, the loss reward was {reward_lose} and the draw reward was {reward_draw}\n")
print(f"Across {test * n_validation} validation episodes, p1 won {p1_validation_wins} times ({100 * round(p1_validation_wins / (test * n_validation), 2)}%)")
print(f"Across {test * n_validation} validation episodes, p1 lost {p1_validation_loses} times ({100 * round(p1_validation_loses / (test * n_validation), 2)}%)")
print(f"Across {test * n_validation} validation episodes, there were {validation_draws} draws ({100 * round(validation_draws / (test * n_validation), 2)}%)")

if training:
    print("\nHere is how the model performed in training:")
    print(training_headline)

print("\nHere is how the model performed in validation:")
for validation_headline in validation_headlines:
    print(validation_headline)

end = datetime.datetime.now()
print(end - start)
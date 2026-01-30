import argparse
from xo_functions import Player
from training_functions import run_training_loop

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "What file are you using to load or save the model weights?")
parser.add_argument("-n", "--number_of_episodes", help = "How many training episodes to run?")
parser.add_argument("-r", "--rewards", help = "What rewards are applied. Format: w|l|d Sample: '[20|-10|10]' ")
parser.add_argument("-e", "--epsilon", help = "todo")

# Read arguments from command line
args = parser.parse_args()


file = args.file
n = int(args.number_of_episodes)
epsilon = float(args.epsilon)
rewards = args.rewards.replace("[","").replace("]","").split("|")
reward_win, reward_lose, reward_draw = rewards
reward_win, reward_lose, reward_draw = float(reward_win), float(reward_lose), float(reward_draw)
rewards = [reward_win, reward_lose, reward_draw]

# For now, always make P1 the model player you are most interested in assesing, with p2 as the benchmark
p1 = Player("Tom (P1)",file,"LEARNING", epsilon, rewards)
p2 = Player("Gregg (P2)","blank_q_learning_table.csv","FIXED")
#p2 = Player("Al (P2)",file,"RULES_IMPERFECT")


run_training_loop(p1, p2, n, "ALTERNATE", 0)

print("\n------------\n")
print("VALIDATION STEP")
p1 = Player("Tom (P1)",file,"FIXED")
p2 = Player("Gregg (P2)","blank_q_learning_table.csv","FIXED")
run_training_loop(p1, p2, int(n / 10), "ALTERNATE", 0)

print(f"For this experiment, there were {n} training episodes and {int(n / 10)} validation episodes, epsilon was {epsilon}, the win reward was {reward_win}, the loss reward was {reward_lose} and the draw reward was {reward_draw}")
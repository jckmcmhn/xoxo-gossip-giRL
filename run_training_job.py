import argparse
from xo_functions import Player
from training_functions import run_training_loop

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "What file are you using to load or save the model weights?")
parser.add_argument("-n", "--number_of_episodes", help = "How many training episodes to run?")
parser.add_argument("-r", "--rewards", help = "What rewards are applied. Format: w|l|d Sample: '20|-10|10' ")
parser.add_argument("-e", "--epsilon", help = "todo")

# Read arguments from command line
args = parser.parse_args()


file = args.file
n = int(args.number_of_episodes)
epsilon = args.epsilon
rewards = args.rewards.split("|")
reward_win, reward_lose, reward_draw = rewards
reward_win, reward_lose, reward_draw = float(reward_win), float(reward_lose), float(reward_draw)

p1 = Player("Tom (P1)",file,"LEARNING", reward_win)
p2 = Player("Al (P2)",file,"RULES_IMPERFECT")


run_training_loop(p1, p2, n, epsilon)
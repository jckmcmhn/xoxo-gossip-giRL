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
parser.add_argument("-t", "--training", help = "Are you training a model in this run: 0 for Validate Model Only, 1 for Train Model Only, 2 for Train and Validate Model")

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
n = int(args.number_of_episodes)
training = int(args.training)


if training > 0:
    print("Training")
    # For now, always make P1 the model player you are most interested in assesing, with p2 as the benchmark
    #p1 = Player("Tom Cruise's character from Live Die Repeat / Edge Of Tomorrow (P1)","LEARNING", in_file, out_file, epsilon, rewards)
    p1 = Player("Tom Cruise's character from Live Die Repeat / Edge Of Tomorrow (P1)","LEARNING_SHARING", in_file, out_file, epsilon, rewards)
    p1.greet()
    #p2 = Player("Gregg (P2)","FIXED", "experiments/20260131_new_champ_15.csv")
    p2 = Player("Bill Murray in GroundHog Day (P1)","LEARNING_SHARING", in_file, out_file, epsilon, rewards)
    #p2 = Player("Tom Cruise's character from Live Die Repeat / Edge Of Tomorrow (P1)","LEARNING", in_file, out_file, epsilon, rewards)
    #p2 = Player("Al (P2)",file,"RULES_IMPERFECT")
    p2.greet()
    p1_wins, p2_wins, draws, training_headline = run_training_loop(p1, p2, n, "ALTERNATE", 0)

if training != 1:
    print("\n------------\n")
    print("VALIDATION STEP")
    print("\n------------\n")
    if n > 2000:
        n_validation = 2000 # Hope this doesn't "nvalidate" the training approach!
    else:
        n_validation = int(n / 10) # "nvalidate", it's one letter off invalidate, do you get it?


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
    p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, n_validation, "ALTERNATE", 0)
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
    p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, n_validation, "ALTERNATE", 0)
    p1_validation_wins += p1_wins
    p1_validation_loses += p2_wins
    validation_draws += draws
    validation_headlines.append(headline)

    test += 1
    print("\n----------")
    print(f"TEST {test}: Trained model vs distracted imperfect rules")
    print("----------")
    p1 = Player("Tom (P1)","FIXED", out_file)
    p1.greet()
    p2 = Player("Al (P2)","RULES_IMPERFECT_NOT_LOCKED_IN")
    p2.greet()
    p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, n_validation, "ALTERNATE", 0)
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
    p2 = Player("Hennimore (P2)","FIXED", "experiments/weakly_trained.csv")
    p2.greet()
    p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, n_validation, "ALTERNATE", 0)
    p1_validation_wins += p1_wins
    p1_validation_loses += p2_wins
    validation_draws += draws
    validation_headlines.append(headline)
    # python .\run_training_job.py -i blank_q_learning_table.csv -o weakly_trained.csv --reward '[10|0|5]' -e 70 -n 100

    test += 1
    print("\n----------")
    print(f"TEST {test}: Trained model vs the champ")
    print("----------")
    p1 = Player("Tom (P1)","FIXED", out_file)
    p1.greet()
    p2 = Player("The Champ (P2)","FIXED", "experiments/the_champ.csv")
    p2.greet()
    p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, n_validation, "ALTERNATE", 0)
    p1_validation_wins += p1_wins
    p1_validation_loses += p2_wins
    validation_draws += draws
    validation_headlines.append(headline)

    #test += 1
    print("\n----------")
    print(f"Extra Test: Trained model vs itself. Not counted in final metrics") # This test is interesting, but makes the final totals harder to make sense of
    print("----------")
    p1 = Player("Tom (P1)","FIXED", out_file)
    p1.greet()
    p2 = Player("Tom (P2)","FIXED", out_file)
    p2.greet()
    p1_wins, p2_wins, draws, headline = run_training_loop(p1, p2, n_validation, "ALTERNATE", 0)



    print("# THE HEADLINES")
    print(f"\nFor this experiment, there were {n} training episodes and {n_validation} validation episodes per benchmark, epsilon was {epsilon}, the win reward was {reward_win}, the loss reward was {reward_lose} and the draw reward was {reward_draw}\n")
    print(f"Across {test * n_validation} validation episodes, p1 won {p1_validation_wins} times ({100 * round(p1_validation_wins / (test * n_validation), 2)}%)")
    print(f"Across {test * n_validation} validation episodes, p1 lost {p1_validation_loses} times ({100 * round(p1_validation_loses / (test * n_validation), 2)}%)")
    print(f"Across {test * n_validation} validation episodes, there were {validation_draws} draws ({100 * round(validation_draws / (test * n_validation), 2)}%)")

    if training:
        print("\nHere is how the model performed in training:")
        # A training agent will spend quite a lot of its training episodes making random moves.
        # So this figure should give some indication that the agent can now perform better than random guesses, but an "all policy all the time" test is needed to get the true performance
        print(training_headline)

    print("\nHere is how the model performed in validation:")
    for validation_headline in validation_headlines:
        print(validation_headline)

    end = datetime.datetime.now()
    print(end - start)
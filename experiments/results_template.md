# Experiment date:
2026-01-31
# Branch:
Development
# Goal:

# Conclusion:

# How was weakly trained created:
python .\run_training_job.py -i blank_q_learning_table.csv -o weakly_trained.csv --reward '[10|0|5]' -e 70 -n 100

# Who is "the champ":
Currently: 20260131_1_results.md which is not checked in yet

# How was the experiment done:
python .\run_training_job.py -o experiments/20260131_4_well_trained.csv -i blank_q_learning_table.csv --reward '[10|-10|5]' -e 70 -n 5000

# Headlines:

# Full Print Out

import random


def run_random_ballot_election(vote_array):
    return (random.choice(vote_array)).get_ballot()

import random
from random import randrange

import main
from Candidate import Candidate
from Vote import Vote


def generate_random_vote_array(amount, complete=False):
    ret = []
    for i in range(amount):
        length = randrange(1, main.candidate_num + 1) if not complete else main.candidate_num
        temp_list = list(range(0, main.candidate_num))
        temp_ret = []

        for j in range(length):
            a = randrange(len(temp_list))
            temp_ret.append(temp_list[a])
            temp_list.pop(a)
        if length < main.candidate_num:
            b = randrange(len(temp_list))
            ret.append(Vote(temp_ret, temp_list[b]))
        else:
            ret.append(Vote(temp_ret))

    return ret


def generate_candidate_list(ideology_array=None):
    if ideology_array is not None:
        return [Candidate(y, x, ideology_array[x]) for x, y in enumerate(main.candidate_names)]
    return [Candidate(y, x, [random.random(), random.random()]) for x, y in enumerate(main.candidate_names)]


def generate_informed_vote_array(amount, candidate_list):
    x_list = [x / amount for x in list(range(0, amount + 1))]
    y_list = [x / amount for x in list(range(0, amount + 1))]
    ret = []
    for i in range(amount):
        x = randrange(len(x_list))
        y = randrange(len(y_list))
        ideology = [x_list[x], y_list[y]]
        x_list.pop(x)
        y_list.pop(y)
        distance_list = []
        for candidate in candidate_list:
            distance_list.append(((ideology[0] - candidate.get_ideology()[0]) ** 2 + (ideology[1] - candidate.get_ideology()[1]) ** 2) ** (1 / 2))
        support_list = [y.get_index() for y in sorted([candidate_list[j] for j in range(main.candidate_num) if distance_list[j] <= 0.3], key=lambda x: distance_list[x.get_index()])]
        hated_candidate = max(range(len(distance_list)), key=distance_list.__getitem__)
        ret.append(Vote(support_list, hated_candidate, ideology))

    return ret

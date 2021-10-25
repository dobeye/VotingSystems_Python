from random import randrange

import main
from Candidate import Candidate
from Vote import Vote


def generate_random_vote_array(amount):
    ret = []
    candidate_list = generate_candidate_list()
    for i in range(amount):
        length = randrange(1, len(candidate_list) + 1)
        temp_list = list(range(0, len(candidate_list)))
        temp_ret = []

        for j in range(length):
            a = randrange(len(temp_list))
            temp_ret.append(temp_list[a])
            temp_list.pop(a)
        if length < len(candidate_list):
            b = randrange(len(temp_list))
            ret.append(Vote(temp_ret, temp_list[b]))
        else:
            ret.append(Vote(temp_ret))

    return ret


def generate_random_complete_vote_array(amount):
    ret = []
    candidate_list = generate_candidate_list()
    for i in range(amount):
        temp_list = list(range(0, len(candidate_list)))
        temp_ret = []

        for j in range(main.candidate_num):
            a = randrange(len(temp_list))
            temp_ret.append(temp_list[a])
            temp_list.pop(a)
        ret.append(Vote(temp_ret))

    return ret


def generate_candidate_list():
    return [Candidate(y, x) for x, y in enumerate(main.candidate_names)]

import itertools
import random
import Utils
import main
from copy import deepcopy


class ScoreBasedElectionMethods:

    @staticmethod
    def run_copeland_election(vote_array):
        ret = deepcopy(main.candidate_list)
        for index, candidate in enumerate(ret):
            for opponent in ret[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                if temp_array[0] > temp_array[1]:
                    candidate.add_support(1)
                    continue
                if temp_array[1] > temp_array[0]:
                    opponent.add_support(1)
                    continue
                candidate.add_support(0.5)
                opponent.add_support(0.5)

        return ret

    class MinMaxMethods:

        @staticmethod
        def run_min_max_winning_election(vote_array):

            ret = deepcopy(main.candidate_list)
            for index, candidate in enumerate(ret):
                for opponent in ret[(index + 1):]:
                    temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                    if temp_array[0] > temp_array[1]:
                        if -temp_array[0] < opponent.get_support():
                            opponent.set_support(-temp_array[0])
                    if temp_array[1] > temp_array[0]:
                        if -temp_array[1] < candidate.get_support():
                            candidate.set_support(-temp_array[1])

            Utils.election_results_curve(ret)

            return ret

        @staticmethod
        def run_min_max_margin_election(vote_array):

            ret = deepcopy(main.candidate_list)
            for index, candidate in enumerate(ret):
                for opponent in ret[(index + 1):]:
                    temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                    if temp_array[0] > temp_array[1]:
                        if -temp_array[0] + temp_array[1] < opponent.get_support():
                            opponent.set_support(-temp_array[0] + temp_array[1])
                    if temp_array[1] > temp_array[0]:
                        if -temp_array[1] + temp_array[0] < candidate.get_support():
                            candidate.set_support(-temp_array[1] + temp_array[0])

            Utils.election_results_curve(ret)

            return ret

        @staticmethod
        def run_min_max_pairwise_opposition_election(vote_array):

            ret = deepcopy(main.candidate_list)
            for index, candidate in enumerate(ret):
                for opponent in ret[(index + 1):]:
                    temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())
                    opponent.set_support(min(opponent.get_support(), -temp_array[0]))
                    candidate.set_support(min(candidate.get_support(), -temp_array[1]))

            Utils.election_results_curve(ret)

            return ret

    @staticmethod
    def run_anti_plurality_election(vote_array):
        ret = deepcopy(main.candidate_list)
        for vote in vote_array:
            if vote.get_hated_candidate() != -1:
                ret[vote.get_hated_candidate()].add_support(-1)

        Utils.election_results_curve(ret)

        return ret

    @staticmethod
    def run_approval_election(vote_array):
        ret = deepcopy(main.candidate_list)
        for vote in vote_array:
            for support in vote.get_ballot():
                ret[support].add_support(1)

        return ret

    @staticmethod
    def run_borda_election(vote_array):
        return Utils.borda_count(vote_array, deepcopy(main.candidate_list))

    @staticmethod
    def run_nauru_election(vote_array):
        return Utils.borda_count(vote_array, deepcopy(main.candidate_list), lambda x: 1 / (x + 1))

    @staticmethod
    def run_fptp_election(vote_array):
        ret = deepcopy(main.candidate_list)
        for vote in vote_array:
            ret[vote.get_ballot_at(0)].add_support(1)
        return ret

    majority_judgment_methods = {"Typical": (lambda t: t[0] + t[1] - t[2]),
                                 "Usual": (lambda t: t[0] + 0.5 * (t[1] - t[2]) / (1 - t[1] - t[2])),
                                 "Central": (lambda t: t[0] + 0.5 * (t[1] - t[2]) / (t[1] + t[2] + 0.0001))}

    @staticmethod
    def run_majority_judgement_election(vote_array, judgement_method=None):
        candidate_list = deepcopy(main.candidate_list)
        judgement_matrix = Utils.majority_judgement_matrix(vote_array)

        if judgement_method is None:
            while True:
                median_matrix = []
                for candidate in judgement_matrix:
                    median_matrix.append(Utils.find_list_median(candidate))
                max_median_score = max(median_matrix)

                if median_matrix.count(max_median_score) == 1:
                    for index, candidate in enumerate(candidate_list):
                        candidate.set_support(median_matrix[index])
                    return candidate_list

                for candidate in judgement_matrix:
                    try:
                        candidate.remove(max_median_score)
                    except ValueError:
                        pass
        elif type(judgement_method) is str:
            for index, candidate in enumerate(candidate_list):
                candidate.set_support(
                    ScoreBasedElectionMethods.majority_judgment_methods[judgement_method](
                        Utils.mj_median_proponents_opponents(judgement_matrix, index, len(vote_array))))

            return candidate_list
        else:
            for index, candidate in enumerate(candidate_list):
                candidate.set_support(
                    judgement_method(Utils.mj_median_proponents_opponents(judgement_matrix, index, len(vote_array))))

            return candidate_list


class AlternativeElectionMethods:

    @staticmethod
    def run_alternative_copeland_election(vote_array):
        ret = deepcopy(main.candidate_list)
        for candidate in ret:
            for opponent in ret[(candidate.get_index() + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())
                if temp_array[0] >= temp_array[1]:
                    candidate.add_support(1)
                if temp_array[1] >= temp_array[0]:
                    opponent.add_support(1)

        return ret

    @staticmethod
    def run_sequential_pairwise_election(vote_array):
        ret = deepcopy(main.candidate_list)
        contender = 0
        for i in range(1, len(ret)):
            temp_array = Utils.pairwise_comparison(vote_array, contender, i)

            if temp_array[0] == temp_array[1]:
                ret[i].set_support(ret[contender].get_support())
            elif temp_array[0] > temp_array[1]:
                ret[contender].add_support(1)
            elif temp_array[0] < temp_array[1]:
                ret[i].set_support(ret[contender].get_support() + 1)
                contender = i

        return ret

    @staticmethod
    def run_alternative_tideman_election(vote_array):
        candidate_list = deepcopy(main.candidate_list)
        ret = []
        for v in range(len(candidate_list)):
            while True:
                for candidate in candidate_list:
                    candidate.set_support(0)

                current_smith_set = Utils.smith_set_in_adjacency_matrix(
                    Utils.generate_adjacency_matrix(vote_array, candidate_list))
                if len(current_smith_set) == 1:
                    ret += current_smith_set
                    break

                for candidate in candidate_list:
                    candidate.set_validity(False)
                for i in current_smith_set:
                    candidate_list[i].set_validity(True)

                Utils.plurality_count(vote_array, candidate_list)
                min([x for x in candidate_list if x.get_validity()]).set_validity(False)

            for candidate in candidate_list:
                candidate.set_validity(True)
            for i in ret:
                candidate_list[i].set_validity(False)

        return ret

    @staticmethod
    def run_bucklin_election(vote_array):
        ret = deepcopy(main.candidate_list)
        for i in range(main.candidate_num):
            for vote in vote_array:
                if vote.check_validity_at(i):
                    ret[vote.get_ballot_at(i)].add_support(1)

            for candidate in ret:
                if candidate.get_support() > len(vote_array) / 2:
                    return ret

        return ret

    @staticmethod
    def run_alt_fptp_election(vote_array):
        ret = deepcopy(main.candidate_list)
        temp_array = vote_array
        Utils.plurality_count(temp_array, ret)
        return ret

    @staticmethod
    def run_random_ballot_election(vote_array):
        return (random.choice(vote_array)).get_ballot()


class PermutationElectionMethods:

    @staticmethod
    def run_kemeny_young_election(vote_array):
        pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array)

        ret = 0
        ret_support = 0
        for permutation in list(itertools.permutations(list(range(main.candidate_num)))):
            results_contender = permutation
            contender_support = 0
            for index, winner in enumerate(permutation):
                for loser in permutation[(index + 1):]:
                    contender_support += pairwise_support_matrix[winner][loser]

            if contender_support > ret_support:
                ret = results_contender
                ret_support = contender_support

        return ret

    @staticmethod
    def run_ranked_pairs_election(vote_array):
        candidate_list = [True for _ in range(main.candidate_num)]
        election_permutation = []

        for v in range(main.candidate_num):
            pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array, candidate_list)

            for i in range(main.candidate_num):
                while True:
                    min_cycle_win = Utils.pairwise_support_cycle_check(i, i, pairwise_support_matrix, [], 0)
                    if min_cycle_win == -1:
                        break
                    else:
                        pairwise_support_matrix[min_cycle_win[0]][min_cycle_win[1]] = \
                            pairwise_support_matrix[min_cycle_win[1]][min_cycle_win[0]] = 0

            for i in range(main.candidate_num):
                if candidate_list[i]:
                    if all(pairwise_support_matrix[j][i] <= pairwise_support_matrix[i][j] for j in
                           range(main.candidate_num)):
                        election_permutation.append(i)
                        candidate_list[i] = False

        return election_permutation

    @staticmethod
    def run_schulze_election(vote_array):
        candidate_list = list(range(main.candidate_num))
        ret = [0 for _ in range(main.candidate_num)]

        distance_strength_matrix = Utils.generate_adjacency_matrix(vote_array)

        for i in range(main.candidate_num):
            for j in range(main.candidate_num):
                if i != j:
                    for k in range(main.candidate_num):
                        if k != i and k != j:
                            distance_strength_matrix[j][k] = max(distance_strength_matrix[j][k], min(distance_strength_matrix[j][i], distance_strength_matrix[i][k]))

        for x in candidate_list:
            for y in candidate_list[(x + 1):]:
                if distance_strength_matrix[x][y] > distance_strength_matrix[y][x]:
                    ret[x] += 1
                else:
                    ret[y] += 1

        return sorted(candidate_list, key=lambda t: ret[t], reverse=True)

    @staticmethod
    def run_permutation_sequential_pairwise_election(vote_array):
        candidate_list = [True for _ in range(main.candidate_num)]
        election_permutation = []
        for i in range(main.candidate_num):
            contender = 0
            for j in range(1, main.candidate_num):
                temp_array = Utils.pairwise_comparison(vote_array, contender, j, candidate_list)
                if temp_array[0] < temp_array[1]:
                    contender = j

            election_permutation.append(contender)
            candidate_list[contender] = False

        return election_permutation

    @staticmethod
    def run_copeland_election(vote_array):
        ret = [0 for _ in range(main.candidate_num)]
        for candidate in range(main.candidate_num):
            for opponent in range(candidate + 1, main.candidate_num):
                temp_array = Utils.pairwise_comparison(vote_array, candidate, opponent)

                if temp_array[0] > temp_array[1]:
                    ret[candidate] += 1
                    continue
                if temp_array[1] > temp_array[0]:
                    ret[opponent] += 1
                    continue
                ret[candidate] += 0.5
                ret[opponent] += 0.5

        print(ret)
        return sorted(list(range(main.candidate_num)), key=lambda t: ret[t], reverse=True)


class RunoffElectionMethods:

    @staticmethod
    def run_coombs_election(vote_array):
        ret = deepcopy(main.candidate_list)

        for i in range(len(ret) - 2, 0, -1):
            Utils.plurality_count(vote_array, ret)
            counted_votes = 0
            for candidate in ret:
                counted_votes += candidate.get_support()

            for candidate in ret:
                if candidate.get_support() > counted_votes / 2:
                    return ret

            if i == len(ret) - 2:
                for candidate in ret:
                    candidate.set_support(0)
                for vote in vote_array:
                    ret[vote.get_hated_candidate()].add_support(-1)
            else:
                for candidate in ret:
                    candidate.set_support(0)
                    if candidate.get_validity():
                        for vote in vote_array:
                            appearance = False
                            for j in range(i + 1):
                                if vote.get_ballot_at(j) == candidate.get_index():
                                    appearance = True
                                    break
                            if not appearance:
                                candidate.add_support(-1)

            min([x for x in ret if x.get_validity()]).set_validity(False)

        Utils.plurality_count(vote_array, ret)

        return ret

    @staticmethod
    def run_geller_irv_election(vote_array):
        ret = deepcopy(main.candidate_list)

        for i in range(len(ret) - 2):
            Utils.plurality_count(vote_array, ret)
            counted_votes = sum([x.get_support() for x in ret])
            if any([x.get_support() > counted_votes / 2 for x in ret]):
                return ret

            Utils.borda_count(vote_array, ret)
            min([x for x in ret if x.get_validity()]).set_validity(False)

        Utils.plurality_count(vote_array, ret)

        return ret

    @staticmethod
    def run_instant_runoff_election(vote_array):
        ret = deepcopy(main.candidate_list)

        for i in range(len(ret) - 2):
            Utils.plurality_count(vote_array, ret)
            counted_votes = 0
            for candidate in ret:
                counted_votes += candidate.get_support()

            for candidate in ret:
                if candidate.get_support() > counted_votes / 2:
                    return ret

            min([x for x in ret if x.get_validity()]).set_validity(False)

        Utils.plurality_count(vote_array, ret)

        return ret

    @staticmethod
    def run_nanson_election(vote_array):
        ret = deepcopy(main.candidate_list)

        while True:
            valid_candidates = len([candidate for candidate in ret if candidate.get_validity()])
            Utils.borda_count(vote_array, ret)
            if valid_candidates <= 2:
                return ret

            counted_votes = sum([candidate.get_support() for candidate in ret])

            for candidate in ret:
                if candidate.get_support() < counted_votes / valid_candidates:
                    candidate.set_validity(False)

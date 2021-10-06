import itertools
import random
import Generator
import Utils
import main


class ScoreBasedElectionMethods:

    @staticmethod
    def run_copeland_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
        for candidate in ret:
            for opponent in ret[(candidate.get_index() + 1):]:
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

    @staticmethod
    def run_min_max_winning_election(vote_array):

        ret = Generator.generate_candidate_list(main.candidate_names)
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

        ret = Generator.generate_candidate_list(main.candidate_names)
        for index, candidate in enumerate(ret):
            for opponent in ret[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                if temp_array[0] > temp_array[1]:
                    if -temp_array[0] < opponent.get_support():
                        opponent.set_support(-temp_array[0] + temp_array[1])
                if temp_array[1] > temp_array[0]:
                    if -temp_array[1] < candidate.get_support():
                        candidate.set_support(-temp_array[1] + temp_array[0])

        Utils.election_results_curve(ret)

        return ret

    @staticmethod
    def run_min_max_pairwise_opposition_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
        for index, candidate in enumerate(ret):
            for opponent in ret[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                if -temp_array[0] < opponent.get_support():
                    opponent.set_support(-temp_array[0])
                if -temp_array[1] < candidate.get_support():
                    candidate.set_support(-temp_array[1])

        Utils.election_results_curve(ret)

        return ret

    @staticmethod
    def run_anti_plurality_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
        for vote in vote_array:
            if vote.get_hated_candidate() != -1:
                ret[vote.get_hated_candidate()].add_support(-1)

        Utils.election_results_curve(ret)

        return ret

    @staticmethod
    def run_approval_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
        for vote in vote_array:
            for support in vote.get_ballot():
                ret[support].add_support(1)

        return ret

    @staticmethod
    def run_borda_election(vote_array):
        return Utils.borda_count(vote_array, Generator.generate_candidate_list(main.candidate_names))

    @staticmethod
    def run_nauru_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
        for vote in vote_array:
            for placement, support in enumerate(vote.get_ballot()):
                ret[support].add_support(1 / (placement + 1))

        return ret

    @staticmethod
    def run_fptp_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
        for vote in vote_array:
            ret[vote.get_ballot_at(0)].add_support(1)
        return ret

    @staticmethod
    def run_majority_judgement_election(vote_array):
        judgement_matrix = []
        for i in range(main.candidate_num):
            judgement_matrix.append([])
        for vote in vote_array:
            for support, candidate in enumerate(vote.get_ballot()):
                judgement_matrix[candidate].append(main.candidate_num - support)

        for place, i in enumerate(judgement_matrix):
            judgement_matrix[place] = sorted(i, reverse=True)

        while True:
            median_matrix = []
            for candidate in judgement_matrix:
                median_matrix.append(candidate[int(len(candidate) / 2)])
            max_median_score = max(median_matrix)

            if median_matrix.count(max_median_score) == 1:
                ret = Generator.generate_candidate_list(main.candidate_names)
                for index, candidate in enumerate(ret):
                    candidate.set_support(median_matrix[index])
                return ret

            for candidate in judgement_matrix:
                try:
                    candidate.remove(max_median_score)
                except ValueError:
                    pass


class AlternativeElectionMethods:

    @staticmethod
    def run_alternative_copeland_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
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
        ret = Generator.generate_candidate_list(main.candidate_names)
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
        candidate_list = Generator.generate_candidate_list(main.candidate_names)
        ret = []
        for v in range(len(candidate_list)):
            while True:
                for candidate in candidate_list:
                    candidate.set_support(0)

                current_smith_set = Utils.smith_set_in_adjacency_matrix(Utils.generate_adjacency_matrix(vote_array, candidate_list))
                if len(current_smith_set) == 1:
                    ret += current_smith_set
                    break

                for candidate in candidate_list:
                    candidate.set_validity(False)
                for i in current_smith_set:
                    candidate_list[i].set_validity(True)

                Utils.fptp_pseudo_vote(vote_array, candidate_list)
                Utils.last_place_invalidation(candidate_list)

            for candidate in candidate_list:
                candidate.set_validity(True)
            for i in ret:
                candidate_list[i].set_validity(False)

        return ret

    @staticmethod
    def run_bucklin_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)
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
        ret = Generator.generate_candidate_list(main.candidate_names)
        temp_array = vote_array
        Utils.fptp_pseudo_vote(temp_array, ret)
        return ret

    @staticmethod
    def run_random_ballot_election(vote_array):
        return (random.choice(vote_array)).get_ballot()


class PermutationElectionMethods:

    @staticmethod
    def run_kemeny_young_election(vote_array):
        candidate_list = Generator.generate_candidate_list(main.candidate_names)
        return_options = []
        for candidate in candidate_list:
            for opponent in candidate_list[(candidate.get_index() + 1):]:
                return_options.append([candidate.get_index(), opponent.get_index(), 0, 0, 0])

        round_amount = 0
        for candidate in candidate_list:
            for opponent in candidate_list[(candidate.get_index() + 1):]:
                for vote in vote_array:
                    for i in range(vote.get_ballot_length()):
                        if vote.get_ballot_at(i) == candidate.get_index():
                            return_options[round_amount][2] += 1
                            break
                        if vote.get_ballot_at(i) == opponent.get_index():
                            return_options[round_amount][4] += 1
                            break
                        if i == vote.get_ballot_length() - 1:
                            return_options[round_amount][3] += 1

                round_amount += 1

        ret = 0
        ret_support = 0
        for permutation in list(itertools.permutations(list(range(len(candidate_list))))):
            results_contender = permutation
            contender_support = 0
            for index, winner in enumerate(permutation):
                for loser in permutation[(index + 1):]:
                    for one_on_one in return_options:
                        if min(winner, loser) == one_on_one[0] and max(winner, loser) == one_on_one[1]:
                            contender_support += one_on_one[4] if winner > loser else one_on_one[2]

            if contender_support > ret_support:
                ret = results_contender
                ret_support = contender_support

        return ret

    @staticmethod
    def run_ranked_pairs_election(vote_array):
        candidate_list = Generator.generate_candidate_list(main.candidate_names)
        ret = []
        for v in range(len(candidate_list)):
            adjacency_matrix = Utils.generate_adjacency_matrix(vote_array, candidate_list)

            for i in range(len(adjacency_matrix)):
                while True:
                    min_cycle_win = Utils.adjacency_cycle_check(i, i, adjacency_matrix, [], 0)
                    if min_cycle_win == -1:
                        break
                    else:
                        adjacency_matrix[min_cycle_win[0]][min_cycle_win[1]] = 0

            for i in range(len(candidate_list)):
                if candidate_list[i].get_validity():
                    if all(adjacency_matrix[j][i] == 0 for j in range(len(candidate_list))):
                        ret.append(i)
                        candidate_list[i].set_validity(False)

        return ret

    @staticmethod
    def run_schulze_election(vote_array):
        candidate_list = Generator.generate_candidate_list(main.candidate_names)
        pairwise_results_matrix = []
        ret = []
        for candidate in candidate_list:
            for opponent in candidate_list[(candidate.get_index() + 1):]:
                pairwise_results_matrix.append([candidate.get_index(), opponent.get_index(), 0, 0, 0])

        round_amount = 0
        for candidate in candidate_list:
            for opponent in candidate_list[(candidate.get_index() + 1):]:
                for vote in vote_array:
                    for i in range(vote.get_ballot_length()):
                        if vote.get_ballot_at(i) == candidate.get_index():
                            pairwise_results_matrix[round_amount][2] += 1
                            break
                        if vote.get_ballot_at(i) == opponent.get_index():
                            pairwise_results_matrix[round_amount][4] += 1
                            break
                        if i == vote.get_ballot_length() - 1:
                            pairwise_results_matrix[round_amount][3] += 1

                round_amount += 1

        distance_strength_matrix = [[0 for _ in range(len(candidate_list))] for _ in range(len(candidate_list))]

        for r in pairwise_results_matrix:
            if r[2] == r[4]:
                continue
            distance_strength_matrix[r[0]][r[1]], distance_strength_matrix[r[1]][r[0]] = (r[2], 0) if r[2] > r[4] else (0, r[4])

        for i in range(len(candidate_list)):
            for j in range(len(candidate_list)):
                if i != j:
                    for k in range(len(candidate_list)):
                        if k != i and k != j:
                            distance_strength_matrix[j][k] = max(distance_strength_matrix[j][k], min(distance_strength_matrix[j][i], distance_strength_matrix[i][k]))

        for candidate in candidate_list:
            for opponent in candidate_list[(candidate.get_index() + 1):]:
                candidate.add_support(1) if distance_strength_matrix[candidate.get_index()][opponent.get_index()] > distance_strength_matrix[opponent.get_index()][candidate.get_index()] else opponent.add_support(1)

        for i in range(main.candidate_num):
            for candidate in candidate_list:
                if candidate.get_support() == (main.candidate_num - (i + 1)):
                    ret.append(candidate.get_index())

        return ret

    @staticmethod
    def run_permutation_sequential_pairwise_election(vote_array):
        candidate_list = Generator.generate_candidate_list(main.candidate_names)
        ret = []
        for i in range(len(candidate_list)):
            for candidate in candidate_list:
                candidate.set_support(0)
            contender = 0
            for j in range(1, len(candidate_list)):
                temp_array = Utils.pairwise_comparison(vote_array, contender, j, candidate_list)
                if temp_array[0] < temp_array[1]:
                    contender = j

            ret.append(contender)
            candidate_list[contender].set_validity(False)

        return ret


class RunoffElectionMethods:

    @staticmethod
    def run_coombs_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)

        for i in range(len(ret) - 2, 0, -1):
            Utils.fptp_pseudo_vote(vote_array, ret)
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

            contender_chosen = False
            contender = 0
            for candidate in ret:
                if candidate.get_validity():
                    if not contender_chosen:
                        contender = candidate
                        contender_chosen = True
                    if candidate.get_support() < contender.get_support():
                        contender = candidate
            ret[contender.get_index()].set_validity(False)

        Utils.fptp_pseudo_vote(vote_array, ret)

        return ret

    @staticmethod
    def run_geller_irv_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)

        for i in range(len(ret) - 2):
            Utils.fptp_pseudo_vote(vote_array, ret)
            counted_votes = 0
            for candidate in ret:
                counted_votes += candidate.get_support()

            for candidate in ret:
                if candidate.get_support() > counted_votes / 2:
                    return ret

            borda_results = Utils.borda_count(vote_array, Generator.generate_candidate_list(main.candidate_names))

            contender_chosen = False
            contender = 0
            for candidate in borda_results:
                if ret[candidate.get_index()].get_validity():
                    if not contender_chosen:
                        contender = candidate
                        contender_chosen = True
                    if candidate.get_support() < contender.get_support():
                        contender = candidate
            ret[contender.get_index()].set_validity(False)

        Utils.fptp_pseudo_vote(vote_array, ret)

        return ret

    @staticmethod
    def run_instant_runoff_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)

        for i in range(len(ret) - 2):
            Utils.fptp_pseudo_vote(vote_array, ret)
            counted_votes = 0
            for candidate in ret:
                counted_votes += candidate.get_support()

            for candidate in ret:
                if candidate.get_support() > counted_votes / 2:
                    return ret

            Utils.last_place_invalidation(ret)

        Utils.fptp_pseudo_vote(vote_array, ret)

        return ret

    @staticmethod
    def run_nanson_election(vote_array):
        ret = Generator.generate_candidate_list(main.candidate_names)

        for i in range(len(ret) - 2):
            valid_candidates = 0
            for candidate in ret:
                candidate.set_support(0)
                if candidate.get_validity():
                    valid_candidates += 1

            Utils.borda_count(vote_array, ret)

            if valid_candidates <= 2:
                return ret

            counted_votes = 0
            for candidate in ret:
                counted_votes += candidate.get_support()

            for candidate in ret:
                if candidate.get_support() < counted_votes / valid_candidates:
                    candidate.set_validity(False)

        return ret

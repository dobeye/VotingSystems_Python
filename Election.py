import Generator
import Utils
import main
from Candidate import Candidate


class Election:
    def __init__(self, election_type, winner):
        self.winner = winner
        if len(winner) == 1:
            self.winner = winner[0]
        self.election_type = election_type

    def get_winner(self):
        return self.winner


class PlacementElection(Election):
    def __init__(self, candidate_list, election_type):
        self.placement_list = sorted(candidate_list, key=lambda x: x.get_placement())
        if election_type is None:
            election_type = type(self).__name__
        super().__init__(election_type, [candidate for candidate in self.placement_list if candidate.get_placement() == 1])

    def run_election(self, vote_array):
        pass

    def run_method_divergent_election(self, vote_array, election_method, method_name):
        pass


class ScoreBased(PlacementElection):
    def __init__(self, vote_array, election_method=None, method_name=None, election_type=None):
        self.candidate_list = Generator.generate_candidate_list()
        self.run_election(vote_array)
        self.run_method_divergent_election(vote_array, election_method, method_name)
        Candidate.placement_by_support(self.candidate_list)
        super().__init__(self.candidate_list, election_type)


# region Score based election classes
class FPTP(ScoreBased):
    def run_election(self, vote_array):
        for vote in vote_array:
            self.candidate_list[vote.get_ballot_at(0)].add_support(1)


class AntiPlurality(ScoreBased):
    def run_election(self, vote_array):
        for vote in vote_array:
            if vote.get_hated_candidate() != -1:
                self.candidate_list[vote.get_hated_candidate()].add_support(-1)

        Utils.election_results_curve(self.candidate_list)


class Copeland(ScoreBased):
    def run_election(self, vote_array):
        for index, candidate in enumerate(self.candidate_list):
            for opponent in self.candidate_list[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                if temp_array[0] > temp_array[1]:
                    candidate.add_support(1)
                    continue
                if temp_array[1] > temp_array[0]:
                    opponent.add_support(1)
                    continue
                candidate.add_support(0.5)
                opponent.add_support(0.5)


class Approval(ScoreBased):
    def run_election(self, vote_array):
        for vote in vote_array:
            for support in vote.get_ballot():
                self.candidate_list[support].add_support(1)


class Borda(ScoreBased):
    def run_election(self, vote_array):
        Utils.borda_count(vote_array, self.candidate_list)


class BordaNauru(ScoreBased):
    def run_election(self, vote_array):
        Utils.borda_count(vote_array, self.candidate_list, lambda x: 1 / (x + 1))


class Bucklin(ScoreBased):
    def run_election(self, vote_array):
        for i in range(main.candidate_num):
            for vote in vote_array:
                if vote.check_validity_at(i):
                    self.candidate_list[vote.get_ballot_at(i)].add_support(1)

            if any([x.get_support() > (len(vote_array) / 2) for x in self.candidate_list]):
                return


class MinMax(ScoreBased):

    min_max_methods = {"Winning": (False, (lambda x: (-x[0], -x[1]))), "Margin": (False, (lambda x: (-x[0] + x[1], -x[1] + x[0]))), "Pairwise Opposition": (True, (lambda x: (-x[0], -x[1])))}

    def run_method_divergent_election(self, vote_array, judgement_method, method_name):
        if judgement_method is None:
            judgement_method = "Winning"
        if method_name is None:
            method_name = judgement_method

        method_tuple = MinMax.min_max_methods[judgement_method]

        for index, candidate in enumerate(self.candidate_list):
            for opponent in self.candidate_list[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.get_index(), opponent.get_index())

                if temp_array[0] > temp_array[1] or method_tuple[0]:
                    opponent.set_support(min(opponent.get_support(), method_tuple[1](temp_array)[0]))
                if temp_array[1] > temp_array[0] or method_tuple[0]:
                    candidate.set_support(min(candidate.get_support(), method_tuple[1](temp_array)[1]))

        Utils.election_results_curve(self.candidate_list)
        self.election_type = type(self).__name__ + method_name


class MajorityJudgement(ScoreBased):

    majority_judgment_methods = {"Typical": (lambda t: t[0] + t[1] - t[2]),
                                 "Usual": (lambda t: t[0] + 0.5 * (t[1] - t[2]) / (1 - t[1] - t[2])),
                                 "Central": (lambda t: t[0] + 0.5 * (t[1] - t[2]) / (t[1] + t[2] + 0.000001))}

    def run_method_divergent_election(self, vote_array, judgement_method, method_name):
        judgement_matrix = Utils.majority_judgement_matrix(vote_array)
        if method_name is None:
            method_name = judgement_method

        if judgement_method is None:
            while True:
                median_matrix = [Utils.find_list_median(candidate) for candidate in judgement_matrix]
                max_median_score = max(median_matrix)

                if median_matrix.count(max_median_score) == 1:
                    for index, candidate in enumerate(self.candidate_list):
                        candidate.set_support(median_matrix[index])
                    break

                for candidate in judgement_matrix:
                    try:
                        candidate.remove(max_median_score)
                    except ValueError:
                        pass
        elif isinstance(judgement_method, str):
            for index, candidate in enumerate(self.candidate_list):
                candidate.set_support(MajorityJudgement.majority_judgment_methods[judgement_method](Utils.mj_median_proponents_opponents(judgement_matrix, index, len(vote_array))))
        else:
            for index, candidate in enumerate(self.candidate_list):
                candidate.set_support(judgement_method(Utils.mj_median_proponents_opponents(judgement_matrix, index, len(vote_array))))

        self.election_type = type(self).__name__ + method_name
# endregion


class RunOff(PlacementElection):
    def __init__(self, vote_array, election_type=None):
        self.candidate_list = Generator.generate_candidate_list()
        self.pseudo_result_list = []
        self.run_runoff_election(vote_array)
        super().__init__(self.candidate_list, election_type)

    def run_runoff_election(self, vote_array):
        for i in range(main.candidate_num):
            self.run_election(vote_array)
            self.pseudo_result_list.append(self.RunOffStep([x for x in self.candidate_list if not x.get_validity()],
                                                           [x for x in self.candidate_list if x.get_validity()],
                                                           min([x for x in self.candidate_list if x.get_validity()]),
                                                           i))

            min([x for x in self.candidate_list if x.get_validity()]).set_validity(False)
            for candidate in self.candidate_list:
                if not candidate.get_validity():
                    candidate.demote_placement(1)

    class RunOffStep:
        def __init__(self, invalidated_list, candidate_list, removed_candidate, round_number):
            self.invalidated_list = invalidated_list
            self.candidate_array = candidate_list
            self.removed_candidate = removed_candidate
            self.round_number = round_number


# region Runoff election classes
class InstantRunOff(RunOff):
    def run_election(self, vote_array):
        Utils.plurality_count(vote_array, self.candidate_list)


class CoombsRule(RunOff):
    def run_election(self, vote_array):
        for candidate in self.candidate_list:
            candidate.set_support(0)
            for vote in vote_array:
                if all([candidate.get_index() != x for x in vote.get_ballot()[:(main.candidate_num - 1)]]):
                    candidate.add_support(-1)


class BaldwinMethod(RunOff):
    def run_election(self, vote_array):
        Utils.borda_count(vote_array, self.candidate_list)


class NansonMethod(RunOff):
    def run_runoff_election(self, vote_array):
        round_number = 0

        while any([x.get_validity() for x in self.candidate_list]):
            Utils.borda_count(vote_array, self.candidate_list)
            counted_votes = sum([candidate.get_support() for candidate in self.candidate_list])
            self.pseudo_result_list.append(self.RunOffStep([x for x in self.candidate_list if not x.get_validity()], [x for x in self.candidate_list if x.get_validity()], [x for x in self.candidate_list if x.get_support() <= counted_votes], round_number))

            for candidate in [x for x in self.candidate_list if x.get_support() <= (counted_votes / len([0 for x in self.candidate_list if x.get_validity()]))]:
                candidate.set_validity(False)
            for candidate in self.candidate_list:
                if not candidate.get_validity():
                    candidate.demote_placement(1)
            round_number += 1
# endregion


class Condorcet(PlacementElection):
    def __init__(self, vote_array, election_type=None):
        self.pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array)
        self.candidate_list = Generator.generate_candidate_list()
        self.run_election(vote_array)
        super().__init__(self.candidate_list, election_type)


# region Condorcet election classes
class KemenyYoung(Condorcet):
    def run_election(self, vote_array):
        pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array)

        election_permutation = 0
        ret_support = 0
        import itertools
        for permutation in list(itertools.permutations(list(range(main.candidate_num)))):
            results_contender = permutation
            contender_support = 0
            for index, winner in enumerate(permutation):
                for loser in permutation[(index + 1):]:
                    contender_support += pairwise_support_matrix[winner][loser]

            if contender_support > ret_support:
                election_permutation = results_contender
                ret_support = contender_support

        for index, candidate in enumerate(election_permutation):
            self.candidate_list[candidate].set_placement(index + 1)


class RankedPairs(Condorcet):
    def run_election(self, vote_array):
        for v in range(main.candidate_num):
            pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array, self.candidate_list)

            for i in range(main.candidate_num):
                while True:
                    min_cycle_win = Utils.pairwise_support_cycle_check(i, i, pairwise_support_matrix, [], 0)
                    if min_cycle_win == -1:
                        break
                    else:
                        pairwise_support_matrix[min_cycle_win[0]][min_cycle_win[1]] = pairwise_support_matrix[min_cycle_win[1]][min_cycle_win[0]] = 0

            for i in range(main.candidate_num):
                if self.candidate_list[i].get_validity():
                    if all(pairwise_support_matrix[j][i] <= pairwise_support_matrix[i][j] for j in range(main.candidate_num)):
                        self.candidate_list[i].set_placement(v + 1)
                        self.candidate_list[i].set_validity(False)


class Schulze(Condorcet):
    def run_election(self, vote_array):
        candidate_list = list(range(main.candidate_num))
        for candidate in self.candidate_list:
            candidate.set_placement(main.candidate_num)

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
                    self.candidate_list[x].demote_placement(-1)
                else:
                    self.candidate_list[y].demote_placement(-1)


class SequentialPairwise(Condorcet):
    def run_election(self, vote_array):
        for i in range(main.candidate_num):
            contender = 0
            for j in range(1, main.candidate_num):
                temp_array = Utils.pairwise_comparison(vote_array, contender, j, self.candidate_list)
                if temp_array[0] < temp_array[1]:
                    contender = j

            self.candidate_list[contender].set_placement(i + 1)
            self.candidate_list[contender].set_validity(False)


class AlternativeTideman(Condorcet):
    def run_election(self, vote_array):
        for v in range(main.candidate_num):
            while True:
                for candidate in self.candidate_list:
                    candidate.set_support(0)

                current_smith_set = Utils.smith_set_in_adjacency_matrix(Utils.generate_adjacency_matrix(vote_array, self.candidate_list))
                if len(current_smith_set) == 1:
                    self.candidate_list[current_smith_set[0]].set_placement(v + 1)
                    break

                for candidate in self.candidate_list:
                    candidate.set_validity(False)
                for i in current_smith_set:
                    self.candidate_list[i].set_validity(True)

                Utils.plurality_count(vote_array, self.candidate_list)
                min([x for x in self.candidate_list if x.get_validity()]).set_validity(False)

            for candidate in self.candidate_list:
                if candidate.get_placement() == 0:
                    candidate.set_validity(True)
                else:
                    candidate.set_validity(False)
# endregion

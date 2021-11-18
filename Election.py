from copy import deepcopy
import Generator
import Utils
from Items import Candidate


class Election:

    functional_election = False
    multi_type = False

    def __init__(self, winner):
        self.winner = winner
        if len(winner) == 1:
            self.winner = winner[0]

    def get_winner(self):
        return self.winner

    @classmethod
    def is_election(cls):
        return cls.functional_election


class PlacementElection(Election):
    def __init__(self, vote_array, election_type=None, candidate_list=None):
        self.candidate_list = deepcopy(candidate_list)
        if candidate_list is None:
            self.candidate_list = Generator.generate_candidate_list()
        self.election_type = election_type

        self.run_entire_election(vote_array)
        self.placement_list = sorted(self.candidate_list, key=lambda x: x.place)

        if self.election_type is None:
            self.election_type = type(self).__name__

        super().__init__([candidate for candidate in self.placement_list if candidate.place == 1])

    # region dummy methods
    def run_election(self, vote_array):
        pass

    def run_entire_election(self, vote_array):
        self.run_election(vote_array)
    # endregion

    def print_election(self):
        print(f"\n{self.election_type}\n")
        for candidate in self.placement_list:
            print(f"{candidate.place}: {candidate.name}")


class ScoreBased(PlacementElection):
    def run_election(self, vote_array):
        Candidate.placement_by_support(self.candidate_list)

    def print_election(self):
        print(f"\n{self.election_type}\n")
        for candidate in self.placement_list:
            print(f"{candidate.place}: {candidate.name} - {candidate.supporters}")


class RunOff(PlacementElection):
    def __init__(self, vote_array, election_type=None, candidate_list=None):
        self.pseudo_result_list = []
        super().__init__(vote_array, election_type, candidate_list)

    def run_entire_election(self, vote_array):
        for i in range(Candidate.candidate_num):
            self.run_election(vote_array)
            self.add_runoff_step(i)

            min([x for x in self.candidate_list if x.exists]).set_validity(False)
            for candidate in self.candidate_list:
                if not candidate.exists:
                    candidate.demote_placement(1)

    def add_runoff_step(self, i):
        self.pseudo_result_list.append(
            self.RunOffStep([deepcopy(x) for x in self.candidate_list if not x.exists],
                            [deepcopy(x) for x in self.candidate_list if x.exists],
                            min([deepcopy(x) for x in self.candidate_list if x.exists]),
                            i))

    def print_runoff_steps(self):
        for runoff in self.pseudo_result_list:
            runoff.print_valid_candidates()
            print("")

    class RunOffStep:
        def __init__(self, invalidated_list, candidate_list, removed_candidate, round_number):
            self.invalidated_list = invalidated_list
            self.candidate_list = candidate_list
            self.removed_candidate = removed_candidate
            self.round_number = round_number

        def print_valid_candidates(self):
            for first, candidate in enumerate(sorted(self.candidate_list, key=lambda x: x.supporters, reverse=True)):
                if first > 0:
                    print(", ", end="")
                print(f"{candidate.name}: {candidate.supporters}", end="")


class Condorcet(PlacementElection):
    pass


# region Score based election classes
class FPTP(ScoreBased):

    functional_election = True

    def run_election(self, vote_array):
        Utils.plurality_count(vote_array, self.candidate_list)
        super().run_election(vote_array)


class AntiPlurality(ScoreBased):

    functional_election = True

    def run_election(self, vote_array):
        for vote in vote_array:
            if vote.hated is not None:
                self.candidate_list[vote.hated].add_support(-1)

        Utils.election_results_curve(self.candidate_list)
        super().run_election(vote_array)


class Copeland(ScoreBased, Condorcet):

    functional_election = True

    def run_election(self, vote_array):
        for index, candidate in enumerate(self.candidate_list):
            for opponent in self.candidate_list[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.number, opponent.number)

                if temp_array[0] > temp_array[1]:
                    candidate.add_support(1)
                    continue
                if temp_array[1] > temp_array[0]:
                    opponent.add_support(1)
                    continue
                candidate.add_support(0.5)
                opponent.add_support(0.5)
        super().run_election(vote_array)


class Approval(ScoreBased):

    functional_election = True

    def run_election(self, vote_array):
        for vote in vote_array:
            for support in vote.ballot:
                self.candidate_list[support].add_support(1)
        super().run_election(vote_array)


class Borda(ScoreBased):

    functional_election = True

    def run_election(self, vote_array):
        Utils.borda_count(vote_array, self.candidate_list)
        super().run_election(vote_array)


class BordaNauru(ScoreBased):

    functional_election = True

    def run_election(self, vote_array):
        Utils.borda_count(vote_array, self.candidate_list, lambda x: 1 / (x + 1))
        super().run_election(vote_array)


class MinMax(ScoreBased):

    functional_election = True
    multi_type = True

    election_methods = {"Winning": (False, (lambda x: (-x[0], -x[1]))),
                        "Margin": (False, (lambda x: (-x[0] + x[1], -x[1] + x[0]))),
                        "PairwiseOpposition": (True, (lambda x: (-x[0], -x[1])))}

    def run_election(self, vote_array):
        if self.election_type is None:
            self.election_type = "Winning"

        method_tuple = MinMax.election_methods[self.election_type]

        for index, candidate in enumerate(self.candidate_list):
            for opponent in self.candidate_list[(index + 1):]:
                temp_array = Utils.pairwise_comparison(vote_array, candidate.number, opponent.number)

                if temp_array[0] > temp_array[1] or method_tuple[0]:
                    opponent.set_support(min(opponent.supporters, method_tuple[1](temp_array)[0]))
                if temp_array[1] > temp_array[0] or method_tuple[0]:
                    candidate.set_support(min(candidate.supporters, method_tuple[1](temp_array)[1]))

        Utils.election_results_curve(self.candidate_list)
        self.election_type = type(self).__name__ + self.election_type
        super().run_election(vote_array)


class MajorityJudgement(ScoreBased):

    functional_election = True
    multi_type = True

    election_methods = {"Standard": None,
                        "Typical": (lambda t: t[0] + t[1] - t[2]),
                        "Usual": (lambda t: t[0] + 0.5 * (t[1] - t[2]) / (1 - t[1] - t[2])),
                        "Central": (lambda t: t[0] + 0.5 * (t[1] - t[2]) / (t[1] + t[2] + 0.000001))}

    def run_election(self, vote_array):
        judgement_matrix = Utils.majority_judgement_matrix(vote_array)
        if self.election_type is None:
            self.election_type = "Standard"

        if MajorityJudgement.election_methods[self.election_type] is None:
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
        else:
            for index, candidate in enumerate(self.candidate_list):
                candidate.set_support(MajorityJudgement.election_methods[self.election_type](Utils.mj_median_proponents_opponents(judgement_matrix, index, len(vote_array))))

        if self.election_type is not None:
            self.election_type = type(self).__name__ + str(self.election_type)
        super().run_election(vote_array)
# endregion


# region Runoff election classes
class InstantRunOff(RunOff):

    functional_election = True

    def run_election(self, vote_array):
        Utils.plurality_count(vote_array, self.candidate_list)


class CoombsRule(RunOff):

    functional_election = True

    def run_election(self, vote_array):
        for candidate in self.candidate_list:
            candidate.set_support(0)
            for vote in vote_array:
                if all([candidate.number != x for x in vote.ballot[:(Candidate.candidate_num - 1)]]):
                    candidate.add_support(-1)


class BaldwinMethod(RunOff):

    functional_election = True

    def run_election(self, vote_array):
        Utils.borda_count(vote_array, self.candidate_list)


class NansonMethod(RunOff):

    functional_election = True

    def run_entire_election(self, vote_array):
        round_number = 0

        while any([x.exists for x in self.candidate_list]):
            Utils.borda_count(vote_array, self.candidate_list)
            counted_votes = sum([candidate.supporters for candidate in self.candidate_list])
            valid_amount = 0
            for candidate in self.candidate_list:
                if candidate.exists:
                    valid_amount += 1
            self.pseudo_result_list.append(self.RunOffStep([deepcopy(x) for x in self.candidate_list if not x.exists],
                                                           [deepcopy(x) for x in self.candidate_list if x.exists],
                                                           [deepcopy(x) for x in self.candidate_list if x.supporters <= counted_votes / valid_amount],
                                                           round_number))

            for candidate in [x for x in self.candidate_list if x.supporters <= counted_votes / valid_amount]:
                candidate.set_validity(False)
            for candidate in self.candidate_list:
                if not candidate.exists:
                    candidate.demote_placement(1)
            round_number += 1


class Bucklin(RunOff, ScoreBased):

    functional_election = True

    def run_entire_election(self, vote_array):
        for i in range(Candidate.candidate_num):
            for vote in vote_array:
                if vote.check_validity_at(i):
                    self.candidate_list[vote.get_ballot_at(i)].add_support(1)

            self.pseudo_result_list.append(self.RunOffStep(None,
                                                           [deepcopy(x) for x in self.candidate_list if x.exists],
                                                           None,
                                                           i))

            if any([x.supporters > (len(vote_array) / 2) for x in self.candidate_list]):
                super().run_election(vote_array)
                return
        super().run_election(vote_array)


class AlternativeTideman(RunOff, Condorcet):

    functional_election = True

    def run_entire_election(self, vote_array):
        for v in range(Candidate.candidate_num):
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
                self.add_runoff_step(v)

                min([x for x in self.candidate_list if x.exists]).set_validity(False)

            for candidate in self.candidate_list:
                if candidate.place == 0:
                    candidate.set_validity(True)
                else:
                    candidate.set_validity(False)
# endregion


# region Condorcet election classes
class KemenyYoung(Condorcet):

    functional_election = True

    def run_election(self, vote_array):
        pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array)

        election_permutation = []
        ret_support = 0
        import itertools
        for permutation in list(itertools.permutations(list(range(Candidate.candidate_num)))):
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


class SplitCycle(Condorcet):

    functional_election = True

    def run_election(self, vote_array):
        for v in range(Candidate.candidate_num):
            pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array, self.candidate_list)

            split_cycles = set()
            for i in range(Candidate.candidate_num):
                for j in range(Candidate.candidate_num):
                    if pairwise_support_matrix[i][j] > pairwise_support_matrix[j][i]:
                        cycle_path = Utils.pairwise_support_cycle_check(i, j, pairwise_support_matrix, [])
                        if cycle_path == -1:
                            continue
                        min_cycle_win = min(cycle_path, key=lambda x: x[2])
                        for step in cycle_path:
                            if step[2] == min_cycle_win[2]:
                                split_cycles.add(step)

            for step in split_cycles:
                pairwise_support_matrix[step[0]][step[1]] = pairwise_support_matrix[step[1]][step[0]] = 0

            for i in range(Candidate.candidate_num):
                if self.candidate_list[i].exists:
                    if all(pairwise_support_matrix[j][i] <= pairwise_support_matrix[i][j] for j in range(Candidate.candidate_num)):
                        self.candidate_list[i].set_placement(v + 1)
                        self.candidate_list[i].set_validity(False)


class RankedPairs(Condorcet):

    functional_election = True

    def run_election(self, vote_array):
        for i in range(Candidate.candidate_num):
            adjacency_matrix = Utils.generate_adjacency_matrix(vote_array, self.candidate_list)
            return_key = [[0 for _ in range(Candidate.candidate_num)] for _ in range(Candidate.candidate_num)]
            while True:
                largest_win = (0, 0, 0)
                for j in range(Candidate.candidate_num):
                    for k in range(Candidate.candidate_num):
                        if adjacency_matrix[j][k] > largest_win[2]:
                            largest_win = (j, k, adjacency_matrix[j][k])

                adjacency_matrix[largest_win[0]][largest_win[1]] = 0
                return_key[largest_win[0]][largest_win[1]] = largest_win[2]

                if largest_win[2] == 0:
                    break

                if Utils.pairwise_support_cycle_check(largest_win[0], largest_win[1], return_key) != -1:
                    return_key[largest_win[0]][largest_win[1]] = 0

            for j in range(Candidate.candidate_num):
                if self.candidate_list[j].exists:
                    if all(return_key[k][j] <= return_key[j][k] for k in range(Candidate.candidate_num)):
                        self.candidate_list[j].set_placement(i + 1)
                        self.candidate_list[j].set_validity(False)


class Schulze(Condorcet):

    functional_election = True

    def run_election(self, vote_array):
        candidate_list = list(range(Candidate.candidate_num))
        for candidate in self.candidate_list:
            candidate.set_placement(Candidate.candidate_num)

        distance_strength_matrix = Utils.generate_adjacency_matrix(vote_array)

        for i in range(Candidate.candidate_num):
            for j in range(Candidate.candidate_num):
                if i != j:
                    for k in range(Candidate.candidate_num):
                        if k != i and k != j:
                            distance_strength_matrix[j][k] = max(distance_strength_matrix[j][k], min(distance_strength_matrix[j][i], distance_strength_matrix[i][k]))

        for x in candidate_list:
            for y in candidate_list[(x + 1):]:
                if distance_strength_matrix[x][y] > distance_strength_matrix[y][x]:
                    self.candidate_list[x].demote_placement(-1)
                else:
                    self.candidate_list[y].demote_placement(-1)


class SequentialPairwise(Condorcet):

    functional_election = True

    def run_election(self, vote_array):
        for i in range(Candidate.candidate_num):
            contender = 0
            for j in range(1, Candidate.candidate_num):
                temp_array = Utils.pairwise_comparison(vote_array, contender, j, self.candidate_list)
                if temp_array[0] < temp_array[1]:
                    contender = j

            self.candidate_list[contender].set_placement(i + 1)
            self.candidate_list[contender].set_validity(False)
# endregion


class AllTypeElection:

    """The AllTypeElection represents all other elections simulated from the same base vote array, and all vote based
    traits (E.G. adjacency matrix, the smith set, the condorcet winner). Also includes general vote information such as
    voter and candidate amount."""

    def __init__(self, vote_array, candidate_list):
        self.voter_amount = len(vote_array)
        self.candidate_amount = len(candidate_list)

        self.adjacency_matrix = Utils.generate_adjacency_matrix(vote_array, binary=True)
        self.pairwise_support_matrix = Utils.generate_pairwise_support_matrix(vote_array)

        self.smith_set = Utils.smith_set_in_adjacency_matrix(self.adjacency_matrix)
        if len(self.smith_set) == 1:
            self.condorcet_winner = self.smith_set[0]
        else:
            self.condorcet_winner = None

        self.support_by_candidate = [[0 for _ in range(self.candidate_amount)] for _ in range(self.candidate_amount)]
        for vote in vote_array:
            for index, support in enumerate(vote.ballot):
                self.support_by_candidate[support][index] += 1

        # election generation
        self.election_dict = {}
        for election_type in Utils.get_all_subclasses(Election):
            if election_type.is_election():
                if election_type.__name__ not in self.election_dict:
                    if election_type.multi_type:
                        for election_method in election_type.election_methods:
                            self.election_dict[election_type.__name__ + election_method] = election_type(vote_array, election_method, candidate_list)
                    else:
                        self.election_dict[election_type.__name__] = election_type(vote_array, candidate_list=candidate_list)

        # condorcet cycle generation
        self.condorcet_cycle = []
        for i in range(len(candidate_list)):
            while True:
                cycle = Utils.pairwise_support_cycle_check(i, i, self.pairwise_support_matrix)
                if cycle != -1 and cycle not in self.condorcet_cycle:
                    self.condorcet_cycle.append(Utils.pairwise_support_cycle_check(i, i, self.pairwise_support_matrix))
                    continue
                break
        for i in self.condorcet_cycle:
            for j in self.condorcet_cycle:
                if i != j and sorted(i, key=lambda x: x[2]) == sorted(j, key=lambda x: x[2]):
                    self.condorcet_cycle.remove(j)

        self.smith_cycle = [cycle for cycle in self.condorcet_cycle if any([win[0] in self.smith_set for win in cycle])]

    def get_election(self, election):
        return self.election_dict[election]

    def get_all_election_names(self):
        return list(self.election_dict.keys())

    def print_winner_by_election(self):
        for i, k in self.election_dict.items():
            print(f"\n{i}:\n")
            if type(k.get_winner()) == list:
                for j in k.get_winner():
                    print(j.name)
            else:
                print(self.election_dict[i].get_winner().name)

    def print_wins_per_candidate(self):
        wins = [0 for _ in range(self.candidate_amount)]
        for i in self.election_dict.values():
            if type(i.get_winner()) == list:
                for j in i.get_winner():
                    wins[j.number] += 1
            else:
                wins[i.get_winner().number] += 1

        for index, candidate in enumerate(Candidate.candidate_names):
            print(f"{candidate} {wins[index]}")

    def print_all_elections(self):
        for election in self.election_dict.values():
            election.print_election()
        print("")

    def print_pairwise_comparison(self, candidate, opponent):
        print(f"{Candidate.candidate_names[candidate]}: {self.pairwise_support_matrix[candidate][opponent]}")
        print(f"{Candidate.candidate_names[opponent]}: {self.pairwise_support_matrix[opponent][candidate]}")
        print(f"Abstain: {self.voter_amount - self.pairwise_support_matrix[candidate][opponent] - self.pairwise_support_matrix[opponent][candidate]}")

    def print_all_condorcet_cycles(self, smith=False):
        cycle_type = self.condorcet_cycle
        if smith:
            cycle_type = self.smith_cycle

        for path in cycle_type:
            print(str(len(path)) + "-cycle: ")
            for win in path:
                print(f"{Candidate.candidate_names[win[0]]} beats {Candidate.candidate_names[win[1]]} by {win[2]}")
            print("")

    def get_condorcet_winner(self):
        return self.condorcet_winner

    def print_support_per_candidate(self):
        for index, candidate in Candidate.candidate_names:
            print(f"{candidate} {self.support_by_candidate[index]}")

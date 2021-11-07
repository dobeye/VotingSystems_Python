import main
from Candidate import Candidate


class PrintUtilities:

    @staticmethod
    def print_tdl(tdl):
        for i in tdl:
            print(i)

    @staticmethod
    def print_pairwise_matrix(pm):
        for j, i in enumerate(pm):
            print(Candidate.candidate_names[j], i, sum(i))

    @staticmethod
    def name_vote_array(vote_array):
        vote_array_with_names = []
        for rep, vote in enumerate(vote_array):
            vote_array_with_names.append([])
            for i in vote.get_ballot():
                vote_array_with_names[rep].append(Candidate.candidate_names[i])
        for vote in vote_array_with_names:
            print(vote, "\n")

    @staticmethod
    def print_vote_based_election(candidate_list):
        candidate_list = sorted(candidate_list, reverse=True)
        for candidate in candidate_list:
            print(candidate.get_name(), ": ", int(candidate.get_support()))

    @staticmethod
    def print_percentage_election(candidate_list, exactness=2):
        candidate_list = sorted(candidate_list, reverse=True)
        for candidate in candidate_list:
            if candidate.get_support() == int(candidate.get_support()):
                print(candidate.get_name(), ": ", int(candidate.get_support()))
                continue
            print(candidate.get_name(), ": ", int(candidate.get_support() * (10 ** exactness)) / (10 ** exactness))

    @staticmethod
    def print_permutation_election(election_results):
        for placement, i in enumerate(election_results):
            print("#" + str(placement + 1) + ": " + str(Candidate.candidate_names[i]))

    @staticmethod
    def print_winner_only_election(winner):
        print("winner: " + winner)


def plurality_count(vote_array, candidate_list):
    for candidate in candidate_list:
        candidate.set_support(0)
    for vote in vote_array:
        for i in range(vote.get_ballot_length()):
            if candidate_list[vote.get_ballot_at(i)].get_validity():
                candidate_list[vote.get_ballot_at(i)].add_support(1)
                break


def borda_count(vote_array, candidate_list, borda_method=None):
    for candidate in candidate_list:
        candidate.set_support(0)
    for vote in vote_array:
        placement = 0
        for support in vote.get_ballot():
            if candidate_list[support].get_validity():
                if borda_method is None:
                    candidate_list[support].add_support(len(Candidate.candidate_names) - placement)
                else:
                    candidate_list[support].add_support(borda_method(placement))
                placement += 1
    return candidate_list


def pairwise_comparison(vote_array, candidate, opponent, validity_chart=None):
    def vote_support_validity(contender):
        return vote.get_ballot_at(i) == contender and ((validity_chart is None) or (isinstance(validity_chart[0], Candidate) and validity_chart[contender].get_validity()) or (isinstance(validity_chart[0], bool) and validity_chart[contender]))
    ret = [0, 0]
    for vote in vote_array:
        x = None
        for i in range(vote.get_ballot_length()):
            if vote_support_validity(candidate):
                x = 0
            elif vote_support_validity(opponent):
                x = 1
            try:
                ret[x] += 1
                break
            except TypeError:
                pass

    return ret


def generate_adjacency_matrix(vote_array, candidate_list=None, binary=False):
    adjacency_matrix = [[0 for _ in range(Candidate.candidate_num)] for _ in range(Candidate.candidate_num)]
    for i in range(Candidate.candidate_num):
        for j in range(i + 1, Candidate.candidate_num):
            temp_array = pairwise_comparison(vote_array, i, j, candidate_list)

            if temp_array[0] > temp_array[1]:
                if binary:
                    adjacency_matrix[i][j] = 1
                else:
                    adjacency_matrix[i][j] = temp_array[0]
            elif temp_array[1] > temp_array[0]:
                if binary:
                    adjacency_matrix[j][i] = 1
                else:
                    adjacency_matrix[j][i] = temp_array[1]

    return adjacency_matrix


def generate_pairwise_support_matrix(vote_array, candidate_list=None):
    adjacency_matrix = [[0 for _ in range(Candidate.candidate_num)] for _ in range(Candidate.candidate_num)]
    for i in range(Candidate.candidate_num):
        for j in range(i + 1, Candidate.candidate_num):
            temp_array = pairwise_comparison(vote_array, i, j, candidate_list)
            adjacency_matrix[i][j] = temp_array[0]
            adjacency_matrix[j][i] = temp_array[1]

    return adjacency_matrix


def pairwise_support_cycle_check(unbeatable, candidate, pairwise_support_matrix, path=None):
    if path is None:
        path = []
    if pairwise_support_matrix[candidate][unbeatable] > pairwise_support_matrix[unbeatable][candidate]:
        return path + [[candidate, unbeatable, pairwise_support_matrix[candidate][unbeatable] - pairwise_support_matrix[unbeatable][candidate]]]
    if all([pairwise_support_matrix[candidate][x] <= pairwise_support_matrix[x][candidate] for x in range(Candidate.candidate_num)]):
        return -1

    for opponent in range(Candidate.candidate_num):
        if any([n[0] == candidate and n[1] == opponent for n in path]):
            return -1
        if pairwise_support_matrix[candidate][opponent] > pairwise_support_matrix[opponent][candidate]:
            recursion_variable = pairwise_support_cycle_check(unbeatable, opponent, pairwise_support_matrix, path + [[candidate, opponent, pairwise_support_matrix[candidate][opponent] - pairwise_support_matrix[opponent][candidate]]])
            if recursion_variable != -1:
                return recursion_variable
    return -1


def smith_set_in_adjacency_matrix(adjacency_matrix):
    copeland_score_list = []
    for i in adjacency_matrix:
        score = 0
        for j in i:
            if j != 0:
                score += 1
        copeland_score_list.append(score)

    ret = []
    for i, support in enumerate(copeland_score_list):
        if support == max(copeland_score_list):
            ret.append(i)

    while True:
        added_ret = []
        for candidate in ret:
            for index, support in enumerate(adjacency_matrix[candidate]):
                if support == 0 and ret.count(index) == 0:
                    added_ret.append(index)

        if not added_ret:
            break

        ret += added_ret

    return ret


def majority_judgement_matrix(vote_array):
    judgement_matrix = [[] for _ in Candidate.candidate_names]
    for vote in vote_array:
        supported_candidates = set()
        for placement, candidate in enumerate(vote.get_ballot()):
            judgement_matrix[candidate].append(Candidate.candidate_num - placement)
            supported_candidates.add(candidate)
        for candidate in set(range(Candidate.candidate_num)) - supported_candidates:
            judgement_matrix[candidate] += [0]

    return judgement_matrix


def mj_median_proponents_opponents(judgement_matrix, index, voter_num):
    candidate_array = judgement_matrix[index]
    list_median = find_list_median(candidate_array)
    p = q = 0
    for i in candidate_array:
        if i > list_median:
            p += 1
        elif i < list_median:
            q += 1
    p /= voter_num
    q /= voter_num
    return list_median, p, q


def election_results_curve(candidate_list):
    curve = min([x.get_support() for x in candidate_list])
    for candidate in candidate_list:
        candidate.add_support(-curve)


def find_list_median(integer_list):
    if len(integer_list) != 0:
        return sorted(integer_list, reverse=True)[int(len(integer_list) / 2)]
    return 0


def get_all_subclasses(class_input):
    all_subclasses = []

    for subclass in class_input.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses += get_all_subclasses(subclass)

    return all_subclasses


def input_validation(accepted_inputs, input_type, input_prompt):
    while True:
        ret = input(input_prompt)
        if input_type is str:
            if ret not in accepted_inputs:
                print("not a valid input\n")
                continue
            return ret

        elif input_type is int:
            try:
                if int(ret) < accepted_inputs[0] or int(ret) > accepted_inputs[1]:
                    print("not a valid input\n")
                    continue
                else:
                    return int(ret)
            except ValueError:
                print("not a valid input\n")
                continue

        elif input_type is float:
            try:
                if float(ret) < accepted_inputs[0] or float(ret) > accepted_inputs[1]:
                    print("not a valid input\n")
                    continue
                else:
                    return float(ret)
            except ValueError:
                print("not a valid input\n")
                continue

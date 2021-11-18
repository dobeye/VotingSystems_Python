from Items import Candidate


class PrintUtilities:

    @staticmethod
    def print_tdl(tdl):

        """print every row in 2d list"""

        for i in tdl:
            print(i)

    @staticmethod
    def name_vote_array(vote_array):

        """prints a vote array with candidate names instead of candidate indices"""

        vote_array_with_names = []
        for rep, vote in enumerate(vote_array):
            vote_array_with_names.append([])
            for i in vote.ballot:
                vote_array_with_names[rep].append(Candidate.candidate_names[i])
        for vote in vote_array_with_names:
            print(f"{vote} \n")


def plurality_count(vote_array, candidate_list):

    """Run basic FPTP election by counting every voters top valid choice and adding support to the candidate with that index"""

    for candidate in candidate_list:
        candidate.set_support(0)

    for vote in vote_array:
        for i in range(vote.size):
            if candidate_list[vote.get_ballot_at(i)].exists:
                candidate_list[vote.get_ballot_at(i)].add_support(1)
                break


def borda_count(vote_array, candidate_list, borda_method=None):

    """run borda election with optional lambda inputs.
    gives each candidate a different amount of support depending on their placement in voter ballots.
    Default function is the amount of candidates minus the candidates placement in the ballot"""

    for candidate in candidate_list:
        candidate.set_support(0)

    for vote in vote_array:
        placement = 0
        for support in vote.ballot:
            if candidate_list[support].exists:
                if borda_method is None:
                    candidate_list[support].add_support(len(Candidate.candidate_names) - placement)
                else:
                    candidate_list[support].add_support(borda_method(placement))
                placement += 1
    return candidate_list


def pairwise_comparison(vote_array, candidate, opponent, validity_chart=None):

    """returns the amount of ballots ranking the candidate over the opponent and the amount of ballots ranking the opponent over the candidate. Support for
    validity chart which automatically gives invalid candidates a loss"""

    def vote_support_validity(contender):

        """Checks candidate support in ballot along with candidate validity. Validity chart can come in the form of either True and false list, in which case the function checks
        if the Bool variable at the place of the candidate index is true, or in the form of a candidate list, in which case the function checks that the candidate being checked is valid"""

        return vote.get_ballot_at(i) == contender and ((validity_chart is None) or (isinstance(validity_chart[0], Candidate) and validity_chart[contender].exists) or (isinstance(validity_chart[0], bool) and validity_chart[contender]))
    ret = [0, 0]
    for vote in vote_array:
        x = None
        for i in range(vote.size):
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

    """generates 2d list of every candidates voter support over all other candidates.
    Optional candidate list argument disqualifies invalid candidates,
    optional binary argument disregards amount of support and labels every win as 1 and every loss as 0"""

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

    """returns 2d list of every candidates voter support over every other candidate.
    Optional candidate list argument automatically gives every invalid candidate losses"""

    adjacency_matrix = [[0 for _ in range(Candidate.candidate_num)] for _ in range(Candidate.candidate_num)]
    for i in range(Candidate.candidate_num):
        for j in range(i + 1, Candidate.candidate_num):
            temp_array = pairwise_comparison(vote_array, i, j, candidate_list)
            adjacency_matrix[i][j] = temp_array[0]
            adjacency_matrix[j][i] = temp_array[1]

    return adjacency_matrix


def pairwise_support_cycle_check(unbeatable, candidate, pairwise_support_matrix, path=None):

    """recursively checks for a pairwise win cycle, and returns a win path along a pairwise support matrix going in a circle, or returns -1 if no such cycle exists"""

    if path is None:
        path = []
    if pairwise_support_matrix[candidate][unbeatable] > pairwise_support_matrix[unbeatable][candidate]:
        # if the currently checked candidate has beaten the first candidate checked, implying a cycle of pairwise wins
        return path + [(candidate, unbeatable, pairwise_support_matrix[candidate][unbeatable] - pairwise_support_matrix[unbeatable][candidate])]
    if all([pairwise_support_matrix[candidate][opponent] <= pairwise_support_matrix[opponent][candidate] for opponent in range(Candidate.candidate_num)]):
        # if the currently checked candidate has beaten no one, implying a dead end
        return -1

    for opponent in range(Candidate.candidate_num):
        if any([n[0] == candidate and n[1] == opponent for n in path]):
            # if this comparison has already been checked in the recursion
            return -1
        if pairwise_support_matrix[candidate][opponent] > pairwise_support_matrix[opponent][candidate]:
            recursion_variable = pairwise_support_cycle_check(unbeatable, opponent, pairwise_support_matrix, path + [(candidate, opponent, pairwise_support_matrix[candidate][opponent] - pairwise_support_matrix[opponent][candidate])])
            if recursion_variable != -1:
                return recursion_variable
    return -1


def smith_set_in_adjacency_matrix(adjacency_matrix):

    """returns the smith set in a given adjacency matrix by first adding every candidate with the maximum amount of pairwise wins,
    then adding every candidate who doesn't lose to the existing candidates"""

    # create a list with the number of pairwise wins per winner, meaning if the candidate with index 0 has beaten 5 candidates,
    # list index 0 would be 5
    copeland_score_list = []
    for i in adjacency_matrix:
        score = 0
        for j in i:
            if j != 0:
                score += 1
        copeland_score_list.append(score)

    # append every candidate with the maximal copeland score to the return list
    ret = []
    for i, support in enumerate(copeland_score_list):
        if support == max(copeland_score_list):
            ret.append(i)

    while True:
        # include every candidate not beaten by the candidates in the current return list, until no new candidates are found.
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

    """returns a list of every candidates appearances in every voters ballot, 0 meaning they didn't appear in the ballot"""

    judgement_matrix = [[] for _ in Candidate.candidate_names]
    for vote in vote_array:
        supported_candidates = set()
        for placement, candidate in enumerate(vote.ballot):
            judgement_matrix[candidate].append(Candidate.candidate_num - placement)
            supported_candidates.add(candidate)
        for candidate in set(range(Candidate.candidate_num)) - supported_candidates:
            judgement_matrix[candidate] += [0]

    return judgement_matrix


def mj_median_proponents_opponents(judgement_matrix, index, voter_num):

    """returns the majority judgement list median, the percentage of supporters relative to the median,
    and the percentage of non supporters relative to the median"""

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

    """grades all candidate support along a curve, so as to not include candidates with negative support,
    since only relative support is measured in elections"""

    curve = min([x.supporters for x in candidate_list])
    for candidate in candidate_list:
        candidate.add_support(-curve)


def find_list_median(integer_list):

    """finds list median (what did you really expect?)"""

    if len(integer_list) != 0:
        return sorted(integer_list, reverse=True)[int(len(integer_list) / 2)]
    return 0


def get_all_subclasses(class_input):

    """returns all class subclasses (what did you really expect?)"""

    ret = []

    for subclass in class_input.__subclasses__():
        ret.append(subclass)
        ret += get_all_subclasses(subclass)

    return ret


def input_validation(accepted_inputs, input_type, input_prompt):

    """simplifies getting user input by locking user in while loop until they enter a valid input.
    Valid inputs are defined as inputs included in the valid inputs list in case the valid input is a string,
    or in the valid range if the valid input is an integer/double"""

    while True:
        ret = input(input_prompt)
        if input_type is str:
            alt_inputs = [x[0] for x in accepted_inputs]
            if ret not in accepted_inputs:
                if ret not in alt_inputs:
                    print("not a valid input\n")
                    continue
                else:
                    return accepted_inputs[alt_inputs.index(ret)]
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


def dict_input_validation(valid_input_list, input_type, prompt):

    """(essentially an improved input validation method which uses a dictionary to define valid inputs, and only accepts input indices)
    simplifies getting user input by locking user in while loop until they enter a valid input.
        Valid inputs are defined as inputs included in the valid inputs list in case the valid input is a string,
        or in the valid range if the valid input is an integer/double"""

    print(prompt)
    if input_type is str:
        menu_dict = {place + 1: option for place, option in enumerate(valid_input_list)}
        while True:
            for i, j in menu_dict.items():
                print(f"{i}: {j}")

            choice = input()
            try:
                return menu_dict[int(choice)]
            except ValueError:
                print("not a valid input")
            except KeyError:
                print("not a valid option")

    elif input_type is int:
        while True:
            print(f"{valid_input_list[0]} - {valid_input_list[1]}")

            choice = input()
            try:
                if valid_input_list[0] <= int(choice) <= valid_input_list[1] and float(choice) == int(choice):
                    return int(choice)
                else:
                    raise ValueError
            except ValueError:
                print("not a valid input")

    elif input_type is float:
        while True:
            print(f"{valid_input_list[0]} -- {valid_input_list[1]}")

            choice = input()
            try:
                if valid_input_list[0] <= float(choice) <= valid_input_list[1]:
                    return float(choice)
                else:
                    raise ValueError
            except ValueError:
                print("not a valid input")

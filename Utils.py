import Generator
import main
import ElectionMethods


def print_tdl(tdl):
    for i in tdl:
        print(i)


def name_vote_array(vote_array):
    vote_array_with_names = []
    for rep, vote in enumerate(vote_array):
        vote_array_with_names.append([])
        for i in vote.get_ballot():
            vote_array_with_names[rep].append(main.candidate_names[i])
    for vote in vote_array_with_names:
        print(vote, "\n")


def print_vote_based_election(candidate_list):
    candidate_list = sorted(candidate_list, reverse=True)
    for candidate in candidate_list:
        print(candidate.get_name(), ": ", int(candidate.get_support()))


def print_percentage_election(candidate_list):
    candidate_list = sorted(candidate_list, reverse=True)
    for candidate in candidate_list:
        if candidate.get_support() == int(candidate.get_support()):
            print(candidate.get_name(), ": ", int(candidate.get_support()))
            continue
        print(candidate.get_name(), ": ", int(candidate.get_support() * 100) / 100)


def print_permutation_election(election_results):
    for placement, i in enumerate(election_results):
        print("#" + str(placement + 1) + ": " + str(main.candidate_names[i]))


def print_winner_only_election(winner):
    print("winner: " + winner)


def print_randomly_generated_election(votes):
    vote_array = Generator.generate_random_vote_array(votes)
    print("\nFirst Past The Post voting \n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_fptp_election(vote_array))
    print("\nAnti Plurality voting\n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_anti_plurality_election(vote_array))
    print("\nApproval voting \n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_approval_election(vote_array))
    print("\nBorda voting \n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_borda_election(vote_array))
    print("\nBorda Nauru voting \n")
    print_percentage_election(ElectionMethods.ScoreBasedElectionMethods.run_nauru_election(vote_array))
    print("\nNanson voting \n")
    print_vote_based_election(ElectionMethods.RunoffElectionMethods.run_nanson_election(vote_array))
    print("\nCoombs rule voting \n")
    print_vote_based_election(ElectionMethods.RunoffElectionMethods.run_coombs_election(vote_array))
    print("\nInstant Runoff voting \n")
    print_vote_based_election(ElectionMethods.RunoffElectionMethods.run_instant_runoff_election(vote_array))
    print("\nGeller Instant Runoff voting\n")
    print_vote_based_election(ElectionMethods.RunoffElectionMethods.run_geller_irv_election(vote_array))
    print("\nBucklin voting \n")
    print_vote_based_election(ElectionMethods.AlternativeElectionMethods.run_bucklin_election(vote_array))
    print("\nCopeland voting \n")
    print_percentage_election(ElectionMethods.ScoreBasedElectionMethods.run_copeland_election(vote_array))
    print("\nSequential Pairwise voting \n")
    print_permutation_election(
        ElectionMethods.PermutationElectionMethods.run_permutation_sequential_pairwise_election(vote_array))
    print("\nMin Max win voting \n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_min_max_winning_election(vote_array))
    print("\nMin Max margin voting \n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_min_max_margin_election(vote_array))
    print("\nSchulze voting \n")
    print_permutation_election(ElectionMethods.PermutationElectionMethods.run_schulze_election(vote_array))
    print("\nRanked Pairs election\n")
    print_permutation_election(ElectionMethods.PermutationElectionMethods.run_ranked_pairs_election(vote_array))
    print("\nKemeny Young voting \n")
    print_permutation_election(ElectionMethods.PermutationElectionMethods.run_kemeny_young_election(vote_array))
    print("\nMajority Judgement voting\n")
    print_vote_based_election(ElectionMethods.ScoreBasedElectionMethods.run_majority_judgement_election(vote_array))
    print("\nAlternative Tideman voting\n")
    print_permutation_election(ElectionMethods.AlternativeElectionMethods.run_alternative_tideman_election(vote_array))


def fptp_pseudo_vote(vote_array, candidate_list):
    for candidate in candidate_list:
        candidate.set_support(0)
    for vote in vote_array:
        """while True:
            if vote.get_vote_validity():
                if candidate_list[vote.get_ballot_at_top_choice()].get_validity():
                    candidate_list[vote.get_ballot_at_top_choice()].add_support(1)
                    break
                vote.remove_top_choice()
                continue
            break"""
        for i in range(vote.get_ballot_length()):
            if candidate_list[vote.get_ballot_at(i)].get_validity():
                candidate_list[vote.get_ballot_at(i)].add_support(1)
                break


def borda_count(vote_array, candidate_list):
    for vote in vote_array:
        for placement, support in enumerate(vote.get_ballot()):
            candidate_list[support].add_support(main.candidate_num - placement)


def last_place_invalidation(candidate_list):
    contender_chosen = False
    contender = 0
    for candidate in candidate_list:
        if candidate.get_validity():
            if not contender_chosen:
                contender = candidate
                contender_chosen = True
            if candidate.get_support() < contender.get_support():
                contender = candidate
    candidate_list[contender.get_index()].set_validity(False)


def pairwise_comparison(vote_array, candidate, opponent, validity_chart=None):
    ret = [0, 0]
    for vote in vote_array:
        for i in range(vote.get_ballot_length()):
            if validity_chart is not None:
                if vote.get_ballot_at(i) == candidate:
                    if validity_chart[candidate].get_validity():
                        ret[0] += 1
                        break
                if vote.get_ballot_at(i) == opponent:
                    if validity_chart[opponent].get_validity():
                        ret[1] += 1
                        break
            else:
                if vote.get_ballot_at(i) == candidate:
                    ret[0] += 1
                    break
                if vote.get_ballot_at(i) == opponent:
                    ret[1] += 1
                    break

    return ret


def generate_adjacency_matrix(vote_array, candidate_list=None):
    adjacency_matrix = [[0 for _ in range(main.candidate_num)] for _ in range(main.candidate_num)]
    for i in range(main.candidate_num):
        for j in range(i + 1, main.candidate_num):
            temp_array = pairwise_comparison(vote_array, i, j, candidate_list)

            if temp_array[0] > temp_array[1]:
                adjacency_matrix[i][j] = temp_array[0]
            elif temp_array[1] > temp_array[0]:
                adjacency_matrix[j][i] = temp_array[1]

    return adjacency_matrix


def adjacency_cycle_check(unbeatable, candidate, adjacency_matrix, path, layer):
    if adjacency_matrix[candidate][unbeatable] != 0:
        return min(path, key=lambda x: x[2])
    if all([x == 0 for x in adjacency_matrix[candidate]]):
        return -1

    for opponent, support in enumerate(adjacency_matrix[candidate]):
        if any([n[0] == candidate and n[1] == opponent for n in path]):
            return -1
        if support != 0:
            recursion_variable = adjacency_cycle_check(unbeatable, opponent, adjacency_matrix,
                                                       path + [[candidate, opponent, support]], layer + 1)
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


def election_results_curve(candidate_list):
    curve = 0
    for candidate in candidate_list:
        if candidate.get_support() < curve:
            curve = candidate.get_support()
    for candidate in candidate_list:
        candidate.add_support(-curve)

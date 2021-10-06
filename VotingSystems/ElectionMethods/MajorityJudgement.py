import Generator
import main


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

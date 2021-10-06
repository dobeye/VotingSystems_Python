import Generator
import main


def run_borda_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    for vote in vote_array:
        for placement, support in enumerate(vote.get_ballot()):
            ret[support].add_support(main.candidate_num - placement)

    return ret

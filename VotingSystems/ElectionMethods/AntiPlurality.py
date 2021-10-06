import Generator
import main


def run_anti_plurality_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    for vote in vote_array:
        if vote.get_hated_candidate() != -1:
            ret[vote.get_hated_candidate()].add_support(-1)

    return ret

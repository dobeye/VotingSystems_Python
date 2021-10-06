import Generator
import main


def run_approval_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    for vote in vote_array:
        for support in vote.get_ballot():
            ret[support].add_support(1)

    return ret

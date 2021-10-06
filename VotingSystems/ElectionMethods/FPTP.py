import Generator
import Utils
import main


def run_fptp_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    for vote in vote_array:
        ret[vote.get_ballot_at_top_choice()].add_support(1)
    return ret


def run_alt_fptp_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    temp_array = vote_array
    Utils.fptp_pseudo_vote(temp_array, ret)
    return ret

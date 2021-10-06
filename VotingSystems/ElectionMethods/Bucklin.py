import Generator
import main


def run_bucklin_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    for i in range(main.candidate_num):
        for vote in vote_array:
            if vote.check_validity_at(i):
                ret[vote.get_ballot_at(i)].add_support(1)

        for candidate in ret:
            if candidate.get_support() > len(vote_array) / 2:
                return ret

    return ret

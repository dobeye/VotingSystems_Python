import Generator
import main


def run_nanson_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    temp_array = vote_array

    """This step should not be remotely necessary as both coombs rule voting and instant runoff voting use temporary
    voting arrays. Except for some reason without this step they both generate the same results. I give up"""
    for vote in temp_array:
        vote.set_top_choice(0)
        vote.set_vote_validity(True)

    for i in range(len(ret) - 2):
        valid_candidates = 0
        for candidate in ret:
            candidate.set_support(0)
            if candidate.get_validity():
                valid_candidates += 1

        for vote in vote_array:
            placement = 0
            for support in vote.get_ballot():
                if ret[support].get_validity():
                    ret[support].add_support(valid_candidates - placement)
                    placement += 1

        if valid_candidates <= 2:
            return ret

        counted_votes = 0
        for candidate in ret:
            counted_votes += candidate.get_support()

        for candidate in ret:
            if candidate.get_support() < counted_votes / valid_candidates:
                candidate.set_validity(False)

    return ret

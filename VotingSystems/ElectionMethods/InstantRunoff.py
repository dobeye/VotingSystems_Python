import Generator
import Utils
import main


def run_instant_runoff_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    temp_array = vote_array

    # This step should not be remotely necessary as both coombs rule voting and instant runoff voting use temporary
    # voting arrays. Except for some reason without this step they both generate the same results. I give up
    for vote in temp_array:
        vote.set_top_choice(0)
        vote.set_vote_validity(True)
    for i in range(len(ret) - 2):
        Utils.fptp_pseudo_vote(temp_array, ret)
        counted_votes = 0
        for candidate in ret:
            counted_votes += candidate.get_support()

        for candidate in ret:
            if candidate.get_support() > counted_votes / 2:
                return ret

        Utils.last_place_invalidation(ret)

    Utils.fptp_pseudo_vote(temp_array, ret)

    return ret

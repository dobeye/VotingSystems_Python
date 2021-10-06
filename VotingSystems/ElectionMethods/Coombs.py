import Generator
import Utils
import main


def run_coombs_election(vote_array):
    ret = Generator.generate_candidate_list(main.candidate_names)
    temp_array = vote_array

    # This step should not be remotely necessary as both coombs rule voting and instant runoff voting use temporary
    # voting arrays. Except for some reason without this step they both generate the same results. I give up
    for vote in temp_array:
        vote.set_top_choice(0)
        vote.set_vote_validity(True)
    for i in range(len(ret) - 2, 0, -1):
        Utils.fptp_pseudo_vote(temp_array, ret)
        counted_votes = 0
        for candidate in ret:
            counted_votes += candidate.get_support()

        for candidate in ret:
            if candidate.get_support() > counted_votes / 2:
                return ret

        for candidate in ret:
            candidate.set_support(0)
            if candidate.get_validity():
                for vote in temp_array:
                    if vote.get_vote_validity():
                        appearance = False
                        for j in range(i + 1):
                            if vote.get_ballot_at(j) == candidate.get_index():
                                appearance = True
                                break
                        if not appearance:
                            candidate.add_support(-1)

        contender_chosen = False
        contender = 0
        for candidate in ret:
            if candidate.get_validity():
                if not contender_chosen:
                    contender = candidate
                    contender_chosen = True
                if candidate.get_support() < contender.get_support():
                    contender = candidate
        ret[contender.get_index()].set_validity(False)

    Utils.fptp_pseudo_vote(temp_array, ret)

    return ret

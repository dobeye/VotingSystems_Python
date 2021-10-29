import main


class Vote:
    def __init__(self, support_arr, hated_candidate=None, ideology_array=None):
        self.support_arr = support_arr
        self.vote_length = len(support_arr)
        self.ideology = ideology_array
        if self.vote_length == len(main.candidate_names):
            self.hated_candidate = support_arr[-1]
        else:
            self.hated_candidate = hated_candidate

    def __repr__(self):
        return str(self.ideology) + ": " + str(self.support_arr) + " (" + str(self.hated_candidate) + ")"

    def get_ballot(self):
        return self.support_arr

    def get_ballot_at(self, pos):
        if pos >= self.vote_length:
            return -1
        return self.support_arr[pos]

    def get_hated_candidate(self):
        return self.hated_candidate

    def check_validity_at(self, pos):
        return self.vote_length > pos

    def get_ballot_length(self):
        return self.vote_length

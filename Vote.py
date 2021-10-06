import main


class Vote:
    def __init__(self, support_arr, hated_candidate=-1):
        self.support_arr = support_arr
        self.top_choice = 0
        self.vote_length = len(support_arr)
        if self.vote_length == len(main.candidate_names):
            self.hated_candidate = support_arr[-1]
        else:
            self.hated_candidate = hated_candidate
        self.vote_validity = True

    def get_ballot(self):
        return self.support_arr

    def get_ballot_from_top_choice(self):
        return self.support_arr[self.top_choice:]

    def get_ballot_at(self, pos):
        if pos >= self.vote_length:
            return -1
        return self.support_arr[pos]

    def get_hated_candidate(self):
        return self.hated_candidate

    def get_ballot_at_top_choice(self):
        return self.support_arr[self.top_choice]

    def check_validity_at(self, pos):
        return self.vote_length > pos

    def get_ballot_length(self):
        return self.vote_length

    def get_top_choice(self):
        return self.top_choice

    def set_top_choice(self, top_choice):
        self.top_choice = top_choice
        if self.top_choice >= self.vote_length:
            self.vote_validity = False

    def remove_top_choice(self):
        self.top_choice += 1
        if self.top_choice >= self.vote_length:
            self.vote_validity = False

    def get_vote_validity(self):
        return self.vote_validity

    def set_vote_validity(self, vote_validity):
        self.vote_validity = vote_validity

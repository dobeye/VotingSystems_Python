class Candidate:
    """ The candidate object represents a candidate in an election, with a name (purely for aesthetic purposes), an index used to identify the candidate,
            an ideology array which is used when forming an informed voter list by comparing voter ideology to candidate ideology.
            All candidates start out with no support, no placement, and exist as valid candidates."""

    candidate_names = ["Trump", "Clinton", "Stein", "Sanders", "Biden", "Buttigieg", "Iddo", "Cruz"]
    candidate_num = len(candidate_names)
    candidate_ideology = [[0.25, 1.0 / 3], [0.5, 1.0 / 3], [0.75, 1.0 / 3], [0.25, 2.0 / 3], [0.5, 2.0 / 3],
                          [0.75, 2.0 / 3], [1.0 / 3, 0], [2.0 / 3, 1]]

    def __init__(self, name, index, ideology_array):
        if ideology_array is None:
            ideology_array = [0.5, 0.5]
        self.identifier = name
        self.index = index
        self.support = 0
        self.placement = 0
        self.ideology = ideology_array
        self.validity = True

    def __eq__(self, other):
        return self.support == other.support

    def __lt__(self, other):
        return self.support < other.support

    def __str__(self):
        return_string = self.name + "(" + str(self.index) + ") support: " + str(self.support) + " placement: " + str(self.placement)
        if not self.validity:
            return_string += " Invalid"
        return return_string

    def __repr__(self):
        return str(self.index) + " [" + str(int(self.ideology[0] * 10 ** 3) / 10 ** 3) + ", " + str(int(self.ideology[1] * 10 ** 3) / 10 ** 3) + "]: " + str(self.support) + " (" + str(self.placement) + ")"

# region properties
    @property
    def name(self):
        return self.identifier

    @property
    def number(self):
        return self.index

    @property
    def ideology_array(self):
        return self.ideology

    @property
    def supporters(self):
        return self.support

    @property
    def exists(self):
        return self.validity

    @property
    def place(self):
        return self.placement
# endregion

    def set_support(self, support):
        self.support = support

    def add_support(self, support):
        self.support += support

    def set_validity(self, validity):
        self.validity = validity

    def set_placement(self, placement):
        self.placement = placement

    def demote_placement(self, demotion):
        self.placement += demotion

    @staticmethod
    def placement_by_support(candidate_list):
        """assign each candidate a placement according to their amount of support.
        sets each candidate with a current placement their placement according to an index and a changing add variable, and then checks if any other candidates have
        the same level of support, and if they do their placement is set accordingly and the add variable is edited"""
        add_variable = 1
        for index, candidate in enumerate(sorted(candidate_list, reverse=True)):
            if candidate.place == 0:
                candidate.set_placement(index + add_variable)

                for opponent in sorted(candidate_list, reverse=True)[index + 1:]:
                    if candidate == opponent:
                        opponent.set_placement(candidate.place)
                        add_variable -= 1


class Vote:

    """The vote object represents a voter with an ideology (used to generate supported and hated candidates),
    supported candidates, and a single hated candidate used for anti plurality."""

    def __init__(self, support_arr, hated_candidate=None, ideology_array=None):
        self.support_arr = support_arr
        self.vote_length = len(support_arr)
        self.ideology = ideology_array
        if self.vote_length == Candidate.candidate_num:
            self.hated_candidate = support_arr[-1]
        else:
            self.hated_candidate = hated_candidate

    def __repr__(self):
        return str(self.ideology) + ": " + str(self.support_arr) + " (" + str(self.hated_candidate) + ")"

# region properties
    @property
    def ballot(self):
        return self.support_arr

    @property
    def size(self):
        return self.vote_length

    @property
    def hated(self):
        return self.hated_candidate
# endregion

    def check_validity_at(self, pos):
        return self.vote_length > pos

    def get_ballot_at(self, pos):
        if pos >= self.vote_length:
            return -1
        return self.support_arr[pos]

class Candidate:

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
        add_variable = 1
        for index, candidate in enumerate(sorted(candidate_list, reverse=True)):
            if candidate.place == 0:
                candidate.set_placement(index + add_variable)

                for opponent in sorted(candidate_list, reverse=True)[index + 1:]:
                    if candidate == opponent:
                        opponent.set_placement(candidate.place)
                        add_variable -= 1

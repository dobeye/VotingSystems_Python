class Candidate:

    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.support = 0
        self.placement = 0
        self.validity = True

    def __eq__(self, other):
        return self.support == other.support

    def __lt__(self, other):
        return self.support < other.support

    def __str__(self):
        return_string = self.name + "(" + str(self.index) + ") support: " + str(self.support) + " placement: " + str(self.placement)
        if self.validity:
            return return_string
        return return_string + " Invalid"

    def __repr__(self):
        return str(self.index) + ": " + str(self.support) + " (" + str(self.placement) + ")"

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_support(self):
        return self.support

    def set_support(self, support):
        self.support = support

    def add_support(self, support):
        self.support += support

    def get_validity(self):
        return self.validity

    def set_validity(self, validity):
        self.validity = validity

    def get_placement(self):
        return self.placement

    def set_placement(self, placement):
        self.placement = placement

    def demote_placement(self, demotion):
        self.placement += demotion

    @staticmethod
    def placement_by_support(candidate_list):
        add_variable = 1
        for index, candidate in enumerate(sorted(candidate_list, reverse=True)):
            candidate.set_placement(index + add_variable)

            for opponent in sorted(candidate_list, reverse=True)[:index]:
                if candidate == opponent:
                    candidate.set_placement(opponent.get_placement())
                    add_variable -= 1

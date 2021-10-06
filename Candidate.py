class Candidate:

    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.support = 0
        self.validity = True

    def __eq__(self, other):
        return self.support == other.support

    def __lt__(self, other):
        return self.support < other.support

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

from Election import *


def main():
    voter_type = Utils.input_validation(["informed", "random"], str, "Election simulator initiated.\nChoose voter type (informed or random)\n")
    if voter_type == "informed":
        candidate_generation_method = Utils.input_validation(["default", "custom", "random"], str, 'Choose candidate array type (default, custom, or random)\n')
        if candidate_generation_method == "custom":
            Candidate.candidate_names = []
            Candidate.candidate_ideology = []
            while True:
                candidate_name = input("input candidate name\n")
                candidate_ideology_x = Utils.input_validation([0, 1], float, "input candidate ideology x axis (between 0 and 1)\n")
                candidate_ideology_y = Utils.input_validation([0, 1], float, "input candidate ideology y axis (between 0 and 1)\n")
                accepted = Utils.input_validation(["yes", "no"], str, ("is " + candidate_name + " [" + str(candidate_ideology_x) + ", " + str(candidate_ideology_y) + "] your desired candidate? (answer yes or no)\n"))

                if accepted == "no":
                    continue
                Candidate.candidate_names.append(candidate_name)
                Candidate.candidate_ideology.append([float(candidate_ideology_y), float(candidate_ideology_y)])
                accepted = Utils.input_validation(["yes", "no"], str, (str(Candidate.candidate_names) + " is that your entire candidate list? (answer yes or no)\n"))
                if accepted == "yes":
                    Candidate.candidate_num = len(Candidate.candidate_names)
                    break
        elif candidate_generation_method == "random":
            Candidate.candidate_ideology = None

    candidate_list = Generator.generate_candidate_list(Candidate.candidate_ideology)
    voter_amount = Utils.input_validation([0, 1000000000000], int, "Choose voter amount\n")
    vote_array = Generator.generate_informed_vote_array(voter_amount, candidate_list) if voter_type == "informed" else Generator.generate_random_vote_array(voter_amount)
    all_elections = AllTypeElection(vote_array, candidate_list)

    all_elections.print_all_elections()
    if all_elections.get_condorcet_winner() is not None:
        print(Candidate.candidate_names[all_elections.get_condorcet_winner()])
        all_elections.print_all_condorcet_cycles()
    else:
        print("")
        all_elections.print_all_condorcet_cycles(True)
        print("all")
        all_elections.print_all_condorcet_cycles()


if __name__ == "__main__":
    main()

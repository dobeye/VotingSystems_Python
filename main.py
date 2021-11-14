from Election import AllTypeElection
import Utils
from Items import Candidate
import Generator


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
    print("All elections have been simulated and the results are in!", end=" ")

    while True:
        analysis_type = Utils.input_validation(["universal", "class", "individual", "exit"], str, "Which analysis type would you like to enter? (answer universal, class, individual, or exit)\n")

        if analysis_type == "exit":
            break
        elif analysis_type == "universal":
            analysis_function = Utils.input_validation(["condorcet winner", "smith cycles", "all cycles", "wins per candidate", "winner by election", "print all elections", "candidate comparison", "exit"], str,
                                                       "Would you like to see: The condorcet winner, the smith cycles, all pairwise cycles, wins per candidate, the winner of each election, print all elections, candidate comparison, or return to main menu?)\n")

            if analysis_function == "condorcet winner":
                if all_elections.get_condorcet_winner() is not None:
                    print(Candidate.candidate_names[all_elections.get_condorcet_winner()])
                else:
                    print("no condorcet winner")
            elif analysis_function == "smith cycles":
                all_elections.print_all_condorcet_cycles(True)
            elif analysis_function == "all cycles":
                all_elections.print_all_condorcet_cycles()
            elif analysis_function == "wins per candidate":
                all_elections.print_wins_per_candidate()
            elif analysis_function == "winner by election":
                all_elections.print_winner_by_election()
            elif analysis_function == "print all elections":
                all_elections.print_all_elections()
            elif analysis_function == "candidate comparison":
                candidate1 = Utils.input_validation(Candidate.candidate_names, str, "Enter your first candidate\n")
                candidate2 = Utils.input_validation(Candidate.candidate_names, str, "Enter your second candidate\n")
                if candidate1 == candidate2:
                    print("you can't compare a candidate to themself!")
                else:
                    all_elections.print_pairwise_comparison(Candidate.candidate_names.index(candidate1), Candidate.candidate_names.index(candidate2))


if __name__ == "__main__":
    main()

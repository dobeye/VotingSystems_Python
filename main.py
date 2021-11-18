from Election import AllTypeElection
import Utils
from Items import Candidate
import Generator


def main():

    match Utils.dict_input_validation(["import", "generate"], str, "Would you like to import and existing election"
                                                                   "or generate a new election"):
        case "import":
            all_elections = None
            # TODO: create import options
        case "generate":
            voter_amount = Utils.dict_input_validation([0, 1000000000000], int, "Choose voter amount")

            voter_type = Utils.dict_input_validation(["informed", "random"], str, "Choose voter type")
            if voter_type == "informed":
                match Utils.dict_input_validation(["default", "custom", "random"], str, 'Choose candidate array type'):
                    case "custom":
                        while True:
                            Candidate.candidate_names = []
                            Candidate.candidate_ideology = []
                            candidate_name = input("input candidate name\n")
                            candidate_ideology_x = Utils.dict_input_validation([0, 1], float,
                                                                               "input candidate ideology x axis")
                            candidate_ideology_y = Utils.dict_input_validation([0, 1], float,
                                                                               "input candidate ideology y axis")
                            match Utils.dict_input_validation(["yes", "no"], str, f"is {candidate_name} [{candidate_ideology_x},"
                                                                                  f"{candidate_ideology_y}] your desired candidate?"):
                                case "yes":
                                    Candidate.candidate_names.append(candidate_name)
                                    Candidate.candidate_ideology.append([float(candidate_ideology_y), float(candidate_ideology_y)])
                                case "no":
                                    continue

                            match Utils.dict_input_validation(["yes", "no"], str, f"is {Candidate.candidate_names} your entire candidate list?"):
                                case "yes":
                                    Candidate.candidate_num = len(Candidate.candidate_names)
                                    break
                                case "no":
                                    pass
                    case "random":
                        Candidate.candidate_ideology = None
                    case "default":
                        pass

            candidate_list = Generator.generate_candidate_list(Candidate.candidate_ideology)
            vote_list = Generator.generate_informed_vote_array(voter_amount, candidate_list) if voter_type == "informed"\
                else Generator.generate_random_vote_array(voter_amount)

            all_elections = AllTypeElection(vote_list, candidate_list)

    print("All elections have been simulated and the results are in!", end=" ")

    while True:
        match Utils.dict_input_validation(["universal", "individual", "export", "exit"], str, "Choose election analysis type"):
            case "universal":
                match Utils.dict_input_validation(["condorcet winner", "smith cycles", "all cycles", "wins per candidate",
                                                   "winner by election", "print all elections", "candidate comparison", "exit"],
                                                  str, "choose universal analysis type"):
                    # this method of getting user input is still absolute garbage, because adding in another input option means adding it both to the valid input list and to the case list.
                    case "condorcet winner":
                        # noinspection PyUnboundLocalVariable
                        if all_elections.get_condorcet_winner() is not None:
                            print(Candidate.candidate_names[all_elections.get_condorcet_winner()])
                        else:
                            print("no condorcet winner")
                    case "smith cycles":
                        all_elections.print_all_condorcet_cycles(True)
                    case "all cycles":
                        all_elections.print_all_condorcet_cycles()
                    case "wins per candidate":
                        all_elections.print_wins_per_candidate()
                    case "winner by election":
                        all_elections.print_winner_by_election()
                    case "print all elections":
                        all_elections.print_all_elections()
                    case "candidate comparison":
                        candidate1 = Utils.dict_input_validation(Candidate.candidate_names, str, "Enter your first candidate")
                        candidate2 = Utils.dict_input_validation(Candidate.candidate_names, str, "Enter your second candidate")
                        if candidate1 == candidate2:
                            print("you can't compare a candidate to themself!")
                        else:
                            all_elections.print_pairwise_comparison(Candidate.candidate_names.index(candidate1),
                                                                    Candidate.candidate_names.index(candidate2))

            case "individual":
                pass

            case "export":
                pass
            # TODO: Create export options

            case "exit":
                break


if __name__ == "__main__":
    main()

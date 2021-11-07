from Election import *

candidate_names = ["Trump", "Clinton", "Stein", "Sanders", "Biden", "Buttigieg", "Iddo", "Cruz"]
candidate_num = len(candidate_names)
candidate_ideology = [[0.25, 1.0/3], [0.5, 1.0/3], [0.75, 1.0/3], [0.25, 2.0/3], [0.5, 2.0/3], [0.75, 2.0/3], [1.0/3, 0], [2.0/3, 1]]


def main():
    candidate_generation_method = Utils.input_validation(["default", "custom", "random"], str, 'Election simulator initiated. choose default, custom, or random candidate array by writing default, custom, or random\n')

    if candidate_generation_method == "custom":
        main.candidate_names = []
        main.candidate_ideology = []
        while True:
            candidate_name = input("input candidate name\n")
            candidate_ideology_x = Utils.input_validation([0, 1], float, "input candidate ideology x axis (between 0 and 1)\n")
            candidate_ideology_y = Utils.input_validation([0, 1], float, "input candidate ideology y axis (between 0 and 1)\n")
            accepted = Utils.input_validation(["yes", "no"], str, ("is " + candidate_name + " [" + str(candidate_ideology_x) + ", " + str(candidate_ideology_y) + "] your desired candidate? (answer yes or no)\n"))

            if accepted == "no":
                continue
            main.candidate_names.append(candidate_name)
            main.candidate_ideology.append([float(candidate_ideology_y), float(candidate_ideology_y)])
            accepted = Utils.input_validation(["yes", "no"], str, (str(main.candidate_names) + " is that your entire candidate list? (answer yes or no)\n"))
            if accepted == "yes":
                main.candidate_num = len(candidate_names)
                break
    if candidate_generation_method == "random":
        main.candidate_ideology = None
    candidate_list = Generator.generate_candidate_list(candidate_ideology)
    voter_amount = Utils.input_validation([0, 1000000000000], int, "Choose voter amount\n")
    all_elections = AllTypeElection(Generator.generate_informed_vote_array(voter_amount, candidate_list), candidate_list)
    all_elections.print_all_elections()


if __name__ == "__main__":
    main()

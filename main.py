import Election
import ElectionMethods
import Generator
import Utils
from Candidate import Candidate

candidate_names = ["Trump", "Clinton", "Stein", "Sanders", "Biden", "Buttigieg"]
candidate_list = [Candidate(y, x) for x, y in enumerate(candidate_names)]
candidate_num = len(candidate_names)


def main():
    vote_array = Generator.generate_random_vote_array(2000)
    truth = []
    for i in range(200):
        truth.append(Election.AlternativeTideman(vote_array).get_winner().get_index() == ElectionMethods.AlternativeElectionMethods.run_alternative_tideman_election(vote_array)[0])
    print(all(truth))
    """Utils.PrintUtilities.print_randomly_generated_election(vote_array, False)
    print(Election.FPTP(vote_array).get_winner())
    print(Election.AntiPlurality(vote_array).get_winner())
    print(Election.Copeland(vote_array).get_winner())
    print(Election.Approval(vote_array).get_winner())
    print(Election.Borda(vote_array).get_winner())
    print(Election.BordaNauru(vote_array).get_winner())
    print(Election.MinMax(vote_array, "Winning").get_winner())
    print(Election.MinMax(vote_array, "Margin").get_winner())
    print(Election.MinMax(vote_array, "Pairwise Opposition").get_winner())
    print(Election.MajorityJudgement(vote_array, "Typical").get_winner())
    print(Election.MajorityJudgement(vote_array, "Usual").get_winner())
    print(Election.MajorityJudgement(vote_array, "Central").get_winner())
    print(Election.InstantRunOff(vote_array).get_winner())
    print(Election.CoombsRule(vote_array).get_winner())
    print(Election.BaldwinMethod(vote_array).get_winner())
    print(Election.NansonMethod(vote_array).get_winner())
    print(Election.KemenyYoung(vote_array).get_winner())
    print(Election.RankedPairs(vote_array).get_winner())
    print(Election.Schulze(vote_array).get_winner())
    print(Election.SequentialPairwise(vote_array).get_winner())"""
    """truth = []
    for i in range(200):
        vote_array = Generator.generate_random_vote_array(2000)
        copeland_list = ElectionMethods.ScoreBasedElectionMethods.run_copeland_election(vote_array)
        if max(copeland_list).get_support() == 5:
            nanson_list = ElectionMethods.RunoffElectionMethods.run_nanson_election(vote_array)
            truth.append(max(nanson_list).get_index() == max(copeland_list).get_index())
            if not truth[-1]:
                print("problem", Utils.PrintUtilities.print_vote_based_election(nanson_list), i, Utils.PrintUtilities.print_vote_based_election(copeland_list))
                break
    print(all(truth))"""


if __name__ == "__main__":
    main()

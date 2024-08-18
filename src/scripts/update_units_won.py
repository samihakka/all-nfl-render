

import requests
from mongo_support import MongoConnect



mongo = MongoConnect()

coll = mongo.get_collection("getting_there")

document = coll.find_one({"season": 2023})

all_teams = document["team_stats"]
filter = {"season": 2023}


for team in all_teams:

    did_cover = 0
    no_cover = 0
    pushed = 0
    print(team)
    for i, game in enumerate(all_teams[team]["game_log"]):

        scores = game["score"].split('-')
        if game["home_away"] == "away":
            team_score = scores[1]
            other_team_score = scores[0]
        else:
            team_score = scores[0]
            other_team_score = scores[1]
        # print("team score: ", team_score)
        # print("other team score: ", other_team_score)
        
        diff = int(team_score) - int(other_team_score)
        spread = game["spread"]
        if spread[0] == '+':

            if diff > 0:
                covered = "covered"
            else:
                if float(abs(diff)) == float(spread[1:]):
                    cover = "push"
                elif abs(diff) < float(spread[1:]):
                    covered = "covered"
                else:
                    covered = "no_cover"
        else:
            
            if diff < 0:
                covered = "no_cover"
            else:
                if float(diff) == float(spread[1:]):
                    cover = "push"
                elif diff > float(spread[1:]):
                    covered = "covered"
                else:
                    covered = "no_cover"
        
        if covered == "covered":
            print(f"week {i+1}: covered!")
            did_cover += 1
        elif covered == "push":
            pushed += 1
        elif covered == "no_cover":
            print(f"week {i+1}: No cover.")
            no_cover += 1
        else:
            print("ERROR BRUH")
            exit()


    print("spreads covered: ", did_cover)
    print("spreads lost:", no_cover)
    print("spreads pushed: ", pushed)

    total = did_cover - no_cover


    # print("avg ou: ", avg_ou)
    # print("avg spread: ", avg_spread)
    # print("team: ", team)

    update_spread_unit_won = {"$set": {f"team_stats.{team}.spread_units_won": total}}
    # update_spread = {"$set": {f"team_stats.{team}.avg_spread": avg_spread}}
    coll.update_one(filter, update_spread_unit_won)
    # print("average o/u", round(average_ou, 1))
    # exit()




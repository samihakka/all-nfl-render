

import requests
from mongo_support import MongoConnect



mongo = MongoConnect()

coll = mongo.get_collection("getting_there")

document = coll.find_one({"season": 2023})

all_teams = document["team_stats"]
filter = {"season": 2023}


for team in all_teams:

    ou = []
    spread = []

    for game in all_teams[team]["game_log"]:
        print("its in da game")
        print(game)
        ou.append(game["over/under"])
        spread.append(float(game["spread"]))

    avg_ou = round(sum(ou) / len(ou), 1)
    avg_spread = round(sum(spread) / len(spread), 1)

    print("avg ou: ", avg_ou)
    print("avg spread: ", avg_spread)
    print("team: ", team)

    update_ou = {"$set": {f"team_stats.{team}.avg_over_under": avg_ou}}
    update_spread = {"$set": {f"team_stats.{team}.avg_spread": avg_spread}}
    coll.update_one(filter, update_ou)
    coll.update_one(filter, update_spread)
    # print("average o/u", round(average_ou, 1))
    # exit()







# Define the update to add the "stadium" field
# update = {"$set": {"team_stats.1.stadium": "Mercedes-Benz Stadium"}}

# # Perform the update
# coll.update_one(filter, update)

# print(cheddar)
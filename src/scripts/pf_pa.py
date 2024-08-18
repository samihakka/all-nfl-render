


import requests
from mongo_support import MongoConnect



mongo = MongoConnect()

coll = mongo.get_collection("getting_there")

document = coll.find_one({"season": 2023})

all_teams = document["team_stats"]
filter = {"season": 2023}



def get_request(url):

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
    return json_data


for team in all_teams:
    # team = team_id
    
    # make a request

    team_url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/types/2/teams/{team}/record"

    data = get_request(team_url)
    
    item_1 = data["items"][0]["stats"]
    pa_result = next((item for item in item_1 if item["name"] == "pointsAgainst"), None)
    pf_result = next((item for item in item_1 if item["name"] == "pointsFor"), None)

    pa = pa_result["value"]
    pf = pf_result["value"]

    update_pa = {"$set": {f"team_stats.{team}.points against": pa}}
    update_pf = {"$set": {f"team_stats.{team}.points for": pf}}

    coll.update_one(filter, update_pa)
    coll.update_one(filter, update_pf)
    # exit()




    # update_ou = {"$set": {f"team_stats.{team}.avg_over_under": avg_ou}}
    # update_spread = {"$set": {f"team_stats.{team}.avg_spread": avg_spread}}
    # coll.update_one(filter, update_ou)
    # coll.update_one(filter, update_spread)
    # print("average o/u", round(average_ou, 1))
    # exit()







# Define the update to add the "stadium" field
# update = {"$set": {"team_stats.1.stadium": "Mercedes-Benz Stadium"}}

# # Perform the update
# coll.update_one(filter, update)

# print(cheddar)


import requests
from mongo_support import MongoConnect


# sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams/25/events

mongo = MongoConnect()

coll = mongo.get_collection("schedule_predict")


def get_request(url):

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
    return json_data



teams_url = "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/teams?lang=en&region=us&limit=100"
teams = get_request(teams_url)

# keys: team ID
# vals: team Name
# Ex: {22: "ARI", 25: "SF", ...}
team_id_map = {}

for team in teams["items"]:
    team_info = get_request(team["$ref"])

    team_id_map[team_info["id"]] = {
        "name": team_info["abbreviation"], 
        "logo": team_info["logos"][0]["href"], 
        "schedule": []
    }


# cycle through team id map keys

for id, _ in team_id_map.items():

    string_x = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams/{id}/events"

    # print(string_x)

    # Run Schedule URL for each team
    schedule_url_list = get_request(string_x)

    # items = get_request(schedule_url_list["items"])
    # print(schedule_url_list)
    print("!!!!!!!!!!!!!!!!!!!!")
    for url in schedule_url_list["items"]:

        team_x_week_x_event = get_request(url["$ref"])

        season_type = get_request(team_x_week_x_event["seasonType"]["$ref"])

        if season_type["id"] == "2":
        
            print("boom boom pow")

            week_res = get_request(team_x_week_x_event["week"]["$ref"])
            week = week_res["number"]

            competitors = team_x_week_x_event["competitions"][0]["competitors"]

            for comp in competitors:
                print("entered")
                if comp["id"] == id:

                    home_away = comp["homeAway"]
                
                else:

                    opponent = comp["id"]

            my_dic = {
                "opponent": opponent,
                "homeAway": home_away,
                "week": week
            }
            print(my_dic)
            team_id_map[id]["schedule"].append(my_dic)
        # exit()
    # exit()

insertion = {
    "season": 2024,
    "team_schedules": team_id_map
}

mongo.deploy(insertion)
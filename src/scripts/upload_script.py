import requests
from mongo_support import MongoConnect

mongo = MongoConnect()


def get_request(url):

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
    return json_data

weeks_url = "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/types/2/weeks?lang=en&region=us"


teams_url = "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/teams?lang=en&region=us&limit=100"
teams = get_request(teams_url)


dashboard = {}

for team in teams["items"]:
    team_info = get_request(team["$ref"])
    dashboard[team_info["id"]] = {
        "name": team_info["abbreviation"], 
        "wins": 0, "losses": 0, 
        "logo": team_info["logos"][0]["href"], 
        "game_log": []
    }


weeks_data = get_request(weeks_url)

# cycle from week to week
for i, week in enumerate(weeks_data['items']):
    print(i)

    week_x = get_request(week["$ref"])
    week_x_events = get_request(week_x["events"]["$ref"])
    print(week_x_events["count"])
    
    
    # go through all team's games from each week
    for j, game in enumerate(week_x_events["items"]):
        game_x = get_request(game["$ref"])
        # if(len(game_x["competitions"])) != 0:
        #     print("LENGTH OF COMPETITIONS NOT ZERO")
        #     exit()


        line_link = game_x["competitions"][0]["odds"]["$ref"]

        main_line = ""
        over_under = 0
        odds_x = get_request(line_link)
        print("length of odds items: ", len(odds_x["items"]))
        for item in odds_x["items"]:
            if item["provider"]["name"] == "DraftKings":
                main_line = item["details"]
                over_under = int(item["overUnder"])
                break
            # print(item["provider"]["name"]) show all betting platforms

        if main_line == "":
            print("NO DRAFT KINGS BITCH")
            exit()
        if over_under == 0:
            print("over under access error")
            exit()

        # print(odds_x)
        favorite_x = main_line.split(" ")
        print(favorite_x)
        favorite_x[1] = favorite_x[1]

        game_result = {}
        # loop of 2, both teams playing in the game
        diff=0
        total=0
        total_score = []
        for item in game_x["competitions"][0]["competitors"]:

            team = dashboard[item["id"]]["name"]
            print("team:", team)

            score = get_request(item["score"]["$ref"])
            score = score["displayValue"]

            total_score.append(score)
            total += int(score)


            if team == favorite_x[0]:
                # team was favored. Just add spread
                spread = favorite_x[1]
            else:
                # team not favored, flip spread
                spread = "+" + favorite_x[1][1:]

            if item["winner"] == True:

                # currently iterating winner
                # adding game line. Future plans to add W/L spread
                dashboard[item["id"]]["wins"] += 1
                result = "W"
                winner = True

                diff += int(score)

            else:


                dashboard[item["id"]]["losses"] += 1
                result = "L"
                winner = False

                diff -= int(score)

            game_result[team] = {
                    "team_id": item["id"],
                    "winner": winner, 
                    "score": score,
                    "spread": spread,
                    "home_away": item["homeAway"],
                    "result": result,
                }



        for key, value in game_result.items():

            print(value)

            if value["spread"][0] == "-":
                if value["result"] == "W" and diff > float(value["spread"][1:]):
                    covered_spread = True
                else:
                    covered_spread = False
            else:
                if result == "L" and diff < float(value["spread"][1:]):
                    covered_spread = False
                else:
                    covered_spread = True

            if total > int(over_under):
                hit_over = True
            else:
                hit_over = False


            # have loser's score be negative
            dashboard[value["team_id"]]["game_log"].append({
                "week": i+1, 
                "teams": game_x["shortName"], 
                "result": value["result"],
                "spread": value["spread"],
                "covered_spread": covered_spread,
                "home_away": value["home_away"],
                "score": "-".join(total_score),
                "over/under": over_under,
                "hit_over": hit_over

            })



insertion = {
    "season": 2023,
    "team_stats": dashboard
}

mongo.deploy(insertion)
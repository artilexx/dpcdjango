from django.shortcuts import render
import requests
import json
from collections import defaultdict
from website.functions.player_ids import player_ids, roles
from website.functions.assign_grade import assign_grade
from dpcdjango.settings import BASE_DIR

def get_player_stats(request, player):
    player = player.lower()
    if player not in player_ids:
        if player.isnumeric() == False:
            context = {"player":player}
            return render(request, "404.html", context) #return 404page
        else:
            account_id = player
            player_role = "pos3" #default to pos3 when user enters their own ID
    else: 
        account_id = player_ids[player]
        for role in roles:
            if player in roles[role]:
                player_role = role
                break

    params = { 
        "limit": 20 #limit call to last 20 matches
    }

    try:
        winrate_call = requests.get("https://api.opendota.com/api/players/" + str(account_id) + "/wl", params = params)
        stats_call = requests.get("https://api.opendota.com/api/players/" + str(account_id) + "/recentMatches")
        print("API calls suceeded")
    except:
        print("API calls failed")

    stats_data  = json.loads(stats_call.text)
    winrate_data = json.loads(winrate_call.text)

    if stats_data == []: # user entered invalid player_id
        return render(request, "404.html", context) #return 404page

        
    player_stats = defaultdict(list) #stats to be shown on webpage

    for match in stats_data:
        player_stats["kills"].append(float(match.get("kills")))
        player_stats["deaths"].append(float(match.get("deaths")))
        player_stats["gpm"].append(float(match.get("gold_per_min")))
        player_stats["xpm"].append(float(match.get("xp_per_min")))
        player_stats["hd"].append(float(match.get("hero_damage")))
        player_stats["td"].append(float(match.get("tower_damage")))
        player_stats["lh"].append(float(match.get("last_hits")))

    for player_stat in player_stats:
        player_stats[player_stat] = sum(player_stats[player_stat])/len(player_stats[player_stat]) #create avg of each stat for displaying on website
        player_stats[player_stat] = round(player_stats[player_stat],2)
    
    player_stats["kd"] = round(player_stats["kills"]/player_stats["deaths"],2)
    player_stats["winrate"] = round((int(winrate_data.get("win"))/20)*100,2) #convert winrate from deciamal to whole number

    #calculate role averages from file containing role stats
    role_avgs = {}
    with open(f"{BASE_DIR}/website/role_stats/{player_role}_stats.json") as avg_file:
        avg_json = json.load(avg_file)
        role_avgs["kd"] = round(sum(avg_json.get("kdlist")) / len(avg_json.get("kdlist")),2)
        role_avgs["gpm"] = round(sum(avg_json.get("gpmlist")) / len(avg_json.get("gpmlist")),2)
        role_avgs["xpm"] = round(sum(avg_json.get("xpmlist")) / len(avg_json.get("xpmlist")),2)
        role_avgs["hd"] = round(sum(avg_json.get("hdlist")) / len(avg_json.get("hdlist")),2)
        role_avgs["td"] = round(sum(avg_json.get("tdlist")) / len(avg_json.get("tdlist")),2)
        role_avgs["lh"] = round(sum(avg_json.get("lhlist")) / len(avg_json.get("lhlist")),2)

    player_stats["grade"] = assign_grade(player_stats, role_avgs)

    context = {
        "player_stats": player_stats,
        "player_name": player.capitalize(),
        "role_avgs": role_avgs,
        "player_list": sorted(player_ids)
        }

    return render(request, "index.html", context)
def assign_grade(player_stats, role_stats):
    possiblegrades = ["S", "A", "B", "C", "D", "F"]
    weightings = {"kd": 0.1, "gpm": 0.1, "xpm": 0.1, "hd": 0.1, "td":0.1, "lh": 0.1, "winrate": 0.4}
    
    score = 0

    for stat in player_stats:
        if stat == "winrate" or stat == "kills" or stat == "deaths": #ignore stats that can't be compared
            continue
        score += (player_stats.get(stat)/role_stats.get(stat))*weightings.get(stat)
    score += (player_stats.get("winrate")/100)*weightings.get("winrate") #divide winrate by 100 to convert to a decimal 0.0 - 1.0

    if score > 0.95:
        grade = "S"
    elif score > 0.9:
        grade = "A"
    elif score > 0.8:
        grade = "B"
    elif score > 0.7:
        grade = "C"
    elif score > 0.6:
        grade = "D"
    else: 
        grade = "F"

    if player_stats.get("winrate") < 40 and grade != "F":
        grade = possiblegrades[possiblegrades.index(grade)+1]

    return grade
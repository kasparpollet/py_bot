import discord
import requests
import lolchampions
import math

lol_key = "key"
default_region = "euw1"

def get_player(message):
    split_msg = message.content.split(" ", 1)
    sum_name = split_msg[1].replace(" ", "%20")
    if(split_msg[0] != ".lolacc"):
        try:
            region = split_msg[0].split("acc")[1]
        except IndexError:
            region = default_region
        if region == "euw": region = default_region
        elif (region == "eun" or region == "eun1"): region = "eun1"
        elif (region == "br" or region == "br1"): region = "br1"
        elif (region == "jp" or region == "jp1"): region = "jp1"
        elif (region == "la" or region == "la1"): region = "la1"
        elif (region == "na" or region == "na1"): region = "na1"
        elif (region == "oc" or region == "oc1"): region = "oc1"
        elif (region == "tr" or region == "tr1"): region = "tr1"
        elif (region == "kr"): region = "kr"
        elif (region == "ru"): region = "ru"
        else: region = default_region
    else: region = default_region

    player = requests.get('https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + sum_name + '?api_key=' + lol_key)

    if (player.status_code == 200):
        player = player.json()
        summonerlevel = player["summonerLevel"]
        name = player["name"]
        id = player["id"]
        account_id = player["accountId"]

        print(id)

        mastery_points = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/" + id + '?api_key=' + lol_key)
        mastery_points = mastery_points.json()

        mastery = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + id + '?api_key=' + lol_key)
        mastery = mastery.json()
        champion1_name = lolchampions.get_champion_by_id(mastery[0]["championId"])
        champion1_level = mastery[0]["championLevel"]
        champion1_points = mastery[0]["championPoints"]

        embed = discord.Embed(title=f"{name} Level {summonerlevel} ({region})",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )
        embed.add_field(name="Total Masterypoints", value=f"{mastery_points}", inline=False)
        embed.add_field(name="Main Champion", value=f"{champion1_name} Level {champion1_level} with {champion1_points} Points", inline=False)

        current_game = requests.get("https://" + region + ".api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + id + '?api_key=' + lol_key)

        if (current_game.status_code == 200):
            current_game = current_game.json()

            i = -1
            while True:
                i = i + 1
                player_id = current_game["participants"][i]["summonerId"]
                if(player_id == id):
                    break

            champion_playing = lolchampions.get_champion_by_id(current_game["participants"][i]["championId"])
            game_mode = current_game["gameMode"]
            game_type = current_game["gameType"]
            game_start_time = current_game["gameStartTime"]

            embed.add_field(name="Current game", value=f"{champion_playing} in {game_mode} (.lollive{region} {name})", inline=False)
        else:
            last_game = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id + '?api_key=' + lol_key)

            if(last_game.status_code == 200):
                last_game = last_game.json()
                last_game = last_game["matches"][0]
                game_id = last_game["gameId"]
                champion_id = last_game["champion"]
                champion = lolchampions.get_champion_by_id(last_game["champion"])
                rol = last_game["role"]
                lane = last_game["lane"]

                match = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(game_id) + '?api_key=' + lol_key)
                match = match.json()
                game_mode = match["gameMode"]

                i = -1
                while True:
                    i = i + 1
                    champion_id2 = match["participants"][i]["championId"]
                    if (champion_id2 == champion_id):
                        break

                team_id = match["participants"][i]["teamId"]
                if(team_id == 100): x = 0
                else: x = 1
                win_lose = match["teams"][x]["win"]
                if(win_lose == "Win"): win_lose = "Won"
                else: win_lose = "Lost"

                embed.add_field(name="Last game", value=f"{win_lose} as {champion} in {lane}", inline=False)

            else:
                embed.add_field(name="Games", value=f"Has never played", inline=False)

        embed.set_thumbnail(url="https://e7.pngegg.com/pngimages/832/281/png-clipart-blue-and-yellow-l-logo-league-of-legends-computer-icons-garena-video-game-legends-blue-logo.png")
        embed.set_footer(text=f"Requested by {message.author.name}")

        return embed

    else: return discord.Embed(title="Could not find player")

def get_match(message):
    split_msg = message.content.split(" ", 1)
    sum_name = split_msg[1].replace(" ", "%20")

    if(split_msg[0] != ".lollive"):
        try:
            region = split_msg[0].split("acc")[1]
        except IndexError:
            region = default_region
        if (region == "euw"): region = default_region
        elif (region == "eun" or region == "eun1"): region = "eun1"
        elif (region == "br" or region == "br1"): region = "br1"
        elif (region == "jp" or region == "jp1"): region = "jp1"
        elif (region == "la" or region == "la1"): region = "la1"
        elif (region == "na" or region == "na1"): region = "na1"
        elif (region == "oc" or region == "oc1"): region = "oc1"
        elif (region == "tr" or region == "tr1"): region = "tr1"
        elif (region == "kr"): region = "kr"
        elif (region == "ru"): region = "ru"
        else: region = default_region
    else: region = default_region

    player = requests.get('https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + sum_name + '?api_key=' + lol_key)

    if (player.status_code == 200):
        player = player.json()
        id = player["id"]
        name = player["name"]

        current_game = requests.get("https://" + region + ".api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + id + '?api_key=' + lol_key)

        if (current_game.status_code == 200):
            current_game = current_game.json()
            game_mode = current_game["gameMode"]
            game_type = current_game["gameType"]
            game_length_min = math.floor(current_game["gameLength"] / 60)
            game_length_sec = current_game["gameLength"] % 60

            embed = discord.Embed(title=f"{game_mode} {game_length_min}:{game_length_sec}",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )

            for x in range(5):
                name = current_game["participants"][x]["summonerName"]
                champion = lolchampions.get_champion_by_id(current_game["participants"][x]["championId"])
                embed.add_field(name=f"{name}", value=f"Playing as {champion}", inline=False)

            embed.add_field(name=f"VS", value=f"**--------------**", inline=False)

            for x in range(5, 10):
                name = current_game["participants"][x]["summonerName"]
                champion = lolchampions.get_champion_by_id(current_game["participants"][x]["championId"])
                embed.add_field(name=f"{name}", value=f"Playing as {champion}", inline=False)

            embed.set_thumbnail(
                url="https://e7.pngegg.com/pngimages/832/281/png-clipart-blue-and-yellow-l-logo-league-of-legends-computer-icons-garena-video-game-legends-blue-logo.png")
            embed.set_footer(text=f"Requested by {message.author.name}")

            return embed

        else: return discord.Embed(title=f"{name} is not playing right now")

    else: return discord.Embed(title="Could not find player")

def get_top(message):
    split_msg = message.content.split(" ", 1)
    sum_name = split_msg[1].replace(" ", "%20")
    top_number = 25

    if(split_msg[0] != ".loltop"):
        try:
            region = split_msg[0].split("top")[1]
        except IndexError:
            region = default_region
        if (region == "euw"): region = default_region
        elif (region == "eun" or region == "eun1"): region = "eun1"
        elif (region == "br" or region == "br1"): region = "br1"
        elif (region == "jp" or region == "jp1"): region = "jp1"
        elif (region == "la" or region == "la1"): region = "la1"
        elif (region == "na" or region == "na1"): region = "na1"
        elif (region == "oc" or region == "oc1"): region = "oc1"
        elif (region == "tr" or region == "tr1"): region = "tr1"
        elif (region == "kr"): region = "kr"
        elif (region == "ru"): region = "ru"
        else: region = default_region
    else: region = default_region

    # try:
    #     top_number = int(split_msg[0].split("p")[1])
    # except:
    #     return discord.Embed(title=f"Invalid number")
    #
    # if(top_number > 25): top_number = 25

    player = requests.get('https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + sum_name + '?api_key=' + lol_key)

    if (player.status_code == 200):
        player = player.json()
        id = player["id"]
        name = player["name"]

        mastery = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + id + '?api_key=' + lol_key)
        mastery = mastery.json()
        
        embed = discord.Embed(title=f"Top {top_number} Champions From {name} ({region})",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )

        for x in range (top_number):
            champion_name = lolchampions.get_champion_by_id(mastery[x]["championId"])
            champion_level = mastery[x]["championLevel"]
            champion_points = mastery[x]["championPoints"]
            embed.add_field(name=f"{x + 1}-{champion_name}", value=f"Lvl: {champion_level} Points: {champion_points}", inline=True)

        embed.set_footer(text=f"Requested by {message.author.name}")

        return embed
    
    else: return discord.Embed(title="Could not find player")

def get_last_games(message):
    split_msg = message.content.split(" ", 1)
    sum_name = split_msg[1].replace(" ", "%20")
    amount_games = 25

    if(split_msg[0] != ".lolgames"):
        try:
            region = split_msg[0].split("games")[1]
        except IndexError:
            region = default_region
        if (region == "euw"): region = default_region
        elif (region == "eun" or region == "eun1"): region = "eun1"
        elif (region == "br" or region == "br1"): region = "br1"
        elif (region == "jp" or region == "jp1"): region = "jp1"
        elif (region == "la" or region == "la1"): region = "la1"
        elif (region == "na" or region == "na1"): region = "na1"
        elif (region == "oc" or region == "oc1"): region = "oc1"
        elif (region == "tr" or region == "tr1"): region = "tr1"
        elif (region == "kr"): region = "kr"
        elif (region == "ru"): region = "ru"
        else: region = default_region
    else: region = default_region

    if(region == "kr"): amount_games = 9

    player = requests.get('https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + sum_name + '?api_key=' + lol_key)

    if (player.status_code == 200):
        player = player.json()
        id = player["id"]
        name = player["name"]
        account_id = player["accountId"]

        embed = discord.Embed(title=f"Last {amount_games} Games From {name} ({region})",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )

        games = requests.get(
            "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id + '?api_key=' + lol_key)

        win_count = 0
        lose_count = 0
        if (games.status_code == 200):
            games = games.json()
            games = games["matches"]

            for x in range(amount_games):
                game_id = games[x]["gameId"]
                champion_id = games[x]["champion"]
                champion = lolchampions.get_champion_by_id(games[x]["champion"])
                rol = games[x]["role"]
                lane = games[x]["lane"]
                if lane == "BOTTOM": lane = "Bot"
                if lane == "TOP": lane = "Top"
                if lane == "JUNGLE": lane = "Jgl"
                if lane == "MID": lane = "Mid"
                if lane == "NONE": lane = ""

                match = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(game_id) + '?api_key=' + lol_key)
                match = match.json()
                game_mode = match["gameMode"]

                i = -1
                while True:
                    i = i + 1
                    champion_id2 = match["participants"][i]["championId"]
                    if (champion_id2 == champion_id):
                        break

                kills = match["participants"][i]["stats"]["kills"]
                deaths = match["participants"][i]["stats"]["deaths"]
                assists = match["participants"][i]["stats"]["assists"]
                kda = str(kills) + "/" + str(deaths) + "/" + str(assists)
                team_id = match["participants"][i]["teamId"]
                if(team_id == 100): y = 0
                else: y = 1
                win_lose = match["teams"][y]["win"]
                if(win_lose == "Win"):
                    win_lose = "Won"
                    win_count = win_count + 1
                else:
                    win_lose = "Lost"
                    lose_count = lose_count + 1

                embed.add_field(name=f"{x + 1}-{win_lose} in {game_mode}", value=f"{champion} {lane} ({kda})", inline=True)

            embed.set_footer(text=f"{win_count} Wins / {lose_count} Loses")

            return embed

        else: embed.add_field(name="Games", value=f"Has never played", inline=False)

    else: return discord.Embed(title="Could not find player")




import discord
import requests

key = "key"
headers = {"TRN-Api-Key": key}


def get_player(message):
    split_msg = message.content.split(" ", 1)
    name = split_msg[1].replace(" ", "%20")

    data = requests.get("https://public-api.tracker.gg/v2/csgo/standard/profile/steam/" + name, headers=headers)

    data = data.json()

    try:
        avatar = data["data"]["platformInfo"]["avatarUrl"]
        user_name = data["data"]["platformInfo"]["platformUserHandle"]
        stats = data["data"]["segments"][0]["stats"]
        time_played = stats["timePlayed"]["displayValue"]
        kills = stats["kills"]["displayValue"]
        deaths = stats["deaths"]["displayValue"]
        kd = stats["kd"]["displayValue"]
        headshots = stats["headshots"]["displayValue"]
        accuracy = stats["shotsAccuracy"]["displayValue"]
        bombs_planted = stats["bombsPlanted"]["displayValue"]
        bombs_defused = stats["bombsDefused"]["displayValue"]
        money_earned = stats["moneyEarned"]["displayValue"]
        mvp = stats["mvp"]["displayValue"]
        matches_played = stats["matchesPlayed"]["displayValue"]
        wins = stats["wins"]["displayValue"]
        losses = stats["losses"]["displayValue"]
        win_percentage = stats["wlPercentage"]["displayValue"]
        headshot_percentage = stats["headshotPct"]["displayValue"]
        rank = stats["wins"]["rank"]
        if rank == "null": rank = "None"

        embed = discord.Embed(title=f"CS:GO {user_name} Rank: {rank}",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Games", value=f"{matches_played}")
        embed.add_field(name="Wins", value=f"{wins}")
        embed.add_field(name="Losses", value=f"{losses}")
        embed.add_field(name="Win rate", value=f"{win_percentage}")
        embed.add_field(name="MVP's", value=f"{mvp}")
        embed.add_field(name="Money earned", value=f"{money_earned}")
        embed.add_field(name="Kills", value=f"{kills}")
        embed.add_field(name="Deaths", value=f"{deaths}")
        embed.add_field(name="K/D", value=f"{kd}")
        embed.add_field(name="Accuracy", value=f"{accuracy}")
        embed.add_field(name="Headshots", value=f"{headshots}")
        embed.add_field(name="Headshots rate", value=f"{headshot_percentage}")
        embed.add_field(name="Bombs planted", value=f"{bombs_planted}")
        embed.add_field(name="Bombs defused", value=f"{bombs_defused}")
        embed.add_field(name="Time played", value=f"{time_played}")

        embed.set_footer(text=f"Requested by {message.author.name}")

        return embed

    except: return discord.Embed(title="The player either hasn't played CSGO or their profile is private", headers=headers)

def search_player(message):
    split_msg = message.content.split(" ", 1)
    name = split_msg[1].replace(" ", "%20")

    data = requests.get("https://public-api.tracker.gg/v2/csgo/standard/search?platform=steam&query=" + name, headers=headers)
    data = data.json()

    try:
        avatar = data["data"][-1]["avatarUrl"]
        user_name = data["data"][-1]["platformUserHandle"]
        id = data["data"][-1]["platformUserId"]

        embed = discord.Embed(title=f"Found Player {user_name}",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Id", value=f"{id}")
        embed.set_footer(text=f"Requested by {message.author.name}")

        return embed

    except: return discord.Embed(title="Can not find any player")

def get_weapons(message):
    split_msg = message.content.split(" ", 2)
    name = split_msg[2].replace(" ", "%20")
    weapon_name = split_msg[1]

    number_of_weapons = 30

    data = requests.get("https://public-api.tracker.gg/v2/csgo/standard/profile/steam/" + name + "/segments/weapon", headers=headers)

    data = data.json()

    for x in range(number_of_weapons):
        try:
            weapon = data["data"][x]["attributes"]["key"]
            if(weapon == weapon_name):
                weapon = data["data"][x]["metadata"]["name"]
                avatar = data["data"][x]["metadata"]["imageUrl"]
                stats = data["data"][x]["stats"]
                kills = stats["kills"]["displayValue"]
                shots_fired = stats["shotsFired"]["displayValue"]
                shots_hit = stats["shotsHit"]["displayValue"]
                shots_accuracy = stats["shotsAccuracy"]["displayValue"]

                embed = discord.Embed(title=f"{weapon} Stats of {name}",
                                      color=message.guild.me.top_role.color,
                                      timestamp=message.created_at, )
                embed.set_thumbnail(url=avatar)
                embed.add_field(name="Kills", value=f"{kills}")
                embed.add_field(name="Shots fired / Hit", value=f"{shots_fired} / {shots_hit}")
                embed.add_field(name="Shot accuracy", value=f"{shots_accuracy}%")
                embed.set_footer(text=f"Requested by {message.author.name}")

                return embed

        except: return discord.Embed(title="Can not find player or weapon")
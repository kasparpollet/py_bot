import discord
import requests

key = "key"

def get_player(message):
    split_msg = message.content.split(" ", 1)
    name = split_msg[1].replace(" ", "%20")
    
    try:
        id_data = requests.get("https://api.brawlhalla.com/search?steamid=" + name + "&api_key=" + key)
        id = id_data.json()["brawlhalla_id"]
    except: return discord.Embed(title="Can not find player")

    data = requests.get("https://api.brawlhalla.com/player/" + str(id) + "/stats?api_key=" + key)
    ranked_data = requests.get("https://api.brawlhalla.com/player/" + str(id) + "/ranked?api_key=" + key)

    data = data.json()
    ranked_data = ranked_data.json()

    user_name = data["name"]
    level = data["level"]
    games = data["games"]
    wins = data["wins"]

    embed = discord.Embed(title=f"Brawlhalla {user_name}",
                          color=message.guild.me.top_role.color,
                          timestamp=message.created_at, )
    embed.add_field(name="Level", value=f"{level}")
    embed.add_field(name="Games", value=f"{games}")
    embed.add_field(name="Wins", value=f"{wins}")

    try:
        rank = ranked_data["tier"]
        ranked_games = ranked_data["games"]
        ranked_wins = ranked_data["wins"]
        embed.add_field(name="Rank", value=f"{rank}")
        embed.add_field(name="Ranked games", value=f"{ranked_games}")
        embed.add_field(name="Ranked wins", value=f"{ranked_wins}")
    except:
        embed.add_field(name="Ranked games", value=f"Never played ranked")

    embed.set_footer(text=f"Requested by {message.author.name}")

    return embed
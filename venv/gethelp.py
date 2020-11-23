import discord

def get_help(message):
    embed = discord.Embed(title=f"Help",
                          color=message.guild.me.top_role.color,
                          timestamp=message.created_at, )
    embed.add_field(name=".ping", value=f"Test the bot", inline=False)
    embed.add_field(name=".pils", value=f"Get beer prices in the AH", inline=False)
    embed.add_field(name=".weather + city", value=f"Get the weather in any city", inline=False)
    embed.add_field(name=".coinflip", value=f"Do a coinflip", inline=False)
    embed.add_field(name=".lolacc+region + summoner name", value=f"Get someones acc (no region = euw)", inline=False)
    embed.add_field(name=".lollive+region + summoner name", value=f"Get someones live game (no region = euw)", inline=False)
    embed.add_field(name=".loltop+region + summoner name", value=f"Get someones top 25 champions (no region = euw)", inline=False)
    embed.add_field(name=".lolgames+region + summoner name", value=f"Get someones last 25 played games (no region = euw)", inline=False)
    embed.add_field(name=".csgo + name or id", value=f"Get somones csgo stats", inline=False)
    embed.add_field(name=".csgoweapon + weapon name + name or id", value=f"Get somones csgo weapon stats", inline=False)
    embed.add_field(name=".brawl + id", value=f"Get somones brawlhalla stats", inline=False)
    embed.add_field(name=".steam + name or id", value=f"Get somones steam id", inline=False)
    embed.set_footer(text=f"Requested by {message.author.name}")

    return embed
import discord
import weather
import lol
import random
import jokes
import gethelp
import csgo
import brawlhalla
import pils

TOKEN = 'bot_token'
client = discord.Client()
prefix = '.'

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "wat" or message.content == "wat?":
        await message.channel.send("patat")
    
    if message.content == "waarbij" or message.content == "waarbij?":
        await message.channel.send("aardbei")

    if message.content == "5 euro" or message.content == "vijf euro":
        await message.channel.send("5 euro? op je muil gauw!")

    if message.content == prefix + "help":
        msg = gethelp.get_help(message)
        await message.channel.send(embed=msg)

    if message.content == prefix + "ping":
        msg = "pong {0.author.mention}".format(message)
        await message.channel.send(msg)

    if message.content == prefix + "pils":
        msg = pils.get_pils(message)
        await message.channel.send(embed=msg)

    if message.content == prefix + "coinflip":
        msg = coinflip()
        await message.channel.send(msg)

    if message.content.startswith(prefix + "weather"):
        msg = weather.weather_of_city(message, message.content.split(" ")[1])
        await message.channel.send(embed=msg)

    if message.content.startswith(prefix + "lolacc"):
        msg = lol.get_player(message)
        await message.channel.send(embed=msg)
        
    if message.content.startswith(prefix + "lollive"):
        msg = lol.get_match(message)
        await message.channel.send(embed=msg)
        
    if message.content.startswith(prefix + "loltop"):
        msg = lol.get_top(message)
        await message.channel.send(embed=msg)
        
    if message.content.startswith(prefix + "lolgames"):
        msg = lol.get_last_games(message)
        await message.channel.send(embed=msg)
        
    if message.content.startswith(prefix + "csgo "):
        msg = csgo.get_player(message)
        await message.channel.send(embed=msg)        
        
    if message.content.startswith(prefix + "steam"):
        msg = csgo.search_player(message)
        await message.channel.send(embed=msg)     
        
    if message.content.startswith(prefix + "csgoweapon"):
        msg = csgo.get_weapons(message)
        await message.channel.send(embed=msg)

    if message.content.startswith(prefix + "brawl"):
        msg = brawlhalla.get_player(message)
        await message.channel.send(embed=msg)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def coinflip():
    r = random.randrange(2)
    if r == 0:
        return "Head"
    else:
        return "Tails"

client.run(TOKEN)
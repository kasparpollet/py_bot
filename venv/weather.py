import discord
import requests

weather_api = "key"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def weather_of_city(message, city: str):
    city_name = city
    complete_url = base_url + "appid=" + weather_api + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    channel = message.channel

    if data["cod"] != "404":
        x = data["main"]
        current_temperature_celsiuis = str(round(x["temp"] - 273.15))
        feels_like_temperature_celsiuis = str(round(x["feels_like"] - 273.15))
        current_humidity = x["humidity"]
        description = data["weather"]
        weather_description = description[0]["description"]

        embed = discord.Embed(title=f"Weather in {city_name}",
                              color=message.guild.me.top_role.color,
                              timestamp=message.created_at, )
        embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
        embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
        embed.add_field(name="Feels Like(C)", value=f"**{feels_like_temperature_celsiuis}°C**", inline=False)
        embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"Requested by {message.author.name}")

        return embed
    else:
        return discord.Embed(title="City not found")
# coding=utf-8
import discord
from bs4 import BeautifulSoup
import requests


hertogjan_url = "https://www.ah.nl/producten/product/wi2708/hertog-jan-pilsener-natuurzuiver-bier-24-x-30-cl"
heineken_url = "https://www.ah.nl/producten/product/wi210145/heineken-premium-pilsener-krat"
grolsch_url = "https://www.ah.nl/producten/product/wi232949/grolsch-premium-pilsner-krat"
brand_url = "https://www.ah.nl/producten/product/wi227163/brand-pilsener-krat"
amstel_url = "https://www.ah.nl/producten/product/wi2722/amstel-pilsener-krat"
jupiler_url = "https://www.ah.nl/producten/product/wi113050/jupiler-pilsener"
warsteiner_url = "https://www.ah.nl/producten/product/wi126867/warsteiner-pilsener"
pils = [hertogjan_url, heineken_url, grolsch_url, brand_url, amstel_url, jupiler_url, warsteiner_url]


def get_pils(message):
    embed = discord.Embed(title=f"Kratje pils in de Appie!",
                          color=message.guild.me.top_role.color,
                          timestamp=message.created_at, )

    for beers in pils:

        beer = requests.get(beers)
        soup = BeautifulSoup(beer.content, 'html.parser')

        ints = soup.find_all(class_="price-amount_integer__N3JDd")
        commas = soup.find_all(class_="price-amount_fractional__3sfJy")

        try:
            price_int = ints[1].get_text()
            price_comma = commas[1].get_text()
            bonus = "Bonus!"
        except:
            #no bonus
            price_int = ints[0].get_text()
            price_comma = commas[0].get_text()
            bonus = ""
        finally:
            name = soup.find("span", class_="line-clamp line-clamp--active").get_text()
            name = " ".join(name.split(" ")[:2])

            embed.add_field(name=f"{name}", value=f"€{price_int}.{price_comma} {bonus}")

    embed.set_footer(text=f"Requested by {message.author.name}")

    return embed
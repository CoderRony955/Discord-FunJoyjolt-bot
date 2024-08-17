import discord
from discord.ext import commands
import requests

def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} - {data['punchline']}"
    return "Couldn't fetch a joke at the moment. Please try again later."

class JokeView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Regenerate Joke", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        joke = get_joke()
        embed = discord.Embed(title="Here's a joke for you! 😂", description=joke, color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=self)

def register_jokes_commands(bot):

    @bot.command(name='joke')
    async def tell_joke(ctx):
        joke = get_joke()
        embed = discord.Embed(title="Here's a joke for you! 😂", description=joke, color=0x00ff00)
        await ctx.send(embed=embed, view=JokeView())

    @bot.command(name='tell_me_a_joke')
    async def tell_me_a_joke(ctx):
        joke = get_joke()
        embed = discord.Embed(title="Sure, here's a joke for you! 😂", description=joke, color=0x00ff00)
        await ctx.send(embed=embed, view=JokeView())

    @bot.command(name='joke_of_the_day')
    async def joke_of_the_day(ctx):
        joke = get_joke()
        embed = discord.Embed(title="Joke of the Day 📅", description=joke, color=0x00ff00)
        await ctx.send(embed=embed, view=JokeView())

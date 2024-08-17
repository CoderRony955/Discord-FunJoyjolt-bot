import discord
from discord.ext import commands
import requests

def get_motivation():
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        data = response.json()
        return f"{data[0]['q']} - {data[0]['a']}"
    return "Couldn't fetch a motivational quote at the moment. Please try again later."

class MotivationView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Regenerate Motivation", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        motivation = get_motivation()
        embed = discord.Embed(title="Motivation 💪", description=motivation, color=0xf1c40f)
        await interaction.response.edit_message(embed=embed, view=self)

def register_motivation_commands(bot):

    @bot.command(name='motivation')
    async def motivation_about(ctx):
        motivation = get_motivation()
        embed = discord.Embed(title="Motivation 💪", description=motivation, color=0xf1c40f)
        await ctx.send(embed=embed, view=MotivationView())

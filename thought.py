import discord
from discord.ext import commands
import random
import json
import os

# Load thoughts from JSON file or use default thoughts
current_dir = os.path.dirname(os.path.abspath(__file__))
thoughts_file_path = os.path.join(current_dir, 'thoughts.json')

try:
    with open(thoughts_file_path, 'r') as file:
        thoughts = json.load(file)
except FileNotFoundError:
    thoughts = [
        "Believe you can and you're halfway there.",
        "Act as if what you do makes a difference. It does.",
        "Success is not how high you have climbed, but how you make a positive difference to the world.",
        "You make a life out of what you have, not what you're missing.",
        "We generate fears while we sit. We overcome them by action."
    ]
 
class ThoughtView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Regenerate Thought", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        thought = random.choice(thoughts)
        embed = discord.Embed(title="Thoughts 💭", description=thought, color=0x3498db)
        await interaction.response.edit_message(embed=embed, view=self)

def register_thoughts_commands(bot):

    @bot.command(name='thought')
    async def thought_about(ctx, *, topic):
        thought = random.choice(thoughts)
        embed = discord.Embed(title="Thoughts 💭", description=thought, color=0x3498db)
        await ctx.send(embed=embed, view=ThoughtView())

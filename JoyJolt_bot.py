import discord
from discord.ext import commands 
import os

intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content

bot = commands.Bot(command_prefix='/', intents=intents) #<------------------bot prefix

# Import and register commands from commands.py 
from commands import register_commands
register_commands(bot)

bot.run('BOT-TOKEN')

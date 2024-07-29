import discord
from discord.ext import commands
import requests
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content

bot = commands.Bot(command_prefix='/', intents=intents) #<------------------bot prefix

#-----------------------------------------------
# Determine the path to the JSON file
#-----------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
thoughts_file_path = os.path.join(current_dir, 'thoughts.json')

# Read thoughts from JSON file
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
    
#------------------------------------------------------
# Using a random API for getting jokes and motivations
#------------------------------------------------------
def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} - {data['punchline']}"
    return "Couldn't fetch a joke at the moment. Please try again later."

def get_topic_joke(topic):
    response = requests.get(f"https://v2.jokeapi.dev/joke/Any?contains={topic}")
    if response.status_code == 200:
        data = response.json()
        if data.get('error'):
            return "Couldn't fetch a joke on that topic. Please try again later."
        if data['type'] == "single":
            return data['joke']
        elif data['type'] == "twopart":
            return f"{data['setup']} - {data['delivery']}"
    return "Couldn't fetch a joke on that topic. Please try again later."

def get_motivation():
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        data = response.json()
        return f"{data[0]['q']} - {data[0]['a']}"
    return "Couldn't fetch a motivational quote at the moment. Please try again later."

class JokeView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Regenerate Joke", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        joke = get_joke()
        embed = discord.Embed(title="Here's a joke for you! 😂", description=joke, color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=self)

class ThoughtView(discord.ui.View):
    def __init__(self, topic):
        super().__init__()
        self.topic = topic

    @discord.ui.button(label="Regenerate Thought", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        thought = random.choice(thoughts)
        embed = discord.Embed(title="Thoughts 💭", description=thought, color=0x3498db)
        await interaction.response.edit_message(embed=embed, view=self)

class MotivationView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Regenerate Motivation", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        motivation = get_motivation()
        embed = discord.Embed(title="Motivation 💪", description=motivation, color=0xf1c40f)
        await interaction.response.edit_message(embed=embed, view=self)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over jokes"))
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        await message.channel.send(f"Hello {message.author.mention}! Try `%myhelp` for commands.")

    await bot.process_commands(message)

@bot.command(name='yo')
async def yo(ctx):
    embed = discord.Embed(title="Yo!👋🏻", color=0xffffff)
    await ctx.send(embed=embed)

@bot.command(name='joke')
async def tell_joke(ctx):
    joke = get_joke()
    embed = discord.Embed(title="Here's a joke for you! 😂", description=joke, color=0x00ff00)
    await ctx.send(embed=embed, view=JokeView())

@bot.command(name='tell_me_a_joke')
async def tell_me_a_joke(ctx):
    joke = get_joke()
    embed = discord.Embed(title="Sure here's a joke for you! 😂", description=joke, color=0x00ff00)
    await ctx.send(embed=embed, view=JokeView())

@bot.command(name='joke_of_the_day')
async def joke_of_the_day(ctx):
    joke = get_joke()
    embed = discord.Embed(title="Joke of the Day 📅", description=joke, color=0x00ff00)
    await ctx.send(embed=embed, view=JokeView())

@bot.command(name='thought')
async def thought_about(ctx, *, topic):
    thought = random.choice(thoughts)
    embed = discord.Embed(title="Thoughts 💭", description=thought, color=0x3498db)
    await ctx.send(embed=embed, view=ThoughtView(topic))

@bot.command(name='motivation')
async def motivation_about(ctx):
    motivation = get_motivation()
    embed = discord.Embed(title="Motivation 💪", description=motivation, color=0xf1c40f)
    await ctx.send(embed=embed, view=MotivationView())

@bot.command(name='myhelp')
async def help_command(ctx):
    help_message = """
    Meet JoyJolt - Your Ultimate Source of Humor and Inspiration!

JoyJolt is a lively and engaging bot designed to bring joy and motivation to your Discord server. Whether you're looking for a good laugh or a dose of inspiration, JoyJolt is here to brighten your day with a wide array of jokes and motivational quotes. With its user-friendly commands, JoyJolt makes it easy to inject some fun and positivity into your conversations.
**Here are the commands you can use:**
    
    `%joke or %tell_me_a_joke` - Feeling down or just in need of a good laugh? Use these commands to get a 
    random joke that will surely put a smile on your face..
    
    `%joke_of_the_day` - Start your day with a fresh joke. JoyJolt delivers a special 
    
    joke every day to keep the laughter rolling..
    
    `%thought [topic]` - Tells a thought about the specified topic.
    
    `%motivation` - Need a little boost? JoyJolt provides motivational quotes tailored to your query, helping you stay inspired and focused..
    
    `%myhelp` - Displays a beautifully formatted list of all commands, making it easy for users to explore and utilize JoyJolt's features..
    
    `%yo` - Says hello.
     
    **Why Invite JoyJolt?
JoyJolt is more than just a bot; it's your companion for a happier, more motivated life. By adding JoyJolt to your server, you create an environment filled with laughter and positive energy. Whether you're managing a community, a group of friends, or a professional team, JoyJolt's unique blend of humor and motivation can enhance the overall atmosphere, making interactions more enjoyable and uplifting.

Join the Fun!
Invite JoyJolt to your server today and experience the magic of humor and inspiration. With JoyJolt, every day is a chance to laugh a little more and find motivation in unexpected places.**


    """
    embed = discord.Embed(title="Help Commands 🆘", description=help_message, color=0x9b59b6)
    await ctx.send(embed=embed)

@bot.command(name='jokeinfo')
async def jokeinfo(ctx):
    jokeinfo_message = "The `%joke` command tells a random joke."
    embed = discord.Embed(title="Joke Command Info ℹ️", description=jokeinfo_message, color=0x3498db)
    await ctx.send(embed=embed)

@bot.command(name='joke_on_info')
async def joke_on_info(ctx):
    joke_on_info_message = "The `%tell_me_a_joke` command tells a random joke."
    embed = discord.Embed(title="Tell Me A Joke Command Info ℹ️", description=joke_on_info_message, color=0x3498db)
    await ctx.send(embed=embed)

@bot.command(name='joke_of_the_day_info')
async def joke_of_the_day_info(ctx):
    joke_of_the_day_info_message = "The `%joke_of_the_day` command tells the joke of the day."
    embed = discord.Embed(title="Joke of the Day Command Info ℹ️", description=joke_of_the_day_info_message, color=0x3498db)
    await ctx.send(embed=embed)

@bot.command(name='thoughtinfo')
async def thoughtinfo(ctx):
    thoughtinfo_message = "The `%thought [topic]` command tells a thought about the specified topic."
    embed = discord.Embed(title="Thought Command Info ℹ️", description=thoughtinfo_message, color=0x3498db)
    await ctx.send(embed=embed)

@bot.command(name='motivationinfo')
async def motivationinfo(ctx):
    motivationinfo_message = "The `%motivation` command tells a motivational quote."
    embed = discord.Embed(title="Motivation Command Info ℹ️", description=motivationinfo_message, color=0x3498db)
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    embed = discord.Embed(title="Pong! 🏓", color=0x3498db)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # await ctx.send("Sorry, I don't recognize that command. Try `/myhelp` for commands.")
        embed = discord.Embed(title="Sorry, I don't recognize that command. Try `/myhelp` for my commands.", color=0xed0000)
        await ctx.send(embed=embed)

bot.run('BOT_TOKEN')

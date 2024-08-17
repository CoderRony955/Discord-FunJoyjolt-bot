import discord


def register_commands(bot):
    from jokes import register_jokes_commands
    from motivation import register_motivation_commands
    from thought import register_thoughts_commands

    register_jokes_commands(bot)
    register_motivation_commands(bot)
    register_thoughts_commands(bot)

    @bot.command(name='yo')
    async def yo(ctx):
        embed = discord.Embed(title="Yo!👋🏻", color=0xffffff)
        await ctx.send(embed=embed)

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
        embed = discord.Embed(
            title="Help", description=help_message, color=0x00ff00)
        await ctx.send(embed=embed)

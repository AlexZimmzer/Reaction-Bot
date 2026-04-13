from arrow import now
import discord
from discord.ext import commands
import json
import os
import asyncio
from datetime import datetime, timedelta

# Token for bot connection
TOKEN = os.getenv("DISCORD_TOKEN")

heartList = ["❤️", "🤎", "🧡", "💛", "💚", "💙", "🩵", "💜",
             "🩷", "🖤", "🩶", "🤍", "❣️", "💕", "💞", "💓",
             "💗", "💖", "💘", "💝", "💟", "❤️‍🔥", "♥️", "🫀"]

# Permissions
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)


# SCORES #
# Total Scores
def load_scores():
    if not os.path.exists("scores.json"):
        return{}
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error decoding scores.json. Starting with an empty score dictionary.")
        return {}
    return {}

scores = load_scores()

def save_scores():
    with open("scores.json", "w") as f:
        json.dump(scores, f)

# Weekly Scores
def load_weekly_scores():
    if not os.path.exists("weekly_scores.json"):
        return {}
    try:
        with open("weekly_scores.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error decoding weekly_scores.json. Starting with an empty score dictionary.")
        return {}
    return {}

weekly_scores = load_weekly_scores()

def save_weekly_scores():
    with open("weekly_scores.json", "w") as f:
        json.dump(weekly_scores, f)


# Event listener for heart reactions
@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) not in heartList or user.bot:
        return
    author = reaction.message.author
    if user.id == author.id or author.bot:
        return
    user_id = str(author.id)
    scores[user_id] = scores.get(user_id, 0) + 1
    weekly_scores[user_id] = weekly_scores.get(user_id, 0) + 1
    save_scores()
    save_weekly_scores()

# Score command to display user's score
@bot.command()
async def score(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    user_id = str(user.id)
    count = scores.get(user_id, 0)
    await ctx.send(f"```{user.name}'s ❤️ score: {count}```")

# Leaderboard command to display top 5 users
@bot.command()
async def leaderboard(ctx):
    if not scores:
        await ctx.send("``No scores yet.``")
        return
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    msg = "# Leaderboard:\n\n"

    for i, (user_id, score) in enumerate(sorted_scores[:5], start=1):
        user = await bot.fetch_user(int(user_id))
        msg += f"```{i}. {user.name} - {score} ❤️\n```"
    await ctx.send(msg)

# Debug command. I just wanted to test if i could get the server and channel name in a command, and it works!
@bot.command()
async def idk(ctx):
    await ctx.send(f"i think the server name is {ctx.guild.name} and the channel name is {ctx.channel.name} :3")

# Scan previous messages for heart reactions and update scores (backfill)!
# this one was really annyoing 
@bot.command()
async def backfill(ctx):
    scores.clear()
    save_scores()
    await ctx.send("```Starting backfill... this might take me a while...```")

    for channel in ctx.guild.text_channels:
        await ctx.send(f"```Scanning #{channel.name} :3```")
        try:
            async for message in channel.history(limit=1000):

                for reaction in message.reactions:
                    if str(reaction.emoji) not in heartList:
                        continue
                    if message.author.bot:
                        continue
                    if message.author.id == bot.user.id:
                       continue

                    user_id = str(message.author.id)
                    scores[user_id] = scores.get(user_id, 0) + reaction.count

        except Exception as e:
            print(f"```Skipped channel {channel.name}: {e}```")

    save_scores()
    await ctx.send("```Backfill complete!\n Check out your leaderboard! with `!leaderboard````")


# Reset weekly scores every Sunday at midnight
async def weekly_reset():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now()
        days_until_sunday = (6 - now.weekday()) % 7  # Calculate days until next Sunday
        
        next_reset = (now + timedelta(days=days_until_sunday)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        if next_reset < now:
            next_reset += timedelta(days=7)  # Move to the next week if we've already passed this week's reset time
    
        wait_time = (next_reset - now).total_seconds()

        await asyncio.sleep(wait_time)
        channel = bot.get_channel(leaderboard_channel_id)

        if channel:
            if not weekly_scores:
                msg = "``No weekly scores yet.``"
        
            sorted_scores = sorted(weekly_scores.items(), key=lambda x: x[1], reverse=True)
            msg = "# Here's the leaderboard for the past week:\n\n"

            for i, (user_id, score) in enumerate(sorted_scores[:3], start=1):
                user = await bot.fetch_user(int(user_id))
                msg += f"```{i}. {user.name} - {score} ❤️\n```"
            msg += "\n## Weekly scores have been reset!"
            await channel.send(msg)

        weekly_scores.clear()
        save_weekly_scores()


# Command to set the leaderboard channel
leaderboard_channel_id = None

@bot.command()
async def set_leaderboard_channel(ctx, channel: discord.TextChannel):
    global leaderboard_channel_id
    leaderboard_channel_id = channel.id
    await ctx.send(f"Leaderboard channel set to {channel.mention}!")

# Weekly leaderboard command to display top 5 users
@bot.command()
async def weekly(ctx):
    if not weekly_scores:
        await ctx.send("``No weekly scores yet.``")
        return
    
    sorted_scores = sorted(weekly_scores.items(), key=lambda x: x[1], reverse=True)
    msg = "# Weekly Leaderboard:\n\n"

    for i, (user_id, score) in enumerate(sorted_scores[:5], start=1):
        user = await bot.fetch_user(int(user_id))
        msg += f"```{i}. {user.name} - {score} ❤️\n```"
    await ctx.send(msg)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    bot.loop.create_task(weekly_reset())

bot.run(TOKEN)

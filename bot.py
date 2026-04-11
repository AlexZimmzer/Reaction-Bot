import discord
from discord.ext import commands
import json
import os

# Token for bot connection
TOKEN = "I DONT CARE"

heartList = ["❤️", "🤎", "🧡", "💛", "💚", "💙", "🩵", "💜",
             "🩷", "🖤", "🩶", "🤍", "❣️", "💕", "💞", "💓",
             "💗", "💖", "💘", "💝", "💟", "❤️‍🔥", "♥️", "🫀"]

# Permissions
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

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

# Event listener for ❤️ reactions
@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) not in heartList or user.bot:
        return
    author = reaction.message.author
    if user.id == author.id or author.bot:
        return
    user_id = str(author.id)
    scores[user_id] = scores.get(user_id, 0) + 1
    save_scores()

# Score command to display user's score
@bot.command()
async def score(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    user_id = str(user.id)
    count = scores.get(user_id, 0)
    await ctx.send(f"{user.name}'s ❤️ score: {count}")

@bot.command()
async def leaderboard(ctx):
    if not scores:
        await ctx.send("No scores yet.")
        return
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    msg = "**Leaderboard:**\n\n"

    for i, (user_id, score) in enumerate(sorted_scores[:5], start=1):
        user = await bot.fetch_user(int(user_id))
        msg += f"{i}. {user.name} - {score} ❤️\n"
    await ctx.send(msg)


# Scan previous messages for heart reactions and update scores (backfill)!
# this one was really annyoing 
@bot.command()
async def backfill(ctx):
    scores.clear()
    save_scores()
    await ctx.send("Starting backfill... this might take me a while...")

    for channel in ctx.guild.text_channels:
        await ctx.send(f"Scanning #{channel.name} :3")
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
            print(f"Skipped channel {channel.name}: {e}")

    save_scores()
    await ctx.send("Backfill complete!\n Check out your leaderboard! with `!leaderboard`")

bot.run(TOKEN)
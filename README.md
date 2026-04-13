# Discord Reaction Bot
This is my first project involving Discord! I've wanted to do something like this for a while so this was a pretty fun experiment.

This Discord Bot records the number of heart reacts a user has on their messages, generating their "score". This bot was based on an X post by the user [FilledwithUrine](https://x.com/FilledwithUrine/status/2042743092860670456?s=20) and was created by [Alex Zimmer](https://github.com/AlexZimmzer).

## Discord Connection
This bot was created using the [Discord Developer Portal](https://discord.com/developers/home). Using OAuth2's bot scope, it can be invited to servers using a URL.

The bot also uses general permissions in the server to operate, including View Channels and Send Messages. It uses a generated Token to connect with the bot.py file. This token is used in the actual code, but I ran into so many problems with Git trying to get this committed. Simce I'm only using this for one server, I didnt really care if the token was used somewhere, but Git just refused to commit without any changes, and I really didn't want to worry about SECRETS right now. So, the token is customizable :)

## bot.py
This file contains the main operation of the bot, like the permissions, functions, and commands.

### !score (user)
This command will display the score of either the user if the argument was added, or the author if no user was attached.

### !leaderboard
This command shows the top 5 user scores.

### !backfill
This command scans previous messages for heart reactions and updates scores. This command first clears the score.json file, iterates through each channel in the server, and records the number of heart reactions on user messages. The existing operation scans the past 1,000 messages in a channel, but this is fully customizable.

Since the bot cannot operate (currently) without being run on a local machine, this is necessary as it can record everything unaccounted for. **One thing I would like to add is to make this a moderator-only command, so as to prevent individual members from scrubbing records.**

Alternatively, if you want to start with a fresh new score, that works too!

## scores.json
This file contains the list of each user's score. It is accessed in all of the commands and functions.

# Changelog

## 4/12
Today I added a new feature to the bot: weekly scores! Now, users are able to see who in the server has gotten the most heart reacts in the past week.

### weekly_reset
This asyncronous function resets the weekly counter on Sundays at midnight. It calculates the time until the end of the week, determines if the current time is past the the current week's reset time, and will send a leaderboard message to the provided channel from the next command...

### !set_leaderboard_channel
This command requires a **(channel: discord.TextChannel)** parameter, and sets the channel that the weekly message will be sent to. Exploring moderator-only commands might be a future addition, since not everyone should be able to use this.

### !weekly
This is a command similar to **!leaderboard** that will just show the current week's leaderboard. Nothing super different here.

### weekly_scores.json
This is almost exactly similar to scores.json, however this file is reset weekly by **weekly_reset**.

### Other
I also took the opportunity to use [Railway](https://railway.com/) to explore deployment. I was able to use this GitHub repository to remotely run the bot using their servers! Pretty cool stuff!

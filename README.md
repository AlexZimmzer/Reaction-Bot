# Discord Reaction Bot
This is my first project involving Discord! I've wanted to do something like this for a while so this was a pretty fun experiment.
This Discord Bot records the number of heart reacts a user has on their messages, generating their "score". This bot was based on an X post by the user [FilledwithUrine](https://x.com/FilledwithUrine/status/2042743092860670456?s=20) and was created by [Alex Zimmer](https://github.com/AlexZimmzer).

## Discord Connection
This bot was created using the [Discord Developer Portal](https://discord.com/developers/home). Using OAuth2's bot scope, it can be invited to servers using a URL.

The bot also uses general permissions in the server to operate, including View Channels and Send Messages. It uses a generated Token to connect with the bot.py file.

## bot.py
This file contains the main operation of the bot, like the permissions, functions, and commands.

### !score (user)
This command will display the score of either the user, or the author if no user was attached.

### !leaderboard
This command shows the top 5 user scores. 

### !backfill
This command scans previous messages for heart reactions and updates scores. This command first clears the score.json file, iterates through each channel in the server, and records the number of heart reactions on user messages. The existing operation scans the past 1,000 messages in a channel, but this is fully customizable.
Since the bot cannot operate (currently) without being run on a local machine, this is necessary as it can record everything unaccounted for. **One thing I would like to add is to make this a moderator-only command, so as to prevent individual members from scrubbing records.**
Alternatively, if you want to start with a fresh new score, that works too!

## scores.json
This file contains the list of each user's score. It is accessed in all of the commands and functions.

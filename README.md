# cardrpgdiscord
This a bot to play card based rpgs on discord

Here are some of the commands to get started (all commands start with !, this is the prefix that tells discord to talk to this bot):

* `!library`: returns a comma delimited list of all the games implemented in this bot.

* `!play <name of game>`: starts playing a game on this server. This means that each discord server can only have one game running at time. However players can interact with the game fram individual chat channels (mimicing a player's hand if needed).

* `!instructions`: If a game has been started it returns the provided instructions specifc to the game. If a game has not started then it returns this block of text.

* `!draw [optional arguments]`: draws a card from the rpg deck with space-delimited arguments as needed by the individual game

* `!Q <function_name> [optional arguments]`: this essentially a hook to a wild function. This hook calls a function matching the function_name string provided of the game currently being played and passes to it the space-delimted optional arguments.
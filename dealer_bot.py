import discord
from discord.ext import commands
from discord.ext import tasks
import random
import os
import json
from datetime import datetime
import time

import abstract_decks.decks as decks

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''


with open("discord.token", "r") as file:
    token = file.read()

intents = discord.Intents.default()
intents.members = True


test_list = {}

# game_deck =  decks.Juggernaut()



bot = commands.Bot(command_prefix='!', description=description, intents=intents)

bot.games = {}
bot.implemented_decks = decks.implemented_decks
bot.instructions = f'''This a bot to play card based rpgs on discord

Here are some of the commands to get started (all commands start with !, this is the prefix that tells discord to talk to this bot):

* !library: returns a comma delimited list of all the games implemented in this bot.

* !play (name of game): starts playing a game on this server. This means that each discord server can only have one game running at time. However players can interact with the game fram individual chat channels (mimicing a player's hand if needed).

* !instructions: If a game has been started it returns the provided instructions specifc to the game. If a game has not started then it returns this block of text.

* !draw [optional arguments]: draws a card from the rpg deck with space-delimited arguments as needed by the individual game

* !Q <function_name> [optional arguments]: this essentially a hook to a wild function. This hook calls a function matching the function_name string provided of the game currently being played and passes to it the space-delimted optional arguments.
'''

# Helper functions
def _server_has_game(id):
    if id in bot.games.keys():
        return True
    else:
        return False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def library(ctx):
    await ctx.send(" ,".join(decks._implemented_games()))

@bot.command()
async def draw(ctx, *args):
    if _server_has_game(ctx.guild.id):
        bot.games[ctx.guild.id]["last_action"] = datetime.now()
        await bot.games[ctx.guild.id]["game"].draw(ctx, args)

    else:
        await ctx.send("A game has not been started on this server. Send !instructions to find how to get started.")

@bot.command()
async def play(ctx, game: str):
    if game in bot.implemented_decks:
        bot.games[ctx.guild.id] = {"game":bot.implemented_decks[game](), "started": datetime.now(), "last_action": datetime.now()}        
        intro_text = getattr(bot.games[ctx.guild.id]["game"], "introduction", False)
        if intro_text:
            await ctx.send(intro_text)
        else:
            await ctx.send(f"Game of {game} started on this server")

    else:
        await ctx.send(f"Sorry but {game} has not been implemented. Please choose another game from: {' ,'.join(decks._implemented_games())}")

@bot.command()
async def Q(ctx, *args):
    if _server_has_game(ctx.guild.id):
        func = getattr(bot.games[ctx.guild.id]["game"], args[0])
        await func(ctx, args)
    else:
        await ctx.send("A game has not been started on this server. Send !instructions to find how to get started.")

@bot.command()
async def instructions(ctx, *args):
    if ctx.guild.id in bot.games:
        await ctx.send(bot.games[ctx.guild.id]["game"].instructions(ctx, args))
    else:
        await ctx.send(bot.instructions)
    

@tasks.loop(seconds = 300) # repeat after every 300 seconds
async def myLoop():
    ref_t= datetime.now()
    for key, value in bot.games.items():
        game_age = ref_t - value["last_action"]
        if game_age.total_seconds()>12*3600:
            del bot.games[key]

myLoop.start()

bot.run(token)
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

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True


test_list = {}

# game_deck =  decks.Juggernaut()



bot = commands.Bot(command_prefix='!', description=description, intents=intents)

bot.games = {}
bot.implemented_decks = decks.implemented_decks

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def library(ctx):
    await ctx.send(" ,".join(decks._implemented_games()))

@bot.command()
async def draw(ctx, *args):
    bot.games[ctx.guild.id]["last_action"] = datetime.now()

    my_files = await bot.games[ctx.guild.id]["game"].draw(ctx, args)
    my_files = [discord.File(x) for x in my_files]
    await ctx.send(files=my_files)

@bot.command()
async def play(ctx, game: str):
    if game in bot.implemented_decks:
        bot.games[ctx.guild.id] = {"game":bot.implemented_decks[game]()}
        bot.games[ctx.guild.id]["started"] = datetime.now()
        bot.games[ctx.guild.id]["last_action"] = datetime.now()
        await ctx.send(f"Game of {game} started on this server")
    else:
        await ctx.send(f"Sorry but {game} has not been implemented. Please choose another game from: {' ,'.join(decks._implemented_games())}")


@tasks.loop(seconds = 300) # repeat after every 300 seconds
async def myLoop():
    ref_t= datetime.now()
    for key, value in bot.games.items():
        game_age = ref_t - value["last_action"]
        if game_age.total_seconds()>12*3600:
            del bot.games[key]

myLoop.start()

bot.run(os.environ.get("TOKEN"))
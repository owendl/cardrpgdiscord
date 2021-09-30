import discord
from discord.ext import commands
from discord.ext import tasks
import random
import os
import json

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
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def library(ctx):
    await ctx.send(" ,".join(decks._implemented_games()))

@bot.command()
async def draw(ctx):
    await ctx.send("did a draw")

@bot.command()
async def play(ctx, game: str):
    if game in bot.implemented_decks:
        bot.games[ctx.guild.id] = bot.implemented_decks[game]()
        await ctx.send(bot.games[ctx.guild.id].deck_folder)
    else:
        await ctx.send(f"Sorry but {game} has not been implemented. Please choose another game from: {' ,'.join(decks._implemented_games())}")


@tasks.loop(seconds = 30) # repeat after every 10 seconds
async def myLoop():
    print("test")
myLoop.start()

bot.run(os.environ.get("TOKEN"))
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

games = {}

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

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
async def draw(ctx):
    await ctx.send("did a draw")

@bot.command()
async def play(ctx, game: str):
    print(game)
    await ctx.send("starting game of "+game)


@tasks.loop(seconds = 30) # repeat after every 10 seconds
async def myLoop():
    print("test")
myLoop.start()

bot.run(os.environ.get("TOKEN"))
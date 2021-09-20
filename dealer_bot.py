import discord
from discord.ext import commands
from discord.ext import tasks
import random
import os

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True


test_list = []


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
async def add(ctx, value: str):
    global test_list
    test_list.append(value)

@bot.command()
async def check(ctx):
    global test_list
    await ctx.send(", ".join(test_list))

@tasks.loop(seconds = 3) # repeat after every 10 seconds
async def myLoop():
    print("test")


myLoop.start()

bot.run(os.environ.get("TOKEN"))
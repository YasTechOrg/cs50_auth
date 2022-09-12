import disnake
from disnake.ext import commands
import asyncio
import time
import sqlite3

token = input("Copy And paste your token here")

intents = disnake.Intents.all()

bot = commands.Bot(command_prefix = '.', intents=intents, help_command=None)
               #Hamidreza Farzin    Hossein araghi      daniel soheil        sahar halaji     amirhossein foroghi
white_list = [440552369864966144, 696999720182087722, 724108042227941427, 898160244235075625, 714364321139785809]

@bot.event
async def on_ready():
        print(f""" Bot ID : {bot.user.name}""")
        print("Developer : Hamidreza Farzin (H_VICTOR#2999)")
        await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="CS50X Iran"))

@bot.command()
@commands.cooldown(4, 2, commands.BucketType.guild)
async def ping(ctx):
    if ctx.author.id in white_list:
        await ctx.send(f"**Bot ping : {round(bot.latency * 1000)}ms**")
    else: 
        pass

bot.load_extension("cogs.check")
bot.run(token, reconnect=True)

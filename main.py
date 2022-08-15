from itertools import cycle
import discord
from discord.ext import commands, tasks
import json
import os
from itertools import cycle
from dotenv import load_dotenv

# Load .env file
load_dotenv()
token = os.getenv('TOKEN')


prefix = "!"

status = cycle(["Made by Mankifg#1810","Made by luka heric#9699", "Watching You", "m!help"])
@tasks.loop(seconds=10)
async def status_swap():
    await bot.change_presence(activity=discord.Game(next(status)))


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None


intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    description="Poletni Tabor Računalništva",
    intents=intents,
)

#load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    status_swap.start()

bot.run(token)
import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

unwanted_files = ["exam.txt"]

with open("configuration.json", "r") as config: 
	data = json.load(config)
	prefix = data["prefix"]
	owner_id = data["owner_id"]


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None


intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    description="Mankifg's discord bot.",
    intents=intents,
    owner_id=owner_id,
)


if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py") and filename not in unwanted_files:
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
        )
    )

bot.run(token)
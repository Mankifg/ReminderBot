import json
import discord
from discord.ext import commands

def readNewData():
    with open('./data/newSchedule.json', 'r') as f:
        newData = json.load(f)
    
    return newData

def read():
    with open('./data/schedule.json', 'r') as f:
        data = json.load(f)
    
    return data

def write(data):
    with open('./data/schedule.json', 'w') as f:
        json.dump(data, f)

class updateCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="update", usage="", description="")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def update(self, ctx):
        data = read()
        newData = readNewData()

        data.update(newData)

        write(data)

        
def setup(bot: commands.Bot):
    bot.add_cog(updateCog(bot))

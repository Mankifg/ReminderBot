from threading import Timer
import discord
from discord.ext import commands, tasks
from itertools import cycle
import datetime
import json
import asyncio

import requests
import os

TIMER = 30

def read():
    with open('./data/schedule.json', 'r') as f:
        return json.load(f)


class tasksCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot
  
    @commands.command(name="setchannel", usage="", description="Sets channel for preset events.", aliases=['sc'])
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channel: discord.TextChannel):
        with open('data/channel.txt',"w") as f:
            f.write(str(channel.id))
        await ctx.send(f"Channel set to {channel.mention}")

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(TIMER)
            data = read()
 

            for i in range(len(data['times'])):

                if data['times'][i] == datetime.datetime.now().strftime("%H:%M"):
                    channel = self.bot.get_channel(int(open('data/channel.txt', 'r').read()))
                    await channel.send('@everyone')
                    q = discord.Embed(
                        title=f"Event: **{data['tasks'][i]}**",
                        description=f"Event time: {data['times'][i]}",
                        color=discord.Color.dark_blue(),
                    )

                    await channel.send(embed=q)

                    break

                fut_time =  data["times"][i]
                fut_h = int(fut_time.split(":")[0])
                fut_m = int(fut_time.split(":")[1])

                fut_m = fut_m - 30
                if fut_m < 0:
                    fut_m = fut_m + 60
                    fut_h = fut_h - 1

                fut_time = str(fut_h) + ":" + str(fut_m)
                

                if fut_time[-2] == ":":
                    fut_time = fut_time + "0"   
                
                now = datetime.datetime.now()
                a = [now.hour, now.minute]
                b = [fut_h, fut_m]
                if a == b:
                    channel = self.bot.get_channel(int(open('data/channel.txt', 'r').read()))
                    await channel.send('@everyone')
                    q = discord.Embed(
                        title=f"Event **{data['tasks'][i]}** in 30 minutes",
                        description=f"Event time: {data['times'][i]}",
                        color=discord.Color.dark_blue(),
                    )
                    
                    await channel.send(embed=q)

                    break
    

def setup(bot: commands.Bot):
    bot.add_cog(tasksCog(bot))


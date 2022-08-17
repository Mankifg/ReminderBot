from ast import alias
from calendar import WEDNESDAY
import discord
from discord.ext import commands, tasks
from itertools import cycle
import datetime
import json
import asyncio
import requests, os

dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]

def read():
    with open("./data/schedule.json", "r") as f:
        return json.load(f)

with open("data/settings.json", "r") as f:
    settings = json.load(f)
ch = settings["channel"]
delay = settings["delay"]

class dailyCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(10)
            data = read()
            channel = self.bot.get_channel(ch)

            for i in range(len(data["tasks"])):
                curr_time_rl = datetime.datetime.now().strftime("%H:%M")
                curr_time_task = data["tasks"][i]["startTime"]
                curr_date_rl = datetime.datetime.now().strftime("%d.%m.%Y")
                curr_date_task = data["tasks"][i]["date"]

                if curr_date_rl == curr_date_task:

                    if curr_time_rl == curr_time_task:

                        q = discord.Embed(
                            title=data["tasks"][i]["title"],
                            description=data["tasks"][i]["description"],
                            color=discord.Color.blue(),
                        )
                        await channel.send("@everyone")
                        await channel.send(embed=q)

                    for x in range(len(delay)):
                        rem_time = curr_time_task.split(":")
                        rem_h = int(rem_time[0])
                        rem_m = int(rem_time[1])
                        rem_m = rem_m - delay[x]
                        if rem_m < 0:
                            rem_h = rem_h - 1
                            rem_m = rem_m + 60
                        if (
                            curr_date_rl == curr_date_task
                            and rem_h == datetime.datetime.now().hour
                            and rem_m == datetime.datetime.now().minute
                        ):
                            with open("./data/channel.txt", "r") as f:
                                channel = f.read()
                            channel = int(channel)
                            channel = self.bot.get_channel(channel)
                            await channel.send("@everyone")
                            q = discord.Embed(
                                title=f'In **{delay[x]}**: {data["tasks"][i]["title"]}',
                                description=data["tasks"][i]["description"],
                                color=discord.Color.blue(),
                            )
                            await channel.send(embed=q)


def setup(bot: commands.Bot):
    bot.add_cog(dailyCog(bot))

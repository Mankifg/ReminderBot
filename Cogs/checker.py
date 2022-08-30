import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json

from helpers import read

dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]

with open('data/settings.json',"r") as f:
    settings = json.load(f)
    
delay = settings["delay"]
channel = settings["channel"]

class DailyCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ch = self.bot.get_channel(channel)

        while True:
            await asyncio.sleep(10)
            data = read()

            for i in range(len(data['tasks'])):
                date_of_a_task = datetime.strptime(f"{data['tasks'][i]['date']} {data['tasks'][i]['startTime']}", "%Y-%m-%d %H:%M")
                current_date = datetime.now()

                t = date_of_a_task.timestamp() - current_date.timestamp()

                if t < 0 and abs(t) < 30:
                    q = discord.Embed(
                        title=data["tasks"][i]["title"],
                        description=data["tasks"][i]["description"],
                        color=discord.Color.blue()
                        )
                    await channel.send("@everyone")
                    await channel.send(embed=q)
                    await asyncio.sleep(30)

                for x in range(len(delay)):
                    t = date_of_a_task.timestamp() - (current_date.timestamp() + delay[x]*60)
                    if t < 0 and abs(t) < 30:
                        await channel.send("@everyone")
                        q = discord.Embed(
                            title=f'In **{delay[x]}** minutes: {data["tasks"][i]["title"]}',
                            description=data["tasks"][i]["description"],
                            color=discord.Color.blue()
                        )
                        await ch.send(embed=q)
                        await asyncio.sleep(30)


def setup(bot: commands.Bot):
    bot.add_cog(DailyCog(bot))

import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json
import datetime

from helpers import read

dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]

with open('data/settings.json',"r") as f:
    settings = json.load(f)
    
delay = settings["delay"]
channel = settings["channel"]

opt = "@everyone"

class DailyCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ch = self.bot.get_channel(channel)

        while True:
            await asyncio.sleep(10)
            data = read()

            today_n_of_week = datetime.datetime.today().weekday() + 1

            today_format = datetime.datetime.today().strftime("%H:%M")

            if len(today_format) == 4:
                today_format = "0" + today_format 
            
            for i in range(len(data['tasks'])):

                if str(today_n_of_week) in str(data["tasks"][i]["days"]) and str(data['tasks'][i]['time']) == str(today_format):

                    q = discord.Embed(
                        title=data["tasks"][i]["taskname"],
                        description=data["tasks"][i]["description"],
                        color=discord.Color.blue()
                        )

                    await ch.send(opt)
                    await ch.send(embed=q)

                    await asyncio.sleep(30)


        
                    
                for x in range(len(delay)):

                    today_h = int(data['tasks'][i]['time'].split(":")[0])
                    today_m = int(data['tasks'][i]['time'].split(":")[1])
                    today_m = today_m + delay[x]
                    if today_m > 59:
                        today_m = today_m - 60
                        today_h = today_h + 1
                    if today_h > 23:
                        today_h = today_h - 24
                        if len(today_h) == 1:
                            today_h = "0" + str(today_h)
                    
                    if str(today_n_of_week) in str(data["tasks"][i]["days"]) and str(data['tasks'][i]['time']) == f"{today_h}{today_m}":
                        await ch.send("@everyone")
                        q = discord.Embed(
                            title=f'In **{delay[x]}** minutes: {data["tasks"][i]["taskname"]}',
                            description=data["tasks"][i]["description"],
                            color=discord.Color.blue()
                        )

                        await ch.send(embed=q)
                        await asyncio.sleep(30)


def setup(bot: commands.Bot):
    bot.add_cog(DailyCog(bot))

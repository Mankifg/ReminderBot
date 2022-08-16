from ast import alias
import discord
from discord.ext import commands, tasks
from itertools import cycle
import datetime
import json
import asyncio

def read():
    with open('./data/schedule.json', 'r') as f:
        return json.load(f)

class dailyCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(30)
            data = read()

            if "8:00" == datetime.datetime.now().strftime("%H:%M"):
                channel = self.bot.get_channel(int(open('data/channel.txt', 'r').read()))
                await channel.send('@everyone')

                stOpravil = len(data["tasks"])

                urnik2 = discord.Embed(
                    title="Urnik",
                    description="",
                    color=discord.Color.dark_blue(),
                )

                for i in range(stOpravil):
                    urnik2.add_field(
                        name=data['tasks'][i],
                        value=f"**```{data['times'][i]}```**",
                        inline=True,
                    )

                urnik2.set_author(name="Mentorji")
                await channel.send(embed=urnik2)


def setup(bot: commands.Bot):
    bot.add_cog(dailyCog(bot))

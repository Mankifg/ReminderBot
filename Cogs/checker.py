import discord
from discord.ext import commands, tasks
from itertools import cycle
import datetime
import json
import asyncio


def read():
    with open('./data/schedule.json', 'r') as f:
        return json.load(f)


class tasksCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def check_for_tasks():
        print('abc')   

    @commands.command(name="setchannel", usage="", description="izpise urnik", aliases=['sc'])
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channel: discord.TextChannel):
        with open('data/channel.txt',"w") as f:
            f.write(str(channel.id))
        await ctx.send(f"Channel set to {channel.mention}")

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(30)
            data = read()

            for i in range(len(data['times'])):
                if data['times'][i] == datetime.datetime.now().strftime("%H:%M"):
                    channel = self.bot.get_channel(int(open('data/channel.txt', 'r').read()))
                    await channel.send(data['tasks'][i])
                    q = discord.Embed(
                        title="Urnik",
                        description="@everyone",
                        color=discord.Color.random(),
                    )
                    q.add_field(
                        name=data['tasks'][i],
                        value=f"**```{data['times'][i]}```**",
                        inline=True,
                    )
                    q.set_author(name="Mentorji")
                    await channel.send(embed=q)

                    break


    

    

        
def setup(bot: commands.Bot):
    bot.add_cog(tasksCog(bot))


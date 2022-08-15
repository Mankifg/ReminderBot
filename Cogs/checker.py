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
  
    @commands.command(name="setchannel", usage="", description="Sets channel for preset events.", aliases=['sc'])
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
                    await channel.send('@everyone')
                    q = discord.Embed(
                        title=f"Task **{data['tasks'][i]}**",
                        description=f"Time: {data['times'][i]}",
                        color=discord.Color.dark_blue(),
                    )
                    
                    await channel.send(embed=q)

                    break


    

    

        
def setup(bot: commands.Bot):
    bot.add_cog(tasksCog(bot))


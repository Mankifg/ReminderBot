import discord
from discord.ext import commands
import json

def preberiUrnik():
    with open('./data/schedule.json', 'r') as f:
        data = json.load(f)
    
    return data

class izpisUrnikaCog(commands.Cog, name="izpisUrnika"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="schedule", usage="", description="Give you schedule fot the day", aliases=['s'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def schedule(self, ctx):

        urnik = preberiUrnik()
        
        stOpravil = len(urnik["tasks"])

        urnik2 = discord.Embed(
            title="Urnik",
            description="",
            color=discord.Color.dark_blue(),
        )
        
        for i in range(stOpravil):
            urnik2.add_field(
                name=urnik['tasks'][i],
                value=f"**```{urnik['times'][i]}```**",
                inline=True,
            )

        urnik2.set_author(name="Mentorji")
        await ctx.send(embed=urnik2)
        
def setup(bot: commands.Bot):
    bot.add_cog(izpisUrnikaCog(bot))

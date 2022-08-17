import discord
from discord.ext import commands
import json
import datetime


def read():
    with open("./data/schedule.json", "r") as f:
        data = json.load(f)

    return data


dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]


class izpisUrnikaCog(commands.Cog, name="izpisUrnika"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="schedule",
        usage="",
        description="Give you schedule fot the day",
        aliases=["s"],
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def schedule(self, ctx):
        data = read()
        urnik2 = discord.Embed(
            title=f"Urnik {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} - **{dnevi[datetime.datetime.today().weekday()]}**",
            description="",
            color=discord.Color.dark_blue(),
        )

        for task in data["tasks"]:
            urnik2.add_field(
                name=f"**{task['startTime']}**  {task['title']}",
                value=f"_ㅤ{task['description']}_",
                inline=False,
            )

        await ctx.send(embed=urnik2)


def setup(bot: commands.Bot):
    bot.add_cog(izpisUrnikaCog(bot))

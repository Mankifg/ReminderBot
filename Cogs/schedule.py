import discord
from discord.ext import commands
import datetime
from helpers import read

dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]


def sortbytime(data):
    data = sorted(
        data,
        key=lambda x: x["time"],
    )
    return data


class IzpisUrnikaCog(commands.Cog, name="izpisUrnika"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="schedule",
        usage="",
        description="Give you schedule fot the day",
        aliases=["s"],
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def schedule(self, ctx, nOfDay: str = None):
        #! implement checks for nofday
        if nOfDay == None:
            nOfDay = datetime.datetime.today().weekday() + 1
            nOfDay = str(nOfDay)
        else:
            title = f"Urnik za **{dnevi[nOfDay]}** {nOfDay} -- Ni danes"

        data = read()
        data["tasks"] = sortbytime(data["tasks"])

        urnik2 = discord.Embed(
            title=f"Urnik {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} - **{dnevi[int(nOfDay) - 1]}** {nOfDay}",
            description="",
            color=discord.Color.dark_blue(),
        )

        out = ""
        for task in data["tasks"]:
            if nOfDay in str(task["days"]):
                out = out + f"**{task['time']}**  {task['taskname']}" + "\n"

                if not task["description"] == "":
                    out += f"\t_{task['description']}_" + "\n"

        urnik2.add_field(name="Urnik", value=out, inline=True)
        await ctx.send(embed=urnik2)


def setup(bot: commands.Bot):
    bot.add_cog(IzpisUrnikaCog(bot))

import discord
from discord.ext import commands
import datetime,json,asyncio


with open('data/settings.json',"r") as f:
    settings = json.load(f)

TIME = settings["time"]
ch = settings["channel"]

dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]


def read():
    with open("./data/schedule.json", "r") as f:
        return json.load(f)


class dailyCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(10)
            data = read()

            if TIME == datetime.datetime.now().strftime("%H:%M"):
                channel = self.bot.get_channel(ch)
                
                await channel.send("@everyone")

                urnik2 = discord.Embed(
                    title=f"Urnik {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} - **{dnevi[datetime.datetime.today().weekday()]}**",
                    description="",
                    color=discord.Color.dark_blue(),
                )
                
                
                    
                opt = ""
                for task in data["tasks"]:
                    if task["description"] == "":
                        opt += f"**{task['startTime']}**  {task['title']}\n"
                    else:
                        opt += f"**{task['startTime']}**  {task['title']}\n\t_{task['description']}_\n"

                urnik2.add_field(
                    name="Opis",
                    value=opt,
                    inline=False,
                )

                await channel.send(embed=urnik2)

def setup(bot: commands.Bot):
    bot.add_cog(dailyCog(bot))

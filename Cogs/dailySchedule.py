import discord
from discord.ext import commands
import datetime,json,asyncio,requests,os
from dotenv import load_dotenv

load_dotenv()

url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

loc = os.getenv("WEATHER")

with open('data/settings.json',"r") as f:
    settings = json.load(f)

TIME = settings["time"]
ch = settings["channel"]

dnevi = ["ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota", "nedelja"]


def weather():
    with open("./data/settings.json", "r") as f:
        settings = json.load(f)

    location = settings["place"]

    resp = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={loc}"
    ).json()
    try:
        lat = resp[0]["lat"]
        lon = resp[0]["lon"]
    except:
        lat = 0
        lon = 0

    querystring = {"lon": lon, "lat": lat}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDKEY"),
        "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return response, lat, lon


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
                w, lat, lon = weather()
                if not lat == 0 and not lon == 0:

                    urnik2.add_field(
                        name="Temperatura",
                        value=f"{w['data'][0]['temp']}°C",
                        inline=False,
                    )

                    urnik2.set_thumbnail(
                        url=f"https://www.weatherbit.io/static/img/icons/{w['data'][0]['weather']['icon']}.png"
                    )
                else:
                    urnik2.add_field(
                        name="Temperatura",
                        value="Ni podatka",
                        inline=False,
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

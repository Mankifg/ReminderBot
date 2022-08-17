from discord.ext import commands
import json


def read():
    with open("./data/schedule.json", "r") as f:
        data = json.load(f)

    return data


def write(data):
    with open("./data/schedule.json", "w") as f:
        json.dump(data, f)

with open("./data/settings.json", "r") as f:
    settings = json.load(f)
adminrole = settings["adminrole"]

def addSorted(data, task, time, date):
    novaUra, noveMin = time.split(":")
    novaUra = int(novaUra)
    noveMin = int(noveMin)
    novMon, novDay, novYear = date.split("-")
    novMon = int(novMon)
    novDay = int(novDay)
    novYear = int(novYear)
    novCas = (novYear * 365 * 24 * 60) + (novDay * 24 * 60) + (novaUra * 60) + noveMin
    d = len(data["tasks"])
    for i in range(d):
        ure, min = data["tasks"]["startTime"].split(":")
        ure = int(ure)
        min = int(min)
        mon, day, year = data["tasks"]["date"].split("-")
        mon = int(mon)
        day = int(day)
        year = int(year)
        trCas = (year * 365 * 24 * 60) + (day * 24 * 60) + (ure * 60) + min
        if novCas < trCas:
            data["tasks"].insert(
                i,
                {"date": date, "startTime": time, "title": task, "description": "add"},
            )
            return

    data["tasks"].insert(
        i, {"date": date, "startTime": time, "title": task, "description": "add"}
    )
    return


class addtaskCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="addtask",
        usage=" [time] [task]",
        description="Adds task to everyday routine.",
        aliases=["at"],
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.has_role(adminrole)
    async def addtask(self, ctx, time, *, task):
        if (
            len(time) != 16
            or not time[2] == ":"
            or not time[0:2].isdigit()
            or not time[3:5].isdigit()
        ):
            await ctx.send('Time must be in format "MM:HH-DD.MM.YYYY"')
            return

        data = read()
        time, date = time.split("-")



        addSorted(data, task, time, date)
        write(data)
        await ctx.send("Task added.")
        
    @commands.command(
        name="removetask",
        usage=" [task]",
        description="Removes task from everyday routine.",
        aliases=["rt"],
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.has_role(adminrole)
    async def removetask(self, ctx, task):
        data = read()

        d = len(data["tasks"])
        for i in range(d):
            if data["tasks"][i]["title"] == task:
                data["tasks"][i] = []
        write(data)
        await ctx.send("Task removed.")

def setup(bot: commands.Bot):
    bot.add_cog(addtaskCog(bot))
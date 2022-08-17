from datetime import datetime

from discord.ext import commands
from helpers import read, write


def add_sorted(data, task, time, date):
    # Datetime je zelo uporaben modul ;-)
    new_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    d = len(data['tasks'])
    for i in range(d):
        tr_cas = datetime.strptime(f"{data['tasks'][i]['date']} {data['tasks'][i]['startTime']}", "%Y-%m-%d %H:%M")
        if new_date < tr_cas:
            data['tasks'].insert(i, {"date": date, "startTime": time, "title": task, "description": "add"})
            return

    data['tasks'].append({"date": date, "startTime": time, "title": task, "description": "add"})


class AddTaskCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="addtask", usage=" [time] [task]", description="Adds task to everyday routine.",
                      aliases=['at'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def add_task(self, ctx, time, *, task):
        if len(time) != 16:
            await ctx.send("Time must be in format YYYY-MM-DD HH:MM")
            return

        data = read()
        date, time = time.split()
        add_sorted(data, task, time, date)
        write(data)
        await ctx.send("Task added.")

    @commands.command(name="removetask", usage=" [task]", description="Removes task from everyday routine.",
                      aliases=['rt'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remove_task(self, ctx, task):
        data = read()

        d = len(data["tasks"])
        for i in range(d):
            if data["tasks"][i]["title"] == task:
                del data["tasks"][i]

        write(data)
        await ctx.send("Task removed.")


def setup(bot: commands.Bot):
    bot.add_cog(AddTaskCog(bot))

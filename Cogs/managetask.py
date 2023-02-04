from datetime import datetime
from discord.ext import commands
import json
from helpers import read, write

empty = [",","/","-"," ","."]

pathToSchedule = './data/schedule.json'


def add_sorted(data, task, time, date):
    new_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    d = len(data['tasks'])
    for i in range(d):
        tr_cas = datetime.strptime(f"{data['tasks'][i]['date']} {data['tasks'][i]['startTime']}", "%Y-%m-%d %H:%M")
        if new_date < tr_cas:
            data['tasks'].insert(i, {"date": date, "startTime": time, "title": task, "description": "add"})
            return

    data['tasks'].append({"date": date, "startTime": time, "title": task, "description": "add"})


class AddTaskCog(commands.Cog, name="addtask command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="addtask", usage=" [time] [task]", description="Adds task to everyday routine.",
                      aliases=['at'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def add_task(self, ctx):
        await ctx.send('Please enter task name:')

        msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        taskname = msg.content.lower()

        await ctx.send(f'Enter start time of **{taskname}**. (Format HH:MM)')
        msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        time = msg.content.lower()

        if not (len(time) == 5 and time[2] == ":"):
            if not len(time) == 4:
                
                await ctx.send("Invalid time. Please enter time in format HH:MM\nExiting")
                return
            else:
                time = f"0{time}"

        await ctx.send("What days of the week task happened?")
        msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        dates = msg.content.lower()

        await ctx.send(f"Enter description for **{taskname}**. (Type `.`,`/`,`-`,` ` to leave empty)")
        msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        desc = msg.content.lower()

        for i in range(len(empty)):
            if desc == empty[i].lower():
                desc = ""

        data = read()

        djosn = {
            "taskname": taskname,
            "time": time,
            "days": dates,
            "description":desc
        }       
        data["tasks"].append(djosn)

        write(data)
        await ctx.send(f"Added {taskname} to tasks.")

    @commands.command(name="removetask", usage=" [task]", description="Removes task from everyday routine.",
                      aliases=['rt'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remove_task(self, ctx, task):
        data = read()

        d = len(data["tasks"])
        for i in range(d):
            if data["tasks"][i]["taskname"] == task:
                del data["tasks"][i]

        write(data)
        await ctx.send(f"Removed task {task}")

def setup(bot: commands.Bot):
    bot.add_cog(AddTaskCog(bot))

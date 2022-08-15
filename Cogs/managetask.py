import discord
from discord.ext import commands
import json

def read():
    with open('./data/schedule.json', 'r') as f:
        data = json.load(f)
    
    return data

def write(data):
    with open('./data/schedule.json', 'w') as f:
        json.dump(data, f)

def addSorted(data, task, time):
    novaUra, noveMin = time.split(":")
    novaUra = int(novaUra)
    noveMin = int(noveMin)

    d = len(data['times'])
    for i in range(d):
        ure, min = data['times'][i].split(":")
        ure = int(ure)
        min = int(min)
        if (novaUra * 60 + noveMin < ure * 60 + min):
            data['times'].insert(i, time)
            data['tasks'].insert(i, task)
            return
    
    ure, min = data['times'][d-1].split(":")
    ure = int(ure)
    min = int(min)

    
    data['times'].insert(d, time)
    data['tasks'].insert(d, task)
    
    return
                

class addtaskCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="addtask", usage=" [time] [task]", description="Adds task to everyday routine.", aliases=['at'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def addtask(self, ctx, time,*, task):
        if not len(time) == 5 or not time[2] == ":" or not time[0:2].isdigit() or not time[3:5].isdigit():
            await ctx.send("Time must be in format HH:MM")
            return
        
        data = read()
        addSorted(data,task,time)
        write(data)
        await ctx.send("Task added.")

    @commands.command(name="removetask", usage=" [task]", description="Removes task from everyday routine.", aliases=['rt'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def removetask(self, ctx, task):


        data = read()
        try:
            time = data['times'][data['tasks'].index(task)]
        except:
            await ctx.send("Task not found.")
            return

        data['tasks'].remove(task)
        data['times'].remove(time)
        write(data)
        await ctx.send("Task removed.")


        
        
def setup(bot: commands.Bot):
    bot.add_cog(addtaskCog(bot))
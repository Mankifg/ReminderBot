<<<<<<< HEAD
import discord
from discord.ext import commands
import asyncio
import time
import datetime
import requests
import json
import datetime

unix_time_now = "https://showcase.api.linx.twenty57.net/UnixTime/tounixtimestamp?datetime=now"

class ReminderCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="remind", usage="[x[s,m,h,d,w]] / [hh:mm] [msg]", description="It will remind you with preset message.", aliases=['r'],)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remind(self, ctx, time, *, message='Reminder!'):
        now = datetime.datetime.now()
        valid_ends = ['s', 'm', 'h', 'd',"w"]
        dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        
        if time[-1] not in valid_ends:
            if ":" in time:
                time = time.split(":")
                time[0] = int(time[0])
                time[1] = int(time[1])

                if int(time[0]) > 23 or int(time[1]) > 59:
                    await ctx.send("Invalid time")
                    return       

                curr = [now.hour, now.minute] 
                diff = [time[0] - curr[0],time[1] - curr[1]]
                

                if diff[1] < 0:
                    diff[1] = 60 + diff[1]
                    diff[0] = diff[0] - 1
                if diff[0] < 0:
                    diff[0] = 24 + diff[0]

                time_format = f"{diff[0]}:{diff[1]}"

                time_sec = diff[0] * 3600 + diff[1] * 60

                if time_format[0] == 0:
                    time_format = time_format[1:]
                  
                tr = requests.get(unix_time_now).json()["UnixTimeStamp"]
                tr = int(tr) + time_sec

                await ctx.message.delete()
                remind = await ctx.send(f"Set Reminder to {time[0]}:{time[1]}. <t:{tr}:R>")
                await asyncio.sleep(time)
                await remind.delete()
                await ctx.send(message)
                


            else:
                await ctx.send("Invalid time format")
                return
        else:
            await ctx.message.delete()
            time = int(time[:-1]) * dict[time[-1]]
            tr = requests.get(unix_time_now).json()["UnixTimeStamp"]
            tr = int(tr) + time
            remind = await ctx.send(f"Reminder set for {time} seconds in <t:{tr}:R>")
            await asyncio.sleep(time)
            await remind.delete()
            await ctx.send(ctx.author.mention)
            q = discord.Embed(
                title=f"Reminder",
                description=f"{message}",
                color=discord.Color.dark_blue(),
            )
            await ctx.send(embed=q)
            
        
        
def setup(bot: commands.Bot):
=======
import discord
from discord.ext import commands
import asyncio
import time
import datetime
import requests
import json
import datetime

unix_time_now = "https://showcase.api.linx.twenty57.net/UnixTime/tounixtimestamp?datetime=now"

class ReminderCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="remind", usage="", description="", aliases=['r'],)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remind(self, ctx, time, *, message='Reminder!'):
        now = datetime.datetime.now()
        valid_ends = ['s', 'm', 'h', 'd',"w"]
        dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        
        if time[-1] not in valid_ends:
            if ":" in time:
                time = time.split(":")
                time[0] = int(time[0])
                time[1] = int(time[1])

                if int(time[0]) > 23 or int(time[1]) > 59:
                    await ctx.send("Invalid time")
                    return       

                curr = [now.hour, now.minute] 
                diff = [time[0] - curr[0],time[1] - curr[1]]
                

                if diff[1] < 0:
                    diff[1] = 60 + diff[1]
                    diff[0] = diff[0] - 1
                if diff[0] < 0:
                    diff[0] = 24 + diff[0]

                time_format = f"{diff[0]}:{diff[1]}"

                time_sec = diff[0] * 3600 + diff[1] * 60

                if time_format[0] == 0:
                    time_format = time_format[1:]
                  
                tr = requests.get(unix_time_now).json()["UnixTimeStamp"]
                tr = int(tr) + time_sec

                await ctx.message.delete()
                remind = await ctx.send(f"Set Reminder to {time[0]}:{time[1]}. <t:{tr}:R>")
                await asyncio.sleep(time)
                await remind.delete()
                await ctx.send(message)
                


            else:
                await ctx.send("Invalid time format")
                return
        else:
            await ctx.message.delete()
            time = int(time[:-1]) * dict[time[-1]]
            tr = requests.get(unix_time_now).json()["UnixTimeStamp"]
            tr = int(tr) + time
            remind = await ctx.send(f"Reminder set for {time} seconds in <t:{tr}:R>")
            await asyncio.sleep(time)
            await remind.delete()
            await ctx.send(message)
        
        
def setup(bot: commands.Bot):
>>>>>>> 371364d (added reminder)
    bot.add_cog(ReminderCog(bot))
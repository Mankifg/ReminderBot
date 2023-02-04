import discord, asyncio
from discord.ext import commands
from datetime import datetime


class ReminderCog(commands.Cog, name="ping command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="remind",
        usage="[x[s,m,h,d,w]] / [hh:mm] [msg]",
        description="It will remind you with preset message.",
        aliases=["r"],
    )

    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remind(self, ctx, t, *, message="Reminder!"):
        valid_ends = ["s", "m", "h", "d", "w"]
        dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

        now = datetime.now()

        if t[-1] not in valid_ends:
            if ":" in t:
                tf = t.split(":")
                tf[0] = int(tf[0])
                tf[1] = int(tf[1])

                if tf[0] > 23 or tf[1] > 59:
                    await ctx.send("Invalid time")
                    return

                hour_diff, minutes_diff = tf[0] - now.hour, tf[1] - now.minute

                if minutes_diff < 0:
                    minutes_diff += 60
                    hour_diff -= 1
                if hour_diff < 0:
                    hour_diff += 24

                time_sec = hour_diff * 3600 + minutes_diff * 60

                tr = now.timestamp() + time_sec

                # print(tf, hour_diff, minutes_diff, time_sec, tr)

                await ctx.message.delete()
                remind = await ctx.send(f"Set Reminder to {t}. <t:{int(tr)}:R>")
                await asyncio.sleep(time_sec)
                await remind.delete()
                await ctx.send(message)
            else:
                await ctx.send("Invalid time format")
                return
        else:
            await ctx.message.delete()
            time = int(t[:-1]) * dict[t[-1]]
            tr = now.timestamp() + time
            remind = await ctx.send(
                f"Reminder set for {time} seconds in <t:{int(tr)}:R>"
            )
            await asyncio.sleep(time)
            await remind.delete()
            q = discord.Embed(
                title=f"Reminder",
                description=f"{message}",
                color=discord.Color.dark_blue(),
            )
            await ctx.send(ctx.message.author.mention, embed=q)


def setup(bot: commands.Bot):
    bot.add_cog(ReminderCog(bot))

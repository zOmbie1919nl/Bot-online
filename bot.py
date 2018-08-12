import os
import discord
from discord.ext import commands

bot = commands.Bot(description='', command_prefix=commands.when_mentioned_or('z!'), pm_help=False)

#This is an event.
@bot.event
async def on_ready():
    print('Ready sir *salutes*')

'''On all commands the bit after the def is the thing you type after the prefix. All commands need ctx in the ().
The * means that when you type more than one word after the command in Discord it will be counted as one argument.
For example if it was without the * you could only put one word.
But you can do something that has multiple arguments such as a ban command.'''

@bot.command()
async def say(ctx, *, words):
  await ctx.send(words)
  await ctx.message.delete()


@bot.command()
async def kick(ctx, member: discord.Member, *, reason):
  await member.kick(reason=reason)
  em = discord.Embed(title='Kick', colour=0xff0000)
  em.add_field(name='Member:', value=member, inline=False)
  em.add_field(name='Reason:', value=reason, inline=False)
  await ctx.send(embed=em)


@bot.command()
async def ban(ctx, member: discord.Member, *, reason):
    await member.ban(reason=reason)
    em = discord.Embed(title='Ban', colour=0xff0000)
    em.add_field(name='Member:', value=member, inline=False)
    em.add_field(name='Reason', value=reason, inline=False)
    await ctx.send(embed=em)
    await ctx.message.delete()


@bot.command()
async def avatar(ctx, member: discord.Member):
    await ctx.send(member.avatar_url)


bot.run(os.environ['TOKEN'])

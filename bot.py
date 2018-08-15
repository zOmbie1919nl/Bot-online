import discord
import asyncio
import os
import aiohttp
from discord.ext import commands

bot = commands.Bot(description='', command_prefix=commands.when_mentioned_or('-'), pm_help=False)

#This is an event.
@bot.event
async def on_ready():
    print('Ready sir *salutes*')
    await bot.change_presence(activity=discord.Game(name='The moderator game. (prefix: !!)'))
    bot.load_extension('dave_Repl')


bot.remove_command('help')

def has_role (role_name, obj):
    return any(role_name == role.name.lower() for role in obj.roles)

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def joined(ctx, member: discord.Member):
    joindate = f'{member.joined_at.day}-{member.joined_at.month}-{member.joined_at.year}'
    joined = f'{joindate}, {member.joined_at.hour}:{member.joined_at.minute}'
    await ctx.send(f'{member.name} joined at {joined}')

@bot.command()
async def giverole(ctx, member: discord.Member, role):
    role = discord.utils.get(member.guild.roles, name=role)
    await member.add_roles(role)
    await ctx.send('{} has been given the **{}** role.'.format(member.name, role))

@bot.command()
async def id(ctx, member: discord.Member):
    await ctx.send(f'{member.id}')

@bot.command()
async def avatar(ctx, member: discord.Member):
    em = discord.Embed()
    em.set_image(url=f'{member.avatar_url}')
    await ctx.send(embed=em)

@bot.command()
async def userinfo(ctx, member: discord.Member):
    display = member.name
    discrim = member.discriminator
    name = f'{display}#{discrim}'
    joindate = f'{member.joined_at.day}-{member.joined_at.month}-{member.joined_at.year}'
    joined = f'{joindate}, {member.joined_at.hour}:{member.joined_at.minute}'
    createddate = f'{member.created_at.day}-{member.created_at.month}-{member.created_at.year}'
    created = f'{createddate}, {member.created_at.hour}:{member.created_at.minute}'

    em = discord.Embed(title='userinfo', colour=0x89cff0)
    em.set_thumbnail(url=member.avatar_url)
    em.add_field(name='Name:', value=name, inline=False)
    em.add_field(name='Nickname:', value=member.nick, inline=False)
    em.add_field(name='Status:', value=member.status, inline=False)
    em.add_field(name='Created at:', value=created, inline=False)
    em.add_field(name='Joined at:', value=joined, inline=False)
    em.add_field(name='Roles:', value=', '.join(r.name if r.name == '@everyone' else r.mention for r in sorted(member.roles, key=str)), inline=False)
    await ctx.send(embed=em)

@bot.command()
async def dm(ctx, member: discord.Member, *, words):
    await member.send(words)

@bot.command()
async def say(ctx, *, words):
  await ctx.send(words)
  await ctx.message.delete()

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    serverdate = f'{guild.created_at.day}-{guild.created_at.month}-{guild.created_at.year}'
    servercreated = f'{serverdate}, {guild.created_at.hour}:{guild.created_at.minute}'

    em = discord.Embed(title=f'{guild.name}', colour=0xFF69B4)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name='Server Name:', value=guild.name, inline=True)
    em.add_field(name='server Owner:', value=guild.owner, inline=True)
    em.add_field(name='Server Region:', value=guild.region, inline=True)
    em.add_field(name='Server created:', value=servercreated, inline=True)
    em.add_field(name='Members:', value=guild.member_count, inline=False)
    em.add_field(name='Roles:', value=', '.join(r.name if r.name == '@everyone' else r.mention for r in sorted(guild.roles, key=str)), inline=False)
    await ctx.send(embed=em)

@bot.command()
async def apistats(ctx):
    async with aiohttp.request('get', 'https://status.discordapp.com/api/v2/status.json') as resp:
        json_data = await resp.json()

    status = json_data['status']
    description = status['description']

    await ctx.send(description)

@bot.command()
async def iss(ctx):
    async with aiohttp.request('get', 'https://api.wheretheiss.at/v1/satellites/25544') as resp:
        iss_data = await resp.json()

    visibility = iss_data['visibility']
    id = iss_data['id']
    latitude = iss_data['latitude']
    timestamp = iss_data['timestamp']

    em = discord.Embed(title='International Space Station', colour=0xffffffff)
    em.add_field(name='Visibility', value=visibility, inline=False)
    em.add_field(name='Id', value=id, inline=False )
    em.add_field(name='Latitude', value=latitude, inline=False)
    em.add_field(name='Timestamp', value=timestamp, inline=False)
    await ctx.send(embed=em)

bot.run(os.environ['TOKEN'])

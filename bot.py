import discord
import asyncio
import os
import aiohttp
import collections
from discord.ext import commands

bot = commands.Bot(description='', command_prefix=commands.when_mentioned_or('!!'), pm_help=False, case_insensitive=True)

#This is an event.
@bot.event
async def on_ready():
    print('Ready sir *salutes*')
    await bot.change_presence(activity=discord.Game(name='as a beautiful pony in roboland (Help: !!help)'))
    bot.load_extension('dave_Repl')

MAX_BEFORE_SPAM = 4
TIMEOUT = 5.0
bins = collections.defaultdict(lambda: 0)

@bot.listen()
async def on_message(message):
    guild =  message.guild
    user = message.author
    if user is guild.owner:
        return
    if bins[user] > MAX_BEFORE_SPAM:
        return await user.send(f'HEY! You are sending message way too quick in ``{guild.name}``! Stop that!')
        return await message.delete()
    else:
        bins[user] += 1
        await asyncio.sleep(TIMEOUT)
        bins[user] -= 1

bot.remove_command('help')

def has_role (role_name, obj):
    return any(role_name == role.name.lower() for role in obj.roles)

#help commands

@bot.command()
async def help(ctx):
    em = discord.Embed(tile='Robert help desk', colour=0xADD8E6)
    em.set_author(name='Prefix= !! (this is not changable)')
    em.set_footer(text='Robert created by zOmbie1919nl')
    em.add_field(name='Moderations commands', value='Type !!mhelp to see all moderation commands', inline=False)
    em.add_field(name='Information commands', value='Type !!ihelp too see all information commands', inline=False)
    em.add_field(name='Other commands', value='Type !!chelp too see all other commands', inline=False )
    em.add_field(name='Help desk', value='Type !!helpdeks to get addintional information', inline=False)
    em.add_field(name='**note**', value='Keep in mind that the bot is still in development', inline=False)
    await ctx.send(embed=em)

@bot.command()
async def mhelp(ctx):
    author = ctx.author
    em = discord.Embed(title='Moderation commands', colour=0xADD8E6)
    em.set_footer(text='!!help for more help otions')
    em.add_field(name='Kick', value='***Kicks a user*** \n example: \n !!kick [user] [reason] \n !!kick @John being a bad boy!', inline=False)
    em.add_field(name='Ban', value='***Bans a user*** \n example: \n !!ban [user] [reason] \n !!ban @John not giving me food', inline=False)
    em.add_field(name='Clear', value='***Clears the amount of message you\'ve put in*** \n example: \n !!clear 40', inline=False)
    em.add_field(name='Giverole', value='***Give a role to a user*** \n example \n !!giverole @John Plebian', inline=False)
    await author.send(embed=em)
    await ctx.send(f'{author.mention} I\'ve sent all the information to your direct messages!')

@bot.command()
async def ihelp(ctx):
    author = ctx.author
    em = discord.Embed(title='Information commands', colour=0xADD8E6)
    em.set_footer(text='!!help for more help otions')
    em.add_field(name='Joined', value='***Shows you the date when a member joined*** \n example: \n !!joined [user] \n !!Joined @John', inline=False)
    em.add_field(name='Avatar', value='***Gives an enlarged profile picture of a user*** \n example: \n !!avatar [user] \n !!avatar @John', inline=False)
    em.add_field(name='Serverinfo', value='***Shows you some server information***', inline=False)
    em.add_field(name='Userinfo', value='***Shows you some information from a user*** \n example: \n !!userinfo [user] \n !!userinfo @John', inline=False)
    await author.send(embed=em)
    await ctx.send(f'{author.mention} I\'ve sent all the information to your direct messages!')

@bot.command()
async def chelp(ctx):
    author = ctx.author
    em = discord.Embed(title='Other commands', colour=0xADD8E6)
    em.set_footer(text='!!help for more help otions')
    em.add_field(name='DM', value='***Sends a direct message to a user*** \n example: \n !!dm [user] [message] \n !!dm @john Hey honey', inline=False)
    em.add_field(name='Say', value='***Sends a message in the chat*** \n example: \n !!say [message] \n !!say Cookiedough or cakebatter?', inline=False)
    em.add_field(name='Roles', value='***Shows you all the roles the server has***', inline=False)
    em.add_field(name='Apistats', value='***Shows you what the status is from the Discord API*** \n *note:that when the Api is down, the bots are down too, so it won\'t respond*', inline=False)
    em.add_field(name='Boop', value='***boops a user for you*** \n example: \n !!boop [user] \n !!boop @John', inline=False)
    await author.send(embed=em)
    await ctx.send(f'{author.mention} I\'ve sent all the information to your direct messages!')

@bot.command()
async def helpdesk(ctx):
    author = ctx.author
    em = discord.Embed(title='Help desk', colour=0xADD8E6)
    em.add_field(name='Discord Help Desk', value='https://discord.gg/W4B7g9m', inline=True)
    await author.send(embed=em)

#mod commands

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def joined(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send('Please give me a name to work with!')
    else:
        joindate = f'{member.joined_at.day}-{member.joined_at.month}-{member.joined_at.year}'
        joined = f'{joindate}, {str(member.joined_at.time())[:-10]}'
        return await ctx.send(f'{member.name} joined at {joined}')

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    serverdate = f'{guild.created_at.day}-{guild.created_at.month}-{guild.created_at.year}'
    servercreated = f'{serverdate}, {str(guild.created_at.time())[:-10]}'

    em = discord.Embed(title=f'{guild.name}', colour=0xFF69B4)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name='Server Name:', value=guild.name, inline=True)
    em.add_field(name='server Owner:', value=guild.owner, inline=True)
    em.add_field(name='Server Region:', value=guild.region, inline=True)
    em.add_field(name='Server created:', value=servercreated, inline=True)
    em.add_field(name='Members:', value=guild.member_count, inline=False)
    em.add_field(name='Roles:', value=', '.join(r.name if r.name == '@everyone' else r.mention for r in sorted(guild.roles, key=str)), inline=False)
    await ctx.send(embed=em)

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send('Please give me a name to work with!')
    else:
        display = member.name
        discrim = member.discriminator
        name = f'{display}#{discrim}'
        joindate = f'{member.joined_at.day}-{member.joined_at.month}-{member.joined_at.year}'
        joined = f'{joindate}, {str(member.joined_at.time())[:-10]}'
        createddate = f'{member.created_at.day}-{member.created_at.month}-{member.created_at.year}'
        created = f'{createddate}, {str(member.created_at.time())[:-10]}'
        em = discord.Embed(title='userinfo', colour=0xFF69B4)
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name='Name:', value=name, inline=False)
        em.add_field(name='Nickname:', value=member.nick, inline=False)
        em.add_field(name='User id', value=member.id, inline=False)
        em.add_field(name='Status:', value=member.status, inline=False)
        em.add_field(name='Created at:', value=created, inline=False)
        em.add_field(name='Joined at:', value=joined, inline=False)
        em.add_field(name='Roles:', value='\n '.join(r.name if r.name == '@everyone' else r.mention for r in sorted(member.roles, key=str)), inline=False)
        return await ctx.send(embed=em)

@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, member: discord.Member=None, *, reason=None):
    guild = ctx.guild
    if member is None:
        em = discord.Embed(colour=0xff0000)
        em.add_field(name='kick [user] [reason]', value='**user** refers to the user you are wanting to kick \n **reason** refers to the reason for the kick \n **example** !!kick @John being mean!', inline=False)
        return await ctx.send(embed=em)
        if reason is None:
            return await ctx.send('Please give the kick a reason')
    if member is guild.owner:
        return await ctx.send('I cannot kick the server owner sadly')
    else:
        person = member.mention
        em = discord.Embed(title='kick [user] [reason]', colour=0xff0000)
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name='Member:', value=person, inline=False)
        em.add_field(name='Reason:', value=reason, inline=False)
        await ctx.send(embed=em)
        await member.send(f'You have been kicked from {guild.name} for: {reason}')
        await member.kick(reason=reason)

@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, member: discord.Member=None, *, reason=None):
    guild = ctx.guild
    if member is guild.owner:
        return await ctx.send(f'I\'m not gonna ban my buddy {member.mention}')
    if member is None:
        em = discord.Embed(colour=0xff0000)
        em.add_field(name='ban [user] [reason]', value='**user** refers to the user you are wanting to ban \n **reason** refers to the reason of the ban\n **example** !!ban @John Trashtalking my new panda bear')
        return await ctx.send(embed=em)
    if reason is None:
        return await ctx.send('Please put in a reason')
    else:
        person= member.mention
        em = discord.Embed(title='Member banned', clour=0xff0000)
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name='member', value=person, inline=False)
        em.add_field(name='reason', value=reason, inline=False)
        await ctx.send(embed=em)
        await member.send(f'You have been banned form {guild.name} for: {reason}')
        await member.ban(reason=reason)
        await ctx.message.delete()

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def avatar(ctx, member: discord.Member=None):
    if member is None:
        await ctx.send('Please give me a name to work with!')
    else:
        em = discord.Embed()
        em.set_image(url=f'{member.avatar_url}')
        await ctx.send(embed=em)

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def dm(ctx, member: discord.Member=None, *, words=None):
    if member is None:
        return await ctx.send('Please give me a name to work with!')
    if words is None:
        return await ctx.send(f'I gladly want to send {member.name} a message, but I don\'t know what I need to tell them')
    else:
        author = ctx.author
        return await member.send(f'{author.name} wanted me to send you this: {words}')
        return await ctx.send('Message has been sent!')

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def say(ctx, *, words=None):
    if words is None:
        await ctx.send('You want me to say something, but you also want me to say nothing, yeaaah we might have a problem here.')
    else:
        await ctx.send(words)
        await ctx.message.delete()

@commands.has_permissions(manage_messages=True)
@bot.command()
async def clear(ctx, amount: int=None):
    if amount is None:
        await ctx.send('Please put in a value for me to clear!')
    else:
        clear = amount +1
        if amount > 100:
            await ctx.send('I cannot clear more that 100 messages at a time!')
        await ctx.channel.purge(limit=clear)
        await ctx.send(f'``{amount}`` message(s) has been cleared', delete_after = 5)

@commands.has_permissions(manage_roles=True)
@bot.command()
async def roles(ctx):
    guild = ctx.guild
    em = discord.Embed(title='Roles')
    em.add_field(name='Roles:', value='\n '.join(r.name if r.name == '@everyone' else r.mention for r in sorted(guild.roles, key=str)), inline=False)
    await ctx.send(embed=em)

@commands.has_permissions(manage_roles=True)
@bot.command()
async def giverole(ctx, member: discord.Member=None, role: discord.Role=None):
    if member is None:
        return await ctx.send('Who am I supposed to give a role? And what role am I supposed to give them? :confused:')
    if role is None:
        return await ctx.send(f'What role am I supposed to give {member}? :confused:')
    else:
        await member.add_roles(role)
        await ctx.send(f'{member.name} has been given the **{role}** role.')

#other commands

@bot.command()
async def apistats(ctx):
    async with aiohttp.request('get', 'https://status.discordapp.com/api/v2/status.json') as resp:
        json_data = await resp.json()

    status = json_data['status']
    description = status['description']

    await ctx.send(description)

@bot.command()
async def boop(ctx, member: discord.Member=None):
    guild = ctx.guild
    author = ctx.author
    if member is None:
        return await ctx.send(f'Boop! {author.mention} you\'ve been booped by me!')
    else:
        return await ctx.send(f'Boop! {member.mention} you\'ve been booped by {author.mention}!')

bot.run(os.environ['TOKEN'])

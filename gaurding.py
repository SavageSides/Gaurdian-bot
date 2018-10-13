import discord
import json
import random
import time
import asyncio
import os
from discord.ext import commands
from datetime import datetime

def prefix(bot, message):
    with open("serverConfig.json") as f:
        prefixes = json.load(f)
    default_prefix = "-"
    id = message.server.id
    return prefixes.get(id, default_prefix)

client = commands.Bot(command_prefix=prefix)
client.remove_command("help")

@client.event
async def on_server_join(server):
    owner = server.owner
    embed = discord.Embed(color=0xff0251)
    embed.add_field(name=":wave: Supppp", value=f"Hey.. Thanks for adding me to **{server.name}**. I am a moderation bot! You can type -help for everything!", inline=False)
    await client.send_message(owner, embed=embed)
    
    
        
        
@client.event
async def on_ready():
    print("Loading...")
    print("Loagging in and ready to moderate")
    
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(color=0x4e09ff)
    embed.add_field(name="Moderation", value="**-kick @User** Kicks the user from the server \n **-ban @User** Bans the user from the server \n **-mute @User** Gives that user the muted role along with him not being able to talk \n **-unmute @User** Takes away the Muted role from the user allowing him to talk \n **-strike @User** Adds one strike the the user you have mentioned \n **-rmstrikes @User** Removes all of the users strikes \n **-strikes @User** Shows that current amount of strikes the user has \n **-unban User or ID** It will unban a certan user and if you jsut did **-unban** It would unban the first person on the list \n **-prefix <prefix>** Will set that prefix to my dictanary of commands \n **-purge <Amount>** It will clear the chat **P.S it can only clear [2, 100]**", inline=False)
    embed.add_field(name="Role Management", value="**-crole <Role Name>** Creates the role for your server \n **-drole <Role Name>** Deletes the role from your server \n **-addrole @User <Role Name>** Adds the role just like mute but it adds the name of the role to the user \n **-removerole @User <Role Name>** Removes the role you have said from the user you have mentioned \n **-rolecolor <Color> <Role Name>** Sets the color for that role for the role you have said", inline=False)
    embed.add_field(name="Misc", value="**-configs** Shows all of the current configuable commands I have at the moment \n **-stats** Shows all of my stats \n **-uptime** Shows you how long I have been awake \n **-poll** Will go step by step for you to make your dream poll", inline=False)
    embed.set_image(url="https://i.imgur.com/vXRfAd6.gif")
    await client.say(embed=embed)
    

@client.command()
async def configs():
    embed = discord.Embed(color=0xff05cf)
    embed.add_field(name="Gaurdian", value="Here is the list of working configs!")
    embed.add_field(name=":wave: Hellos", value="Set the hello message by doing **-setwelcome**", inline=False)
    embed.add_field(name=":door: Goodbyes", value="Sets the goodbye messages by doin **-setgoodbye**", inline=False)
    embed.add_field(name=":stars: Prefix", value="Sets your custom prefix! Do **-setprefix <prefix>**", inline=False)
    await client.say(embed=embed)

@client.command(name="prefix", pass_context=True)
async def prefix(ctx, new_prefix):
    with open("serverConfig.json", "r") as f:
        prefixes = json.load(f)
    author = ctx.message.author
    if await client.__has_voted(author.id):
        if ctx.message.author.server_permissions.manage_server:
            prefixes[ctx.message.server.id] = new_prefix
            embed = discord.Embed(color=0xff05cf)
            embed.add_field(name="Prefix changed...", value=f"``{new_prefix}``")
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Server```", inline=False)
            await client.say(embed=embed)
    await client.say("YOU HAVENT VOTED YET!")
    with open("serverConfig.json", "w") as f:
        json.dump(prefixes, f)
   
#Role Management

@client.command(pass_context=True)
async def crole(ctx, *, role = None):
    server = ctx.message.server
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            if role is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing some requirements for this command. ```A role name is a missing argument.```", inline=False)
                await client.say(embed=embed)
                return
            await client.create_role(server=server, name=role)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role was created.. **Read** Following Information")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: manage Roles```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There was an error. ```1. I don't have permissions to make roles```", inline=False)
        await client.say(embed=embed)
        
@client.command(pass_context=True)
async def drole(ctx, *, name = None):
    server = ctx.message.server
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            role = discord.utils.get(ctx.message.server.roles, name=name)
            if role is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value=f"There was a unknown error. ```Error: No role called; {name}```")
                await client.say(embed=embed)
                return
            if name is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing some requirements for this command. ```A role name is a missing argument.```", inline=False)
                await client.say(embed=embed)
                return
            await client.delete_role(server=server, role=role)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role was deleted.. **Read** Following Information")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Roles```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There was an error. ```1. I don't have permissions to make roles```", inline=False)
        await client.say(embed=embed)
        
@client.command(pass_context=True)
async def addrole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            role = discord.utils.get(ctx.message.server.roles, name=name)
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing some arguments. ```User is a required argument..```", inline=False)
                embed.set_footer(text=f"Error Created by: {author.name}")
                await client.say(embed=embed)
                return
            if role is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value=f"There was a unknown error. ```Error: No role called; {name}```")
                await client.say(embed=embed)
                return
            await client.add_roles(user, role)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role was added.. **Read** Following Information")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Roles```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There was an error. ```1. I don't have permissions to add roles```", inline=False)
        await client.say(embed=embed)
        
@client.command(pass_context=True)
async def removerole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            role = discord.utils.get(ctx.message.server.roles, name=name)
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing some arguments. ```User is a required argument..```", inline=False)
                embed.set_footer(text=f"Error Created by: {author.name}")
                await client.say(embed=embed)
                return
            if role is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value=f"There was a unknown error. ```Error: No role called; {name}```")
                await client.say(embed=embed)
                return
            await client.remove_roles(user, role)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role was removed.. **Read** Following Information")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Roles```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There was an error. ```1. I don't have permissions to add roles```", inline=False)
        await client.say(embed=embed)
        
@client.command(pass_context=True, no_pm=True)
async def rolecolor(ctx, colour : discord.Colour = None, *, name = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.manage_roles:
            roles = discord.utils.get(ctx.message.server.roles, name=name)
            if roles is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value=f"There was a unknown error. ```Error: No role called; {name}```")
                await client.say(embed=embed)
                return
            if colour is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value=f"There was a unknown error. ```Error: Define a Colour```")
                await client.say(embed=embed)
                return
            await client.edit_role(ctx.message.server, roles, colour=colour)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role was edited.. **Read** Following Information")
            embed.add_field(name="Role:", value=f"{roles}", inline=False)
            embed.add_field(name="Colour:", value=f"{colour}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Roles```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There was an error. ```1. I don't have permissions to Change Roles```", inline=False)
        await client.say(embed=embed)
                
    
            
            
#Lines Below Are all Other Moderation


@client.command(pass_context=True, hidden=True)
@commands.has_role("Savage")
async def debug(ctx, *, code : str):
    """Evaluates code."""
    code = code.strip('` ')
    python = '```py\n{}\n```'
    result = None

    try:
        result = eval(code)
    except Exception as e:
        await client.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    if asyncio.iscoroutine(result):
        result = await result

    await client.say(python.format(result))



@client.command(pass_context=True)
async def kick(ctx, user: discord.Member = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.kick_members:
            if ctx.message.author.bot:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":white_check_mark: Sucessful!", value="Haha. You thought, next time don't use a bot to try to kick!")
                await client.say(embed=embed)
                return
            if author == user:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="Please use common sense. ```Error: Kicking your self is unwise.```", inline=False)
                await client.say(embed=embed)
                return
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing some arguments. ```User is a required argument..```", inline=False)
                embed.set_footer(text=f"Error Created by: {author.name}")
                await client.say(embed=embed)
                return
            await client.kick(user)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Member was kicked.. **Read** Following Information", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}")
            embed.add_field(name="User ID:", value=f"**{user.id}**")
            embed.set_footer(icon_url=user.avatar_url, text=f"Kicked by: {author.name}")
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Kick Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There are two things that could be wrong. ```1. I don't have permissions to kick members``` \n ```2. The user either has a higher role than me or higher permission```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, there was an unknown error... We will fix as soon as possible!")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def ban(ctx, user: discord.Member = None):
    author = ctx.message.author
    try:
        if ctx.message.author.server_permissions.ban_members:
            if ctx.message.author.bot:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":white_check_mark: Sucessful!", value="Haha. You thought, next time don't use a bot to try to ban!")
                await client.say(embed=embed)
                return
            if author == user:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="Please use common sense. ```Error: Banning your self is unwise.```", inline=False)
                await client.say(embed=embed)
                return
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing some arguments. ```User is a required argument..```", inline=False)
                embed.set_footer(text=f"Error Created by: {author.name}")
                await client.say(embed=embed)
                return
            await client.ban(user)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Member was banned.. **Read** Following Information", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}")
            embed.add_field(name="User ID:", value=f"**{user.id}**")
            embed.set_footer(icon_url=user.avatar_url, text=f"Kicked by: {author.name}")
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Ban Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="There are two things that could be wrong. ```1. I don't have permissions to ban members``` \n ```2. The user either has a higher role than me or higher permission```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, there was an unknown error... We will fix as soon as possible!")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def purge(ctx ,*, amount: int = None, limit=1000):
    try:
        if ctx.message.author.server_permissions.manage_messages:
            if amount is None:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error", value="You need some arguments to proceed. ```Amount is a required argument```")
                await client.say(embed=embed)
                return
            channel = ctx.message.channel
            author = ctx.message.author
            messages = []
            async for message in client.logs_from(channel, limit=int(amount)):
                messages.append(message)
            await client.delete_messages(messages)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Messages have been cleared.. **Read** Following Information")
            embed.add_field(name="Amount:", value=f"{amount}", inline=False)
            msg = await client.say(embed=embed)
            await asyncio.sleep(3)
            await client.delete_message(msg)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Ban Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="Well you need to check up with me. ```I don't have permissions to delete messages```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, there was an unknown error... We will fix as soon as possible!")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def mute(ctx, user: discord.Member = None):
    try:
        if ctx.message.author.server_permissions.mute_members:
            MutedRole = discord.utils.get(ctx.message.server.roles, name="Muted")
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error", value="You are missing some arguments. ```User is a required argument.```")
                await client.say(embed=embed)
                return
            if MutedRole is None:
                embed = discord.Embed(color=0xff0200)
                author = ctx.message.author
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing requirements. ```Requirements: Muted``` **Role**")
                await client.say(embed=embed)
                return
            await client.add_roles(user, MutedRole)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Member was muted.. **Read** Following Information")
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            embed.add_field(name="User ID:", value=f"{user.id}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Mute Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="Well you need to check up with me. ```I don't have permissions to mute members```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, there was an unknown error... We will fix as soon as possible!")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member = None):
    try:
        if ctx.message.author.server_permissions.mute_members:
            MutedRole = discord.utils.get(ctx.message.server.roles, name="Muted")
            if user is None:
                embed = discord.Embed(color=0xff0200)
                embed.add_field(name=":x: Error", value="You are missing some arguments. ```User is a required argument.```")
                await client.say(embed=embed)
                return
            if MutedRole is None:
                embed = discord.Embed(color=0xff0200)
                author = ctx.message.author
                embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
                embed.add_field(name=":x: Error", value="You are missing requirements. ```Requirements: Muted``` **Role**")
                await client.say(embed=embed)
                return
            await client.remove_roles(user, MutedRole)
            embed = discord.Embed(color=0x4e09ff)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Member was unmuted.. **Read** Following Information")
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            embed.add_field(name="User ID:", value=f"{user.id}", inline=False)
            await client.say(embed=embed)
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Mute Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="Well you need to check up with me. ```I don't have permissions to unmute members```", inline=False)
        await client.say(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(color=0xff0200)
        embed.add_field(name=":x: Error", value="Sorry, there was an unknown error... We will fix as soon as possible!")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def strike(ctx, member: discord.Member):
    with open("warnings.json", "r") as f:
        warnings = json.load(f)
    author = ctx.message.author
    if ctx.message.author.server_permissions.mute_members:
        if author == member:
            await client.say("You can't warn your self!")
            return
        if not ctx.message.server.id in warnings:
            warnings[ctx.message.server.id] = {}
        if not member.id in warnings[ctx.message.server.id]:
            warnings[ctx.message.server.id][member.id] = 0
        warnings[ctx.message.server.id][member.id] += 1
        embed = discord.Embed(color=0x4e09ff)
        embed.add_field(name=":warning: Striked", value=f"I have striked {member.mention}")
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Mute Members```", inline=False)
        await client.say(embed=embed)
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

@client.command(pass_context=True)
async def rmstrikes(ctx, member: discord.Member):
    with open("warnings.json", "r") as f:
        warnings = json.load(f)
    author = ctx.message.author
    warns = warnings[ctx.message.server.id][member.id]
    if ctx.message.author.server_permissions.mute_members:
        if warnings[ctx.message.server.id][member.id] == 0:
            embed = discord.Embed(color=0xff0200)
            embed.add_field(name=":x: Error", value=f"Something went wrong here is the error. ```{member.name} doesn't have any strikes```")
            await client.say(embed=embed)
            return
        if not ctx.message.server.id in warnings:
            warnings[ctx.message.server.id] = {}
        if not member.id in warnings[ctx.message.server.id]:
            warnings[ctx.message.server.id][member.id] = 0
        warnings[ctx.message.server.id][member.id] -= warns
        embed = discord.Embed(color=0x4e09ff)
        embed.add_field(name=":warning: Removed Strikes", value=f"Removed {member.mention}'s strikes.")
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Mute Members```", inline=False)
        await client.say(embed=embed)
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

@client.command(pass_context=True)
async def strikes(ctx, member: discord.Member):
    with open("warnings.json", "r") as f:
        warnings = json.load(f)
    if not member.id in warnings[ctx.message.server.id]:
        warnings[ctx.message.server.id][member.id] = 0
    warns = warnings[ctx.message.server.id][member.id]
    embed = discord.Embed(color=0x4e09ff)
    embed.add_field(name=":warning: Strikes", value=f"{member.mention} has {warns} strikes")
    await client.say(embed=embed)
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

@client.command(pass_context=True)
async def unban(ctx):
    ban_list = await client.get_bans(ctx.message.server)
    # Show banned users
    embed = discord.Embed(color=0x4e09ff)
    embed.set_author(name="Ban list:\n{}".format("\n".join([user.name for user in ban_list])))
    await client.say(embed=embed)
    # Unban last banned user
    if not ban_list:
        await client.say("Ban list is empty.")
        return
    try:
        if ctx.message.author.server_permissions.ban_members:
            await client.unban(ctx.message.server, ban_list[-1])
            await client.say("Unbanned user: `{}`".format(ban_list[-1].name))
        else:
            embed = discord.Embed(color=0xff0200)
            author = ctx.message.author
            embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
            embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Ban Members```", inline=False)
            await client.say(embed=embed)
    except discord.Forbidden:
        await client.say("I do not have permission to unban.")
        return
    except discord.HTTPException:
        await client.say("Unban failed.")
        return

@client.command(pass_context=True)
async def setwelcome(ctx, *, text = None):
    with open("server.json", "r") as f:
        welcome = json.load(f)
    if ctx.message.author.server_permissions.manage_server:
        if text is None:
            embed = discord.Embed(color=0xff0200)
            embed.add_field(name=":x: Error", value="Some requirements are needed. ```Welcome message is a required argument.```")
            await client.say(embed=embed)
            return
        if not ctx.message.server.id in welcome :
            welcome[ctx.message.server.id] = {}
            welcome[ctx.message.server.id]["welcome"] = "default"
        welcome[ctx.message.server.id]["welcome"] = text
        embed = discord.Embed(color=0x4e09ff)
        embed.add_field(name=":white_check_mark: | Set welcome to:", value=f"*{text}*", inline=True)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Server```", inline=False)
        await client.say(embed=embed)
    with open("server.json", "w") as f:
        json.dump(welcome,f)

@client.command(pass_context=True)
async def setgoodbye(ctx, *, text = None):
    with open("server.json", "r") as f:
        goodbye = json.load(f)
    if ctx.message.author.server_permissions.manage_server:
        if text is None:
            embed = discord.Embed(color=0xff0200)
            embed.add_field(name=":x: Error", value="Some requirements are needed. ```Goodbye message is a required argument.```")
            await client.say(embed=embed)
            return
        if not ctx.message.server.id in goodbye :
            goodbye[ctx.message.server.id] = {}
            goodbye[ctx.message.server.id]["goodbye"] = "default"
        goodbye[ctx.message.server.id]["goodbye"] = text
        embed = discord.Embed(color=0x4e09ff)
        embed.add_field(name=":white_check_mark: | Set goodbye to:", value=f"*{text}*", inline=True)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Server```", inline=False)
        await client.say(embed=embed)
    with open("server.json", "w") as f:
        json.dump(goodbye,f)

@client.command(pass_context=True)
async def setchannel(ctx, channel_name = None):
    with open("server.json", "r") as f:
        channel = json.load(f)
    if ctx.message.author.server_permissions.manage_server:
        if channel_name is None:
            embed = discord.Embed(color=0xff0200)
            embed.add_field(name=":x: Error", value="Some requirements are needed. ```Channel Name is a required argument.```")
            await client.say(embed=embed)
            return
        if not ctx.message.server.id in channel :
            channel[ctx.message.server.id] = {}
            channel[ctx.message.server.id]["channel"] = "default"
        channel[ctx.message.server.id]["channel"] = channel_name
        embed = discord.Embed(color=0x4e09ff)
        embed.add_field(name=":white_check_mark: | Set channel to:", value=f"*{channel_name}*", inline=True)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Server```", inline=False)
        await client.say(embed=embed)
    with open("server.json", "w") as f:
        json.dump(channel,f)

@client.event
async def on_member_join(member):
    with open("server.json", "r") as f:
        join = json.load(f)
    server = member.server
    welcomes = join[member.server.id]["welcome"]
    channels = join[member.server.id]["channel"]
    channel = discord.utils.get(server.channels, name=channels)
    await client.send_message(channel, f"{member.mention}, {welcomes}")
    with open("server.json", "w") as f:
        json.dump(join,f)

@client.event
async def on_member_remove(member):
    with open("server.json", "r") as f:
        bye = json.load(f)
    server = member.server
    goodbyess = bye[member.server.id]["goodbye"]
    channels = bye[member.server.id]["channel"]
    channel = discord.utils.get(server.channels, name=channels)
    await client.send_message(channel, f"{member.mention}, {goodbyess}")
    with open("server.json", "w") as f:
        json.dump(bye,f)

@client.command(pass_context=True)
async def poll(ctx):
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Title:", value="Please pick a topic.. Which is also known as the title.")
    await client.say(embed=embed)
    a = await client.wait_for_message(author=ctx.message.author)
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Sub Heading:", value="Please pick a sub heading.. Which is also known as the sub title.")
    await client.say(embed=embed)
    b = await client.wait_for_message(author=ctx.message.author)
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Message:", value="Please type in a paragraph-message for the poll.")
    await client.say(embed=embed)
    c = await client.wait_for_message(author=ctx.message.author)
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Channel:", value="Please pick a channel for the poll to go to..")
    await client.say(embed=embed)
    d = await client.wait_for_message(author=ctx.message.author)
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Posted", value="The poll has been posted.")
    await client.say(embed=embed)
    channel = discord.utils.get(ctx.message.server.channels, name=d.content)
    #Actual Poll Message
    embed = discord.Embed(color=0x0717f3)
    embed.title = f"{a.content}"
    embed.add_field(name=f"{b.content}", value=f"{c.content}")
    msg = await client.send_message(channel, embed=embed)
    await client.add_reaction(msg, "\U00002705")
    await client.add_reaction(msg, "\U0000274c")

@client.command(pass_context=True)
async def uptime(ctx):
    now = datetime.utcnow()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Gaurdian Uptime", value=f"• I've been online for **{elapsed.days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def stats(ctx):
    now = datetime.utcnow()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(color=0x0717f3)
    embed.add_field(name="Discord", value=f"• Watching **{len(client.servers)}** servers \n • Hosting **{len(set(client.get_all_members()))}** users")
    embed.add_field(name=":thinking: Others", value=f"• Been Online for **{elapsed.days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds", inline=False)
    await client.say(embed=embed)
    

starttime = datetime.utcnow()  
client.run(os.environ.get("TOKEN"))              

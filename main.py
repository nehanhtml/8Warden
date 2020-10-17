import discord
import random
from discord.ext import commands, tasks
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from itertools import cycle
import asyncio

status = cycle(['.h for list of commands', 'Bug ? DM tahlil#3239',])

# command prefix
client = commands.Bot(command_prefix = ">")


# start
@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready')


# welcomer
@client.event
async def on_member_join(member):
	for channel in member.server.channels:
		if str(channel) == "general":
			await client.send_message(f"""Welcome to the server {member.mention} """)

# status loop
@tasks.loop(seconds = 3)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))

# bad word checker
with open('dushtuwords.txt') as file:
	file = file.read().split()

@client.event
async def on_message(message):
	for badword in file:
		if badword in message.content.lower():
			await message.delete()
			await message.channel.send(f'{message.author.mention}! Racial Slurs and excessive bad words are not allowed !')
		else:
			await client.process_commands(message)


# mute
@client.command()
@has_permissions(manage_roles=True, ban_members=True, manage_messages=True)
async def mute(ctx, member : discord.Member): 
	guild = ctx.guild
	
	for role in guild.roles:
		if role.name == "Muted":
			await member.add_roles(role)
			await ctx.send("{} has been muted".format(member.mention, ctx.author.mention))
			return
			
			overwrite = discord.PermissionOverwrite(send_message=False)
			newRole = await guild.create_role(name="Muted")

			for channel in guild.text_channels:
				await channel.set_permissions(newRole, overwrite=overwrite)
			
			await member.add_roles(newRole)
			await ctx.send("{} has been muted".format(member.mention, ctx.author.mention))
@mute.error
async def mute_error(error, ctx):
	if isinstance(error, MissingPermissions):
		await ctx.send(f'You do not have the necessary permissions.')
		return

# unmute
@client.command()
@has_permissions(manage_roles=True, ban_members=True, manage_messages=True)
async def unmute(ctx, member : discord.Member):
	guild = ctx.guild

	for role in guild.roles:
		if role.name == "Muted":
			await member.remove_roles(role)
			await ctx.send("{} has {} has been unmuted".format(member.mention,ctx.author.mention))
			return
@unmute.error
async def unmute_error(error, ctx):
	if isinstance(error, MissingPermissions):
		await ctx.send(f'You do not have the necessary permissions.')
		return
		

# kick 
@client.command()
@has_permissions(manage_roles=True, ban_members=True, manage_messages=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'Kicked {member.mention}')
@kick.error
async def kick_error(error, ctx):
	if isinstance(error, MissingPermissions):
		await ctx.send(f'You do not have the neccesarry permissions.')
		return


# ban
@client.command()
@has_permissions(manage_roles=True, ban_members=True, manage_messages=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}')
@ban.error
async def ban_error(error, ctx):
	if isinstance(error, MissingPermissions):
		await ctx.send(f'You do not have the neccesarry permissions.')
		return


# unban
@client.command()
@has_permissions(manage_roles=True, ban_members=True, manage_messages=True)
async def unban(ctx, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')\

	for ban_entry in banned_users: 
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator): 
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return
@unban.error
async def unban_error(error, ctx):
	if isinstance(error, MissingPermissions):
		await ctx.send(f'You do not have the neccesarry permissions.')
		return


# clear
@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount = 5):
	await ctx.channel.purge(limit=amount)


# help *gonna add more stuff after bot is finished*
@client.command(aliases = ['halp'])
async def h(ctx):
	await ctx.send(f'_USAGE_: \n`**8ball**: Use command "8ball" with "." prefix and ask a question \n**ping**: Use command "ping" with "." prefix to check latency')


# ping
@client.command(aliases = ['pIng','Ping', 'PiNg', 'pINg', 'pinG', 'PING', 'piNg', 'PIng', 'piNG', 'p'])
async def _ping(ctx):
	await ctx.send(f'{round(client.latency * 1000)}ms')


# 8ball
@client.command(aliases = ['8ball', 'eightball', 'EightBall', 'eightBall', 'Eightball','8b'])
async def _8ball(ctx, *, question):
	responses = [   'It is certain.',
			'It is decidedly so.',
			'Without a doubt.',
			'Yes definetly.',
			'You may rely on it.',
			'As i see it yes.',
			'Most likely.',
			'Outlook good.',
			'Yes.',
			'Sign points to yes.',
			'Reply hazy, try again.',
			'Ask again later.',
			'Better not tell you right now.',
			'Cannot predict.',
			'Concentrate and ask again.',
			'Dont count on it.',
			'My reply is no.',
			'My sources say no.',
			'Outlook is not so good.',
			'MMMMMMMMMMMMMMMMMMMMMMMMM.'   ]
	await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# author
@client.command()
async def author(ctx):
	await ctx.sent(f'Coded and developed by Tahlil (tahlil#3239)')


# version
@client.command(aliases = ['v'])
async def _version(ctx):
	await ctx.send(f'Warden Version 1.0')


# client id 
client.run('token go here uwu')
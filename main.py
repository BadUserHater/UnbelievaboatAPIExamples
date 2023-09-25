import discord
from discord.ext import commands
import random
import sys
import requests
import json
from unbelipy import UnbeliClient
import os
from dotenv import load_dotenv

with open('./config.json') as f:
  data = json.load(f)
  for c in data['botConfig']:
     print('Prefix: ' + c['prefix'])

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = c['prefix'], intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot Ready")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} Slash Commands successfully Synced")
    except Exception as e:
        print(e)

UNBELIEVABOAT_AUTH = os.environ.get("UNBELIEVABOATAPITOKEN")



@client.command()
async def help(ctx):
   embed = discord.Embed(title="MY COMMANDS LIST", description="help - This message", color=(16776960))
   embed.add_field(name="Unbelievaboat API Commands", value="top20ulb - Get the top 20 Unbeliveaboat leaderboard\ngetbalance - Get the balance of a user\npermissions - Check what permissions the bot has with the economy in your server\nresetbalance - Reset someones balance in your server\nsetcashbalance - Set someones cash balance to a certain amount\nsetbankbalance - Set someones bank balance to a certain amount\naddcashmoney - Add cash to someones balance\naddbankmoney - Add cash to someones back balance\nroulette - Take a chance to either earn or lose some money\ngetinventoryitems - Get a list of your inventory items for unbelievaboat", inline=False)
   await ctx.send(embed=embed)

@client.command()
async def top20ulb(ctx):
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/?sort=total&limit=20&page=1"
   headers = {"Accept": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.get(url, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Leaderboard", description=f"{response.text}", color=(16776960))
   await ctx.send(embed=embed)

@client.command()
async def getstoreitems(ctx):
   url = "https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/items?sort=id&limit=10&page=1"
   headers = {"accept": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.get(url, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Store items", description=f"{response.text}", color=(16776960))
   await ctx.send(embed=embed)

@client.command()
async def getinventoryitems(ctx):
   url = "https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.author.id}/inventory?sort=id&limit=10&page=1"
   headers = {"accept": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.get(url, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Items for {ctx.author.id}", description=f"{response.text}", color=(16776960))
   await ctx.send(embed=embed)

@client.command()
async def getbalance(ctx, member: discord.Member=None):
   if member is None:
      member = ctx.author
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{member.id}"
   headers = {"accept": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.get(url, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Balance for {member.name}", description=f"{response.text}", color=(16776960))
   await ctx.send(embed=embed)

@client.command()
async def permissions(ctx):
   url = f"https://unbelievaboat.com/api/v1/applications/@me/guilds/{ctx.guild.id}"
   headers = {"accept": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.get(url, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Server Permissions", description=f"{response.text}", color=(16776960))
   await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_guild=True)
async def resetbalance(ctx, member: discord.Member):
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{member.id}"
   payload = {"cash": 0, "bank": 0, "reason": "API Testing"}
   headers = {"accept": "application/json", "content-type": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.put(url, json=payload, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Balance Reset", description=f"I have successfully reset the Unbelievaboat balance for this server for {member.mention}", color=(16776960))
   embed.add_field(name="Json Response", value=f"{response.text}", inline=False)
   await ctx.send(embed=embed)

@resetbalance.error
async def resetbalance_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="You currently do not have the correct permissions to use this command. You need the **Manage Server** permission to use this command", color=(16711839))
      await ctx.send(embed=embed)
   if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="Please put in the correct arguments. resetbalance <usermention>", color=(16711839))
      await ctx.send(embed=embed)
   else:
      raise error

@client.command()
@commands.has_permissions(manage_guild=True)
async def setcashbalance(ctx, member: discord.Member, amount: int):
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{member.id}"
   payload = {"cash": f"{amount}", "reason": "API Testing"}
   headers = {"accept": "application/json", "content-type": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.put(url, json=payload, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Cash Add", description=f"I have successfully put in {amount} to {member.mention} Cash balance in Unbelievaboat", color=(16776960))
   embed.add_field(name="Json Response", value=f"{response.text}", inline=False)
   await ctx.send(embed=embed)

@setcashbalance.error
async def setcashbalance_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="You currently do not have the correct permissions to use this command. You need the **Manage Server** permission to use this command", color=(16711839))
      await ctx.send(embed=embed)
   if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="Please put in the correct arguments. setcashbalance <usermention> <amount>", color=(16711839))
      await ctx.send(embed=embed)
   else:
      raise error

@client.command()
@commands.has_permissions(manage_guild=True)
async def setbankbalance(ctx, member: discord.Member, amount: int):
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{member.id}"
   payload = {"bank": f"{amount}", "reason": "API Testing"}
   headers = {"accept": "application/json", "content-type": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.put(url, json=payload, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Bank Add", description=f"I have successfully put in {amount} to {member.mention} Bank balance in Unbelievaboat", color=(16776960))
   embed.add_field(name="Json Response", value=f"{response.text}", inline=False)
   await ctx.send(embed=embed)

@setbankbalance.error
async def setbankbalance_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="You currently do not have the correct permissions to use this command. You need the **Manage Server** permission to use this command", color=(16711839))
      await ctx.send(embed=embed)
   if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="Please put in the correct arguments. setbankbalance <usermention> <amount>", color=(16711839))
      await ctx.send(embed=embed)
   else:
      raise error

@client.command()
@commands.has_permissions(manage_guild=True)
async def addcashmoney(ctx, member: discord.Member, amount: int):
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{member.id}"
   payload = {"cash": f"{amount}", "reason": "API Testing"}
   headers = {"accept": "application/json", "content-type": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.patch(url, json=payload, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Bank Add", description=f"I have successfully put in {amount} to {member.mention} Bank balance in Unbelievaboat", color=(16776960))
   embed.add_field(name="Json Response", value=f"{response.text}", inline=False)
   await ctx.send(embed=embed)

@addcashmoney.error
async def addcashmoney_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="You currently do not have the correct permissions to use this command. You need the **Manage Server** permission to use this command", color=(16711839))
      await ctx.send(embed=embed)
   if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="Please put in the correct arguments. addcashmoney <usermention> <amount>", color=(16711839))
      await ctx.send(embed=embed)
   else:
      raise error

@client.command()
@commands.has_permissions(manage_guild=True)
async def addbankmoney(ctx, member: discord.Member, amount: int):
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{member.id}"
   payload = {"bank": f"{amount}", "reason": "API Testing"}
   headers = {"accept": "application/json", "content-type": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.patch(url, json=payload, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Bank Add", description=f"I have successfully put in {amount} to {member.mention} Bank balance in Unbelievaboat", color=(16776960))
   embed.add_field(name="Json Response", value=f"{response.text}", inline=False)
   await ctx.send(embed=embed)

@addbankmoney.error
async def addbankmoney_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="You currently do not have the correct permissions to use this command. You need the **Manage Server** permission to use this command", color=(16711839))
      await ctx.send(embed=embed)
   if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="SOMETHING WENT WRONG", description="Please put in the correct arguments. addbankmoney <usermention> <amount>", color=(16711839))
      await ctx.send(embed=embed)
   else:
      raise error

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def roulette(ctx):
   income = ["10000",
             "5000",
             "1000",
             "1000",
             "500",
             "500",
             "500",
             "500",
             "500",
             "100",
             "100",
             "100",
             "100",
             "100",
             "100",
             "100",
             "100",
             "100",
             "-250",
             "-250",
             "-250",
             "-250",
             "-250",
             "-1000",
             "-1000",]
   url = f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.author.id}"
   payload = {"bank": f"{random.choice(income)}", "reason": "API Testing"}
   headers = {"accept": "application/json", "content-type": "application/json", "Authorization": UNBELIEVABOAT_AUTH}
   response = requests.patch(url, json=payload, headers=headers)
   embed = discord.Embed(title=f"{ctx.guild.name} Unbelievaboat Roulette", description="{ctx.author.mention} took a chance at the Roulette. You have earned {income} in Bank balance in Unbelievaboat", color=(16776960))
   embed.add_field(name="Json Response", value=f"{response.text}", inline=False)
   await ctx.send(embed=embed)

@roulette.error
async def roulette_error(ctx, error):
   if isinstance(error, commands.CommandOnCooldown):
      await ctx.send("This command has a 30 second cooldown and you are currently in the cooldown. Please try again later.")





TOKEN = os.getenv("BOTTOKEN")
client.run(TOKEN)

import discord
from discord.ext.commands import Bot
from discord.ext import commands

Client = discord.Client()

bot_prefix = "&&"

client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    print("Bot online")
    print("Name:", client.user.name)
    print("ID:", client.user.id)

@client.command(pass_context=True)
async def ToggleSwitch(ctx):
    global theSwitch
    theSwitch = not theSwitch

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.id == "xxxxx" and theSwitch == True:
        await client.send_message(message.channel, "Switch is on and xxxxx said something")
from src.utils import *
from src.commands import commands

import discord

client = discord.Client()

with open("token.txt", "r") as file:
    token = file.read()

@client.event
async def on_ready():
    print('Connection en tant que '+client.user.name)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author == client.user:
        return

    if message.content.startswith(config["prefix"]):
        for c in commands:
            if message.content.startswith(config["prefix"]+c):
                args = message.content.replace(config["prefix"]+c, "")
                if args != "":
                    args = list(args)
                    del args[0]
                    args = "".join(args)
                result = commands[c](args)
                for action in result:
                    actionType = action[0]
                    actionArgs = action[1]

                    if actionType == "message":
                        await message.channel.send(actionArgs)
                    if actionType == "react":
                        await message.add_reaction(actionArgs)
                    if actionType == "embed":
                        embed = discord.Embed(title=actionArgs[1], description=actionArgs[2])
                        embed.set_author(name=actionArgs[0])
                        embed.set_footer(text=actionArgs[3])
                        await message.channel.send(embed=embed)

client.run(token)
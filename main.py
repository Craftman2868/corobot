from src.utils import *
from src.commands import commands

import discord

client = discord.Client()

with open("token.txt", "r") as file:
    token = file.read()

@client.event
async def on_ready():
    activity = discord.Activity(name="$help !", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Connection en tant que '+client.user.name)

@client.event
async def on_message(message):
    global connection
    if message.author.bot:
        return

    if message.author == client.user:
        return

    msg = message.content.lower()
    if msg.startswith(config["prefix"]):
        # if msg.startswith(config["prefix"]+"say "):
        #     args = msg.replace(config["prefix"]+"say ", "").split(" ")
        #     try:
        #         channel = client.get_channel(int(args[1]))
        #     except IndexError:
        #         try:
        #             connection
        #         except NameError:
        #             await message.channel.send(":x: Merci de préciser le channel pour la première connection")
        #             await message.add_reaction("❌")
        #             return
        #     else:
        #         if channel == None:
        #             await message.channel.send(":x: Merci de rentré un id correcte")
        #             await message.add_reaction("❌")
        #             return
        #         try:
        #             connection
        #         except NameError:
        #             connection = await channel.connect()
        #         else:
        #             await connection.move_to(channel)
        #     try:
        #         toSay = sayNumber(int(args[0]))
        #     except ValueError:
        #         await message.channel.send(":x: Nombre invalide")
        #         await message.add_reaction("❌")
        #     for n in toSay:
        #         while True:
        #             try:
        #                 connection.play(discord.FFmpegPCMAudio("assets/enregistrements/"+str(n)+".mp3"))
        #             except discord.errors.ClientException:
        #                 continue
        #             else:
        #                 print(n)
        #                 break
        #     return
        # if msg.startswith(config["prefix"]+"disconnect ") or msg == config["prefix"]+"disconnect":
        #     try:
        #         await connection.disconnect()
        #     except NameError:
        #         await message.channel.send(":x: Je ne peut pas me déconnecter si je ne suis pas connecté")
        #         await message.add_reaction("❌")
        #     else:
        #         del connection
        for c in commands:
            print("'"+msg+"' '"+config["prefix"]+c+" '")
            if msg.startswith(config["prefix"]+c+" ") or msg == config["prefix"]+c:
                args = msg.replace(config["prefix"]+c, "")
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
                    if actionType == "say":
                        print(result)
                        channel = None
                        for g in client.guilds:
                            m = g.get_member(message.author.id)
                            if m:
                                channel = m.voice
                                if channel:
                                    channel = channel.channel
                                    try:
                                        connection
                                    except NameError:
                                        connection = await channel.connect()
                                    else:
                                        await connection.move_to(channel)
                                break
                            else:
                                continue
                        if not channel:
                            await message.channel.send(":x: Merci de vous connecter à un channel vocal avant d'executer cette commande")
                            await message.add_reaction("❌")
                            return
                        toSay = actionArgs
                        for word in toSay:
                            while True:
                                try:
                                    connection.play(discord.FFmpegPCMAudio("assets/enregistrements/"+str(word)+".mp3"))
                                except discord.errors.ClientException:
                                    continue
                                else:
                                    print(word)
                                    break
                    if actionType == "exit":
                        await client.logout()

client.run(token)
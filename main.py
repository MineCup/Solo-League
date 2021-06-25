from discord import Client, Intents, Embed
from config import *
from aiohttp import ClientSession
from datetime import datetime
from random import randint


async def fight_random(slp, members, message):
    premium = []
    for i in range(len(members)):
        if slp in members[i].roles:
            premium.append(i)
    if premium:
        if len(premium) == 1:
            cap1 = members[premium[0]]
            cap2 = members[randint(0, len(members) - 1)]
            while cap2 == cap1:
                cap2 = members[premium[randint(0, len(premium) - 1)]]
        else:
            cap1 = members[premium[randint(0, len(premium) - 1)]]
            cap2 = members[premium[randint(0, len(premium) - 1)]]
            while cap2 == cap1:
                cap2 = members[premium[randint(0, len(premium) - 1)]]
    else:
        cap1 = members[randint(0, len(members) - 1)]
        cap2 = members[randint(0, len(members) - 1)]
        while cap2 == cap1:
            cap2 = members[randint(0, len(members) - 1)]
    maps = await channel["map_pool"].fetch_message(messages["map_pool"])
    maps = maps.content.split("\n")
    emb = Embed(title="══₪ SOLO LEAGUE ₪══",
                description=f"""**⚔ Карта: {maps[randint(0, len(maps) - 1)]}
                🟥 Капитан: <@{cap1.id}>
                🟦 Капитан: <@{cap2.id}>
                👑 Ведущий: <@{message.author.id}>**""",
                color=3553599)
    await message.channel.send(embed=emb)


async def user_token(mes, user_api):
    async with ClientSession() as session:
        async with session.get(f"https://api.vimeworld.ru/misc/token/{user_api}") as response:
            pip = await response.json()
            if "Method not found" in pip:
                pass
            else:
                if not pip["valid"]:
                    pass
                else:
                    block = False
                    async for history in channel["login"].history(limit=500):
                        if pip["owner"]["username"] in history.embeds[0].description:
                            block = True
                        else:
                            pass
                    if not block:
                        nicknames_1 = await channel["nicks"].fetch_message(857290267845591050)
                        if pip["owner"]["username"].lower() in nicknames_1.content.lower():
                            await mes.author.add_roles(roles["login"], reason="Проверенный")
                        d = datetime.utcnow().strftime("%d/%m/%y")
                        emb = Embed(title="**Принят токен!**", colour=0x19253A)
                        emb.set_footer(text=f"{d}")
                        emb.set_thumbnail(
                            url=f"https://skin.vimeworld.ru/helm/3d/{pip['owner']['username']}.png")
                        dsc = f'**Пользователь:** {mes.author.mention}\n**Ник:** `{pip["owner"]["username"]}`\n' \
                              f'**Уровень:** `{pip["owner"]["level"]} [{int(pip["owner"]["levelPercentage"] * 100)}%]`\n' \
                              f'**Статус:** `{pip["owner"]["rank"]}`\n'
                        emb.description = dsc
                        await mes.channel.send(embed=emb)


class MyClient(Client):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.guilds = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print("Discordo!")
        guild = client.get_guild(guild_id)
        for chan in channel:
            channel[chan] = guild.get_channel(channel[chan])
        for role in roles:
            roles[role] = guild.get_role(roles[role])
        for role in enumerate(slwl):
            slwl[role[0]] = guild.get_role(role[1])

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel == channel["sl"] and message.content == "/fight":
            all_roles = set(list(slwl) + message.author.roles)
            if len(message.author.roles) + 3 == len(all_roles):
                members = message.author.voice.channel.members
                if len(members) == 9:
                    for i in range(len(members)):
                        if members[i] == message.author:
                            members.pop(i)
                            break
                    fight_random(roles["slp"], members, message)
                elif len(members) == 8:
                    fight_random(roles["slp"], members, message)

        if message.channel == channel["login"]:
            mes = message
            await message.delete()
            if "/" in mes.content:
                user_api = mes.content.split("/")[-1]
                await user_token(mes, user_api)
            else:
                user_api = mes.content
                await user_token(mes, user_api)

client = MyClient()
client.run(token["bot"])

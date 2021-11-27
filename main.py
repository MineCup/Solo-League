from discord import Client, Intents, Embed
from config import *
from aiohttp import ClientSession
from asyncio import sleep
from datetime import datetime
from random import randint
from table import table
from time import time

services = table()


async def fight_test(slp, members, message):
    members_id = []
    sostav = "\n**👤 Никнеймы участников:**"
    async for history in channel["login"].history(limit=2500):
        for mem in members:
            if str(mem.id) in history.embeds[0].description and str(mem.id) not in sostav:
                nickname = history.embeds[0].description.split("\n")[1].replace("Ник:", "").replace("`", "").replace(
                    "**", "")
                sostav += f'\n<@{mem.id}>** {nickname}**'
                members_id.append(mem.id)
                break

    await message.channel.send(sostav)


async def fight_random(slp, members, message):
    members_id = []
    sostav = "\n**👤 Никнеймы участников:**"
    async for history in channel["login"].history(limit=2500):
        for mem in members:
            if str(mem.id) in history.embeds[0].description and str(mem.id) not in sostav:
                nickname = history.embeds[0].description.split("\n")[1].replace("Ник:", "").replace("`", "").replace(
                    "**", "")
                sostav += f'\n<@{mem.id}>** {nickname}**'
                members_id.append(mem.id)
                break
    else:
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
                                                    👑 Ведущий: <@{message.author.id}>**{sostav}""",
                    color=3553599)
        await message.channel.send(embed=emb)


async def userToken(message, api):
    async with ClientSession() as session:
        async with session.get(f"https://api.vimeworld.ru/misc/token/{api}") as response:
            pip = await response.json()

            if "Method not found" in pip:
                dell = await message.channel.send(f'<@{message.author.id}> Некорректный токен')
                await dell.delete(delay=10)
                return

            if not pip["valid"]:
                dell = await message.channel.send(f'<@{message.author.id}> Некорректный токен')
                await dell.delete(delay=10)
                return

            nicknames = services["bot"].spreadsheets().values().get(
                spreadsheetId="1OaMpmMMFR_NIzmqtEh12XJ6N4X9R723S4g709FKvj_8",
                range=f'SOLO LEAGUE NICKNAMES!A1:A1000',
                majorDimension='COLUMNS').execute()

            if "values" not in nicknames:
                return

            async for history in channel["login"].history(limit=3500):
                try:
                    if pip["owner"]["username"] in history.embeds[0].description:
                        dell = await message.channel.send(f'Никнейм {pip["owner"]["username"]} уже зарегистрирован.')
                        await dell.delete(delay=10)
                        return
                except:
                    continue
                for name in nicknames["values"][0]:
                    if pip["owner"]["username"].lower() == name.lower().strip():
                        del nicknames
                        await message.author.add_roles(roles["login"], reason="Проверенный")

                        d = datetime.utcnow().strftime("%d/%m/%y")
                        emb = Embed(title="**Принят токен!**", colour=0x19253A)
                        emb.set_footer(text=d)
                        emb.set_thumbnail(url=f"https://skin.vimeworld.ru/helm/3d/{pip['owner']['username']}.png")

                        emb.description = f'**Пользователь:** {message.author.mention}\n' \
                                          f'**Ник:** `{pip["owner"]["username"]}`\n' \
                                          f'**Уровень:** `{pip["owner"]["level"]} [{int(pip["owner"]["levelPercentage"] * 100)}%]`\n' \
                                          f'**Статус:** `{pip["owner"]["rank"]}`'
                        await message.channel.send(embed=emb)
                        return
                dell = await message.channel.send(f'Никнейма {pip["owner"]["username"]} нет в таблице.')
                await dell.delete(delay=10)
                return
            return


class MyClient(Client):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.guilds = True
        intents.voice_states = True
        super().__init__(intents=intents)

    async def on_member_update(self, before, after):
        del before
        if roles["login"] not in after.roles:
            return
        await sleep(3)
        async for history in channel["login"].history(limit=3500):
            try:
                if str(after.id) in history.embeds[0].description:
                    return
            except:
                continue

        await after.remove_roles(roles["login"], reason="Добавление роли не через канал выдача-роли")
        print("чел добавил роль соло лиги не через бота")

    async def on_voice_state_update(self, member, before, after):
        del member, before, after
        async for event in client.get_guild(guild_id).audit_logs(limit=100):
            try:
                if event.action.name != "member_disconnect":
                    return
                for role in slwl:
                    if "Solo" in role.name:
                        await event.user.remove_roles(role, reason="Кик игрока.")
            except:
                continue

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
        if message.author == self.user or message.author.bot:
            return

        if message.channel == channel["sl"]:
            if message.content == "/fight":
                all_roles = set(list(slwl) + message.author.roles)
                if len(message.author.roles) + 3 != len(all_roles):
                    members = message.author.voice.channel.members
                    if len(members) == 9:
                        for i in range(len(members)):
                            if members[i] == message.author:
                                members.pop(i)
                                break
                        await fight_random(roles["slp"], members, message)
                    elif len(members) == 8:
                        await fight_random(roles["slp"], members, message)

        if message.channel == channel["login"] and message.author.id != 630858769630232586:
            await message.delete()
            if "/" in message.content:
                userApi = message.content.split("/")[-1]
                await userToken(message, userApi)
            else:
                userApi = message.content
                await userToken(message, userApi)

        if message.author.id == 630858769630232586 and message.content == "/2fight":
            members = message.author.voice.channel.members
            await fight_test(roles["slp"], members, message)


client = MyClient()
client.run(token["bot"])

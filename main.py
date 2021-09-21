from discord import Client, Intents, Embed
from config import *
from aiohttp import ClientSession
from asyncio import sleep
from datetime import datetime
from random import randint
from table import table

first_game = []
second_game = []

services = table()


async def fight_random(slp, members, message):
    members_id = []
    for mem in members:
        members_id.append(mem.id)
    print(members_id)
    print(first_game)
    print(second_game)
    if members_id in second_game:
        await message.channel.send("Игра не создана. Поменяйте состав.")
    else:
        if members_id in first_game:
            first_game.remove(members_id)
            second_game.append(members_id)
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
        else:
            block = False
            block2 = False
            for game2 in range(len(second_game)):
                counter = 0
                member_remember = []
                for member in range(len(members_id)):
                    if members_id[member] in second_game[game2]:
                        counter += 1
                        member_remember.append(members_id[member])
                if counter > 5:
                    block = True
                    await message.channel.send("Игра не создана. Поменяйте состав.")
                else:
                    for rem in member_remember:
                        second_game[game2].remove(rem)
            for game11 in range(len(first_game)):
                for game2 in range(len(second_game)):
                    if len(second_game[game2]) <= 4:
                        second_game.pop(game2)
                        break
            if not block:
                for game1 in range(len(first_game)):
                    counter = 0
                    member_remember = []
                    for member in range(len(members_id)):
                        if members_id[member] in first_game[game1]:
                            counter += 1
                            member_remember.append(members_id[member])
                    if counter > 5:
                        block2 = True
                        for ii in member_remember:
                            first_game[game1].remove(ii)
                        second_game.append(members_id)
                    else:
                        for rem in member_remember:
                            first_game[game1].remove(rem)
                for game11 in range(len(first_game)):
                    for game1 in range(len(first_game)):
                        if len(first_game[game1]) <= 4:
                            first_game.pop(game1)
                            break
                if not block2:
                    first_game.append(members_id)
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

            async for history in channel["login"].history(limit=500):
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
        async for history in channel["login"].history(limit=500):
            try:
                if str(after.id) in history.embeds[0].description:
                    return
            except:
                continue
                
        await after.remove_roles(roles["login"], reason="Добавление роли не через канал выдача-роли")
        print("Пидорас добавил роль соло лиги не через бота")

    async def on_voice_state_update(self, member, before, after):
        del member, before, after
        async for event in client.get_guild(guild_id).audit_logs(limit=100):
            if event.action.name != "member_disconnect":
                return
            for role in slwl:
                if "Solo" in role.name:
                    await event.user.remove_roles(role, reason="Кик игрока.")
        
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

        if message.channel == channel["login"]:
            await message.delete()
            if "/" in message.content:
                userApi = message.content.split("/")[-1]
                await userToken(message, userApi)
            else:
                userApi = message.content
                await userToken(message, userApi)


client = MyClient()
client.run(token["bot"])

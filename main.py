from discord import Client, Intents, Embed
from config import *
from aiohttp import ClientSession
from datetime import datetime
from random import randint

first_game = []
second_game = []


async def fight_random(slp, members, message):
    print("members:", members)
    print("1:", first_game)
    print("2", second_game)
    members_id = []
    for mem in members:
        members_id.append(mem.id)
    if members_id in second_game:
        await message.channel.send("Игра не создана. Поменяйте состав.")
    else:
        if members_id in first_game:
            first_game.remove(members_id)
            second_game.append(members_id)
        else:
            block = False
            block2 = False
            for game2 in range(len(second_game)):
                counter = 0
                member_remember = []
                for member in range(len(members_id)):
                    if second_game[game2]:
                        if members_id[member] in second_game[game2]:
                            counter += 1
                            member_remember.append(members_id[member])
                if counter > 5:
                    block = True
                    print(second_game[game2])
                    print(members_id)
                    await message.channel.send("Игра не создана. Поменяйте состав.")
                else:
                    for rem in member_remember:
                        second_game[game2].remove(rem)
                if len(second_game[game2]) == 4:
                    second_game.pop(game2)
            if not block:
                for game1 in range(len(first_game)):
                    counter = 0
                    member_remember = []
                    for member in range(len(members_id)):
                        if first_game[game1]:
                            if members_id[member] in first_game[game1]:
                                counter += 1
                                member_remember.append(members_id[member])
                    if counter > 5:
                        block2 = True
                        print(first_game[game1])
                        print(members_id)
                        first_game.remove(members_id)
                        second_game.append(members_id)
                    else:
                        for rem in member_remember:
                            first_game[game1].remove(rem)
                    if len(first_game[game1]) <= 4:
                        first_game.pop(game1)
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
                        nicknames_1 = await channel["nicks"].fetch_message(messages["nicknames"])
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
            mes = message
            await message.delete()
            if "/" in mes.content:
                user_api = mes.content.split("/")[-1]
                await user_token(mes, user_api)
            else:
                user_api = mes.content
                await user_token(mes, user_api)

        if message.content.startswith("*add") and message.channel == channel["nicks"]:
            new_nick = message.content[5:]
            for i in range(5):
                try:
                    mes = await channel["nicks"].fetch_message(messages["nicknames"])
                    await mes.edit(content=f"```{mes.content.replace('```', '')}{new_nick}\n```")
                    break
                except:
                    if i == 4:
                        await channel["nicks"].send("Не удалось изменить сообщение.")

        if message.content.startswith("*rem") and message.channel == channel["nicks"]:
            new_nick = message.content[5:]
            for i in range(5):
                try:
                    mes = await channel["nicks"].fetch_message(messages["nicknames"])
                    mes2 = mes.content.split("\n")
                    mes_new = ""
                    for m in mes2:
                        print(m)
                        if m.replace("\n", "").lower() != new_nick.lower() and m != "":
                            mes_new += m + "\n"
                    await mes.edit(content=mes_new)
                    break
                except:
                    if i == 4:
                        await channel["nicks"].send("Не удалось изменить сообщение.")


client = MyClient()
client.run(token["bot"])

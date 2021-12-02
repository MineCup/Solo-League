from discord import Client, Intents, Embed
from config import *
from aiohttp import ClientSession
from asyncio import sleep
from datetime import datetime
from random import randint
from table import table


async def randomize(members, message, is_one_premium=None):
    if is_one_premium:
        cap1 = is_one_premium
    else:
        cap1 = members[randint(0, len(members) - 1)]
    cap2 = members[randint(0, len(members) - 1)]
    while cap2 == cap1:
        cap2 = members[randint(0, len(members) - 1)]

    maps = await channel["map_pool"].fetch_message(messages["map_pool"])
    maps = maps.content.split("\n")

    sostav = await fight(members)

    emb = Embed(title="══₪ SOLO LEAGUE ₪══",
                description=f"""**⚔ Карта: {maps[randint(0, len(maps) - 1)]}
                                                        🟥 Капитан: <@{cap1.id}>
                                                        🟦 Капитан: <@{cap2.id}>
                                                        👑 Ведущий: <@{message.author.id}>**{sostav}""",
                color=3553599)
    await message.channel.send(embed=emb)


async def fight(members):
    total = 0
    sostav = "\n**👤 Никнеймы участников:**"
    async for history in channel["login"].history(limit=3500):
        if not history.content:
            for member in members:
                if str(member.id) in history.embeds[0].description and str(member.id) not in sostav:
                    nickname = history.embeds[0].description.split("\n")[1]
                    nickname = nickname.replace("Ник:", "").replace("`", "").replace("**", "")
                    sostav += f'\n<@{member.id}>** {nickname.strip()}**'
                    total += 1
                    break
        if len(members) == total:
            break
    return sostav


async def fight_random(slp, members, message):
    premium = []
    for i in range(len(members)):
        if slp in members[i].roles:
            premium.append(i)
    if premium:
        if len(premium) == 1:
            await randomize(members, message, premium[0])
        else:
            await randomize(premium, message)
    else:
        await randomize(members, message)


async def token_info(api):
    async with ClientSession() as session:
        async with session.get(f"https://api.vimeworld.ru/misc/token/{api}") as response:
            return await response.json()


async def user_check(user_info, message):
    nicknames = table()["bot"].spreadsheets().values().get(
        spreadsheetId="1OaMpmMMFR_NIzmqtEh12XJ6N4X9R723S4g709FKvj_8",
        range=f'SOLO LEAGUE NICKNAMES!A1:A2000',
        majorDimension='COLUMNS').execute()

    if "values" not in nicknames:
        dell = await message.channel.send(f'Таблица с никнеймами пуста. Обратитесь к <@630858769630232586>')
        await dell.delete(delay=10)
        return

    if user_info["owner"]["username"].lower() not in str(nicknames["values"][0]).lower():
        dell = await message.channel.send(f'Никнейма {user_info["owner"]["username"]} нет в таблице.')
        del nicknames
        await dell.delete(delay=10)
        return
    del nicknames

    if True in [True if not history.content and f'`{user_info["owner"]["username"]}`' in history.embeds[0].description
                else False
                for history in await message.channel.history(limit=3500).flatten()]:
        dell = await message.channel.send(f'Никнейм {user_info["owner"]["username"]} уже зарегистрирован.')
        await dell.delete(delay=10)
        return

    d = datetime.utcnow().strftime("%d/%m/%y")
    emb = Embed(title="**Принят токен!**", colour=0x19253A)
    emb.set_footer(text=d)
    emb.set_thumbnail(url=f"https://skin.vimeworld.ru/helm/3d/{user_info['owner']['username']}.png")

    emb.description = f'''**Пользователь:** {message.author.mention}
    **Ник:** `{user_info["owner"]["username"]}`
    **Уровень:** `{user_info["owner"]["level"]} [{int(user_info["owner"]["levelPercentage"] * 100)}%]`
    **Статус:** `{user_info["owner"]["rank"]}`'''
    await message.channel.send(embed=emb)

    await message.author.add_roles(roles["login"], reason="Проверенный")
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

        if message.guild:
            if message.channel == channel["login"]:
                await message.delete()
                answer = await token_info(message.content.split("/")[-1])
                if answer.get("error") is None and answer.get("valid"):
                    await user_check(answer, message)
                else:
                    dell = await message.channel.send(f'<@{message.author.id}> Некорректный токен')
                    await dell.delete(delay=10)
                    return

            if message.author.id == 630858769630232586 and message.content == "/testfight":
                members = message.author.voice.channel.members
                sostav = await fight(members)
                await message.channel.send(sostav)

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
                    else:
                        await message.channel.send(f"В вашем канале {len(members)} участников.\n"
                                                   f"/fight доступен при 8 и 9 участниках.")


client = MyClient()
client.run(token["bot"])

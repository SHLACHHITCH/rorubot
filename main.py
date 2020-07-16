import os

import discord
import steam
from discord.ext import commands
from steam import game_servers as gs

Bot = commands.Bot(
    command_prefix="!", activity=discord.Game(name="Welcome to Yong Army")
)

# SERVER STATUS

ADDR = r"\gameaddr\37.230.228.193:7778"
MAPS = (
    "TE-BakovkaB9",
    "TE-Odessa-V7",
    "TE-Bridges_of_Druzhina_MCP",
    "TE-Barracks",
    "TE-Coldsteel_MCP",
    "TE-Spartanovka",
    "TE-MyshkovaRiver_MCP",
    "TE-Stalingradkessel_MCP",
    "TE-MamayevKurgan",
    "TE-PavlovsHouse",
    "TE-Station",
    "TE-Butovo-B14",
    "TE-RedOctoberFactory",
    "TE-DerIwanBerg",
    "TE-CommissarsHouse",
    "TE-Apartments",
    "TE-Rakowice_MCP",
    "TE-Red_Assault_Final",
    "TE-GrainElevator",
    "TE-Zhytomir-B4",
    "TE-Univermag-B10",
    "TE-Kaukasus-V8",
    "TE-Tulaoutskirts_MCP",
    "TE-BakovkaB9",
)

COLORS = (
    15158332,
    15159868,
    15095867,
    15097403,
    15098939,
    15034938,
    15036218,
    15037754,
    14973754,
    14975289,
    14976825,
    14912825,
    14914360,
    14915896,
    14851896,
    14853431,
    14854711,
    14790711,
    14792247,
    14793782,
    14729782,
    14731318,
    14667317,
    14668597,
    14670133,
    14605877,
    14147124,
    13753908,
    13294900,
    12901683,
    12442931,
    12049459,
    11590707,
    11197234,
    10738482,
    10345266,
    9886258,
    9493041,
    9034289,
    8640817,
    8182065,
    7788592,
    7329840,
    6936624,
    6543152,
    6084399,
    5690927,
    5232175,
    4838959,
    4445486,
    3986734,
    3593262,
    3200046,
    3003441,
    3003191,
    3003197,
    3002947,
    3002953,
    3002703,
    3002453,
    3002202,
    3001952,
    3067494,
    3067243,
    3066993,
)


@Bot.command(aliases=['с'])
async def статус(ctx):
    try:
        server = next(gs.query_master(ADDR))
        if not (info := gs.a2s_info(server)):
            raise RuntimeError

        embed_dict = {
            "title": f'Статус __{info["name"]}__',
            "fields": [
                {"name": "Карта:", "value": info["map"], "inline": True},
                {
                    "name": "Игроки:",
                    "value": f"{info['players']}/{info['max_players']}",
                    "inline": True,
                },
                {
                    "name": "Следующая карта:",
                    "value": MAPS[1 + MAPS.index(info["map"])],
                    "inline": False,
                },
            ],
            "color": COLORS[min(info["players"], 64)],  # 64 is max players
        }
    except RuntimeError:
        embed_dict = {
            "title": "Произошла ошибка при получении данных о сервере",
            "description": "Пожалуйста, попробуйте ещё раз позднее.",
        }
    finally:
        embed = discord.Embed().from_dict(embed_dict)
        await ctx.channel.send(embed=embed)

@Bot.command(aliases=['s'])
async def status(ctx):
    try:
        server = next(gs.query_master(ADDR))
        if not (info := gs.a2s_info(server)):
            raise RuntimeError

        embed_dict = {
            "title": f'Status of __{info["name"]}__ ',
            "fields": [
                {"name": "Map:", "value": info["map"], "inline": True},
                {
                    "name": "Players:",
                    "value": f"{info['players']}/{info['max_players']}",
                    "inline": True,
                },
                {
                    "name": "Next map:",
                    "value": MAPS[1 + MAPS.index(info["map"])],
                    "inline": False,
                },
            ],
            "color": COLORS[min(info["players"], 64)],  # 64 is max players
        }
    except RuntimeError:
        embed_dict = {
            "title": "An error occurred while retrieving server information",
            "description": "Please try again later.",
        }
    finally:
        embed = discord.Embed().from_dict(embed_dict)
        await ctx.channel.send(embed=embed)

# WELCOME MESSAGE & ROLE GIVE

WELCOME_TITLE = ":flag_gb: Welcome to Discord server {member.guild.name}\n:flag_ru: Добро пожаловать на Discord сервер {member.guild.name}"
WELCOME_DESCRIPTION = ":flag_gb: There is a bot on our server that will help you find out the current and next map.\nFor technical issues please contact {bubb1e} or {tony}\n:flag_ru: На нашем сервере работает бот, который поможет Вам узнать текущую и следующую карту.\nПо техническим вопросам просьба обращаться к {bubb1e} или {tony}"  # and maybe shardeex..?
WELCOME_IMAGE = "ro2.jpg"

WELCOME_CHANNEL_ID = 728512405667315752
ROLE_ID = 719459081492103218


@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(WELCOME_CHANNEL_ID)
    ext = WELCOME_IMAGE.split(".")[-1]  # Расширение файла
    file = discord.File(WELCOME_IMAGE, filename=f"image.{ext}")

    # I know I should rewrite this
    b_id, t_id = 277060142879604737, 500705347766321153
    try:
        bubb1e = member.guild.get_member(b_id).mention
        tony = member.guild.get_member(t_id).mention
    except AttributeError:
        bubb1e = await Bot.fetch_user(b_id)
        bubb1e = bubb1e.name
        tony = await Bot.fetch_user(t_id)
        tony = tony.name

    embed = discord.Embed(
        title=WELCOME_TITLE.format(member=member),
        description=WELCOME_DESCRIPTION.format(member=member, bubb1e=bubb1e, tony=tony),
    ).set_image(url=f"attachment://image.{ext}")

    try:
        await channel.send(f"Привет, {member.mention}!", file=file, embed=embed)
    except discord.errors.Forbidden as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")

    if (role := member.guild.get_role(ROLE_ID)) :
        await member.add_roles(role)
    else:
        try:
            await member.send(
                f":flag_gb: Unfortunately, I could not give you a role on the server {member.guild.name}, because I could not find it.\n:flag_ru: К сожалению, мне не удалось выдать вам роль на сервере {member.guild.name}, так как я не смог её найти."
            )
        except discord.Forbidden:
            pass  # maybe I should tell bubb1e about this...


@Bot.event
async def on_ready():
    print("logged in.")


Bot.run(os.environ.get("BOT_TOKEN"))

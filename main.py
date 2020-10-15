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
    "TE-Bridges_of_Druzhina_MCP",
    "TE-Coldsteel_MCP",
    "TE-Spartanovka",
    "TE-MyshkovaRiver_MCP",
    "TE-Stalingradkessel_MCP",
    "TE-Butovo-B14",
    "TE-Barracks",
    "TE-RedOctoberFactory",
    "TE-Racowice_MCP",
    "TE-GrainElevator",
    "TE-PavlovsHouse",
    "TE-Apartments",
    "TE-Station",
    "TE-CommissarsHouse",
    "TE-DerIwanBerg",
    "TE-Univermag-B10",
    "TE-Kaukasus-V8",
    "TE-Zhytomir-B4",
    "TE-Tulaoutskirts_MCP",
    "TE-Winterwald_MCP",
    "TE-MamayevKurgan",
)
    
    
    
    
    
    
    
    
   
    
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


@Bot.event
async def on_ready():
    print("logged in.")


Bot.run(os.environ.get("BOT_TOKEN"))

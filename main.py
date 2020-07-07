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


@Bot.command()
async def статус(ctx):
    try:
        server = next(gs.query_master(ADDR))
        if not (info := gs.a2s_info(server)):
            raise RuntimeError

        embed_dict = {
            "title": "Статус сервера",
            "fields": [
                {"name": "Карта:", "value": info["map"], "inline": True},
                {
                    "name": "Игроки:",
                    "value": f"{info['players']}/{info['max_players']}",
                    "inline": True,
                },
            ],
        }
    except RuntimeError:
        embed_dict = {
            "title": "Произошла ошибка при получении данных о сервере",
            "description": "Пожалуйста, попробуйте ещё раз позднее.",
        }
    finally:
        embed = discord.Embed().from_dict(embed_dict)
        await ctx.channel.send(embed=embed)


@Bot.command()
async def status(ctx):
    try:
        server = next(gs.query_master(ADDR))
        if not (info := gs.a2s_info(server)):
            raise RuntimeError

        embed_dict = {
            "title": "Server status",
            "fields": [
                {"name": "Map:", "value": info["map"], "inline": True},
                {
                    "name": "Players:",
                    "value": f"{info['players']}/{info['max_players']}",
                    "inline": True,
                },
            ],
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

bubb1e_id, tony_id = 277060142879604737, 500705347766321153
WELCOME_TITLE = ":flag_gb: Welcome to Discord server {member.guild.name}, {member.mention}\n:flag_ru: Добро пожаловать на Discord сервер {member.guild.name}, {member.mention}"
WELCOME_DESCRIPTION = ":flag_gb: For technical issues please contact {member.guild.get_user(bubble_id).mention} or {member.guild.get_user(tony_id).mention}\n:flag_ru: По техническим вопросам просьба обращаться к {member.guild.get_user(bubble_id).mention} или {member.guild.get_user(tony_id).mention}"  # and maybe shardeex..?
WELCOME_IMAGE = "ro2.jpg"

WELCOME_CHANNEL_ID = 728512405667315752
ROLE_ID = 719459081492103218


@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(WELCOME_CHANNEL_ID)
    ext = WELCOME_IMAGE.split(".")[-1]  # Расширение файла
    file = discord.File(WELCOME_IMAGE, filename=f"image.{ext}")

    embed = discord.Embed(
        title=WELCOME_TITLE.format(member=member), description=WELCOME_DESCRIPTION,
    ).set_image(url=f"attachment://image.{ext}")

    try:
        await channel.send(file=file, embed=embed)
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


TOKEN = os.environ.get("BOT_TOKEN")
Bot.run(TOKEN)

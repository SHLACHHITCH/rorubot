import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import steam
from steam import game_servers
from steam import game_servers as gs
import os



Bot = commands.Bot(command_prefix= "!")

#/////////////////////////////// server status ///////////////////////#

@Bot.command()    ## Инициируем команду боту
async def status(ctx):
	
    server_addr = next(gs.query_master(r'\gameaddr\37.230.228.193:7778')) ## Функция с инфой о сервере(не трогать!!!)
    info_map = gs.a2s_info(server_addr) ['map'] ## Текущая карта
    info_ping = gs.a2s_info(server_addr) ['_ping']  ## Пинг (зависит от местоположения бота, бесполезная строка)
    info_players = gs.a2s_info(server_addr) ['players'] ## Текущее кол-во игроков на сервере
    info_max_players= gs.a2s_info(server_addr) ['max_players'] ## Максимум игроков на сервере
    info_bots = gs.a2s_info(server_addr) ['bots'] ## Текущее кол-во ботов на сервере (бесполезно)

    emb = discord.Embed(title='Статус сервера')  ## Выводим бокс с названием "Статус сервера"
    emb.add_field(name='Карта:', value=info_map) ## Информация по карте и остальному
    emb.add_field(name='Игроки:', value=info_players)
    await ctx.send(embed=emb)
#/////////////////////////////// role giver ///////////////////////#

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="<719459081492103218>")
    await bot.add_roles(member, role)

#/////////////////////////////// server welcomer ///////////////////////#

WELCOME_CHANNEL_ID = 728512405667315752
WELCOME_TITLE = "Welcome To {member.guild.name},{member.name} || Добро пожаловать {member.name},в {member.guild.name}"
WELCOME_DESCRIPTION = "For all technical questions, please contact bubb1e and Tony Montana || По всем техническим вопросам просьба обращаться к bubb1e and Tony Montana"
WELCOME_IMAGE = "ro2.jpg"

WELCOME_CHANNEL = None

@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Activity(name='Welcome to Yong Army', type=discord.ActivityType.watching))
    print('Хэй, я уже в сети!\n1.1.0 (by shardeex, 2020)')

@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(WELCOME_CHANNEL_ID)
    ext = WELCOME_IMAGE.split('.')[-1]  # Расширение файла
    file = discord.File(WELCOME_IMAGE, filename=f"image.{ext}")

    embed = discord.Embed(
        title=WELCOME_TITLE.format(member=member),
        description=WELCOME_DESCRIPTION.format(member=member),
        ).set_image(url=f"attachment://image.{ext}")

    try:
        await channel.send(file=file, embed=embed)
    except discord.errors.Forbidden as e:
        print(f'Произошла ошибка при отправке сообщения: {e}')

token = os.environ.get('BOT_TOKEN')

Bot.run(str(token))

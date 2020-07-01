import discord
from discord.ext import commands
from discord.ext.commands import Bot
import steam
from steam import game_servers
from steam import game_servers as gs
import os


Bot = commands.Bot(command_prefix= "!")


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

token = os.environ.get('BOT_TOKEN')

Bot.run(str(token))

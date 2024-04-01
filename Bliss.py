import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import clean_content
import json
import os
import aiohttp
import io
import winsound
import subprocess
from datetime import datetime
from colorama import Fore, Style, init
import time
import sys


init()
os.system(f"title Bliss Selfbot cargando...")
def setear_tamano_ventana(alto, ancho):
    os.system(f"mode con: cols={ancho} lines={alto}")

setear_tamano_ventana(30, 88)

def menu():
    print(Fore.CYAN + """
                 ▄▄▄▄    ██▓     ██▓  ██████   ██████ 
                ▓█████▄ ▓██▒    ▓██▒▒██    ▒ ▒██    ▒ 
                ▒██▒ ▄██▒██░    ▒██▒░ ▓██▄   ░ ▓██▄   
                ▒██░█▀  ▒██░    ░██░  ▒   ██▒  ▒   ██▒
                ░▓█  ▀█▓░██████▒░██░▒██████▒▒▒██████▒▒
                ░▒▓███▀▒░ ▒░▓  ░░▓  ▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
                ▒░▒   ░ ░ ░ ▒  ░ ▒ ░░ ░▒  ░ ░░ ░▒  ░ ░
                 ░    ░   ░ ░    ▒ ░░  ░  ░  ░  ░  ░  
                 ░          ░  ░ ░        ░        ░  
                      ░                               
                            Bliss Selfbot 1.0
###############################################################""" + Style.RESET_ALL)

bot = commands.Bot(command_prefix=".", help_command=None, case_insensitive=True, self_bot=True)
start_time = datetime.now()

whitelist = [1075975022230900797]

with open('config.json', 'r') as file:
    config = json.load(file)
    token = config['token']

async def send_messages(ctx, message):
    while True:
        if not getattr(bot, 'send_messages', True):
            break
        sent_message = await ctx.channel.send(message)
        await asyncio.sleep(1)
menu()
@bot.event
async def on_ready():
    print(f"    [EXITOSO] Connected as {bot.user.name}({bot.user.id})")
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="/PDAT"
    )
    os.system(f"title Bliss Selfbot Logged as: {bot.user.name}")
    await bot.change_presence(activity=activity, status=discord.Status.online, afk=False)
    pc_name = 'Bliss'  # Reemplaza esto con el nombre de tu PC

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    os.system(f"title Bliss Selfbot logged as {bot.user.name}")
    winsound.PlaySound("C:/Users/bliss/Desktop/bliss selfbot/data/beep.wav", winsound.SND_FILENAME)

@bot.command(pass_context=True)
async def ping(ctx):
    if ctx.author.id in whitelist:
        message = await ctx.reply('Pong!')
        await message.delete()

spam_active = False  # Variable de estado para controlar si el spam está activo

@bot.command(pass_context=True)
async def spam(ctx, *, message: commands.clean_content):
    global spam_active
    if ctx.author.id in whitelist:
        spam_active = True  # Activar el spam
        await ctx.send(message)  # Envía el mensaje inicial
        await asyncio.sleep(2)  # Espera 2 segundos

        while spam_active:
            try:
                await ctx.send(message)  # Envía el mensaje repetido
                await asyncio.sleep(2)  # Espera 2 segundos entre cada repetición
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(3)  # Espera 3 segundos y vuelve a intentar
                    continue
                else:
                    raise

        await ctx.message.delete()  # Elimina el mensaje de comando

@bot.command(pass_context=True)
async def spamstop(ctx):
    global spam_active
    if ctx.author.id in whitelist:
        spam_active = False  # Detener el spam
    await ctx.message.delete()

@bot.command()
async def config(ctx):
    if ctx.author.id in whitelist:
        try:
            subprocess.Popen(['start', 'config.json'], shell=True)
            print("    [EXITOSO] Archivo config.json abierto exitosamente")
        except Exception as e:
            print("    [ERROR] No se pudo abrir config.json")
            print(f"Detalles del error: {e}")
        winsound.PlaySound("C:/Users/bliss/Desktop/bliss selfbot/data/beep.wav", winsound.SND_FILENAME)
        await ctx.message.delete()

@bot.command()
async def actividad(ctx, tipo, *, texto):
    if ctx.author.id in whitelist:
        try:
            if tipo.lower() == "playing":
                activity = discord.Game(name=texto)
            elif tipo.lower() == "streaming":
                activity = discord.Streaming(name=texto, url=texto)
            elif tipo.lower() == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=texto)
            elif tipo.lower() == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=texto)
            else:
                print("    [ERROR] Tipo de actividad no válido. Los tipos válidos son 'playing', 'streaming', 'watching' y 'listening'.")
                return

            winsound.PlaySound("C:/Users/bliss/Desktop/bliss selfbot/data/beep.wav", winsound.SND_FILENAME)
            await bot.change_presence(activity=activity)
            print("    [EXITOSO] Actividad actualizada correctamente.")
            await ctx.message.delete()

        except Exception as e:
            print(f"    [ERROR] Error al actualizar la actividad: {e}")
            await ctx.message.delete()

@bot.command()
async def userinfo(ctx, user_id: int = None):
    if ctx.author.id in whitelist:
        if user_id is None:
            winsound.PlaySound("C:/Users/bliss/Desktop/bliss selfbot/data/beep.wav", winsound.SND_FILENAME)
            print("    [ERROR] No proporcionaste el ID")
            return

        try:
            user = await bot.fetch_user(user_id)
            username = user.name
            user_discriminator = user.discriminator
            created_at = user.created_at.strftime("%d/%m/%Y %H:%M:%S")

            print("    [EXITOSO] Información de Usuario:")
            print(f"    Nombre: {username}")
            print(f"    ID: {user_id}")
            print(f"    Fecha de Creación: {created_at}")

        except discord.NotFound:
            print("    [ERROR] Usuario no encontrado.")
            await ctx.message.delete()

        os.system('cls' if os.name == 'nt' else 'clear')
        menu()

sniped_message = {}

@bot.event
async def on_message_delete(message):
    sniped_message[message.channel.id] = (message.author.name, message.content)

@bot.command()
async def snipe(ctx):
    if ctx.author.id in whitelist:
        return
    channel_id = ctx.channel.id
    if channel_id in sniped_message:
        author, content = sniped_message[channel_id]
        await ctx.send(f"```Mensaje borrado por: {author}\nMensaje: {content}\n\n\n\nBliss Selfbot<3```")
    else:
        await ctx.send("No hay mensajes borrados recientes.")





@bot.command()
async def ayuda(ctx):
    help_message = (
        "```ini\n"
        ".actividad   - Cambia la actividad del bot\n"
        ".cls         - Limpia la consola\n"
        ".config      - Abre la configuración del bot\n"
        ".exit        - Apaga el bot\n"
        ".ayuda        - Muestra este mensaje\n"
        ".ping        - Muestra el ping del bot\n"
        ".snipe       - Muestra el último mensaje borrado\n"
        ".spam        - Envia multiples mensajes\n"
        ".spamstop    - Deja de enviar los multiples mensajes\n"
        ".userinfo    - Muestra la información de un usuario\n"
        "\n"
        "[ Bliss Selfbot, release 1.3.0 ]```"
    )

    await ctx.reply(help_message)













































































































































## COMANDOS DEL FINAL
@bot.command()
async def cls(ctx):
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()
    await ctx.message.delete()

@bot.command()
async def exit(ctx):
    time.sleep(1)
    print("    [EXIT] Gracias por usar Bliss Private Panel, Vuelve pronto!")
    print("    [EXIT] Cerrando sesión, la consola se cerrará en 5 segundos...")
    await ctx.message.delete()
    time.sleep(5)
    sys.exit()
bot.run(token, bot=False)



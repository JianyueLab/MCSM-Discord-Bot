# ===== imports =====
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ===== Environmental Variables =====
load_dotenv()
# DC Token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
# Message
MESSAGE: bool = os.getenv("EPHEMERAL_MESSAGE", "False").lower() in ("true", "1")
# Version Information
BOT_VERSION = '0.1.2'
BOT_BUILD_TYPE = 'beta'

# ===== BOT =====
# Initial
intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print('Bot is ready')
    except Exception as e:
        print(e)



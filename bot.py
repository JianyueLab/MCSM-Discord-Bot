# imports
import os

import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

from scripts import instance_control, list_all, update, check_instance

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')

bot_version = 'v0.0.2'
build_type = 'Dev / 请不要用于生产等'

# 默认配置
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)


# 启动之后
@client.event
async def on_ready():
    # 终端输出
    try:
        synced = await client.tree.sync()
        result = update()
        print(f"机器人已启动 | 已同步 {len(synced)} 条指令 | {result}")

    except Exception as e:
        print(e)


# /list
@client.tree.command(name='list', description='显示全部节点和实例')
async def status(interaction: discord.Interaction):
    # 等待请求，并隐藏
    await interaction.response.defer(ephemeral=True)
    result = list_all()
    await interaction.followup.send(result)


# /instance 
@client.tree.command(name='instance', description='实例控制')
@app_commands.choices(choices=[
    app_commands.Choice(name="开启", value="start"),
    app_commands.Choice(name="关闭", value="stop"),
    app_commands.Choice(name="重启", value="restart"),
    app_commands.Choice(name="强制关闭", value="kill")
])
async def instance(interaction: discord.Interaction, choices: app_commands.Choice[str], instance_name: str):
    await interaction.response.defer(ephemeral=True)
    action = choices
    result = instance_control(action, instance_name)
    await interaction.followup.send(result)
    return


# /check
@client.tree.command(name='check', description='查看某个特定实例的信息')
async def check(interaction: discord.Interaction, instance_name: str):
    await interaction.response.defer(ephemeral=True)
    result = check_instance(instance_name)
    await interaction.followup.send(result)
    return


# /info
@client.tree.command(name='info', description='bot相关信息')
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        f'### MCSManager Discord Bot\nCopyright (C) JianyueLab | MIT LICENSE\n-------------------------\n- **版本: ** {bot_version} **|** {build_type}\n- **Github Repo: ** https://github.com/jianyuelab/mcsm-discord-bot\n欢迎通过PR或ISSUE来帮助优化项目'
    )
    return


client.run(TOKEN)

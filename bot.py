# imports
import discord
from discord.ext import commands
from discord import app_commands
from settings import TOKEN
from scripts import getAll

# 默认配置
intents = discord.Intents.all() 
client = commands.Bot(command_prefix='!', intents=intents)

# 启动之后
@client.event
async def on_ready():
    # 终端输出
    print("机器人已启动")
    try:
        synced = await client.tree.sync()
        print(f"已同步 {len(synced)} 条指令")
    except Exception as e:
        print(e)
    
# 获取全部的实例和节点
# /list
@client.tree.command(name='list', description='获取全部节点和实例')
async def status(interaction: discord.Interaction):
    # 等待请求，并隐藏
    await interaction.response.defer(ephemeral=True)
    result = getAll()
    if result == 'None':
        await interaction.followup.send("请求发生错误，请稍后重试")
        return
    else:
        await interaction.followup.send(result)
        return

client.run(TOKEN)
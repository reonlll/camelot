import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot起動完了: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

keep_alive()
bot.run(os.environ['TOKEN'])  # ← TOKENはRenderで設定する

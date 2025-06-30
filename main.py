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

@tree.command(name="残高", description="自分の所持GOLDを確認します")
async def check_balance(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    balance = balance_data.get(user_id, 0)
    await interaction.response.send_message(
        f"💰 {interaction.user.mention} の残高: {balance:,} GOLD", ephemeral=True
    )


keep_alive()
bot.run(os.environ['TOKEN'])  # ← TOKENはRenderで設定する

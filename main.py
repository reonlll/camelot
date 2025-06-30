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

@tree.command(name="送金", description="他のユーザーにGOLDを送ります")
@app_commands.describe(user="送金先ユーザー", amount="送る金額")
async def send_gold(interaction: discord.Interaction, user: discord.User, amount: int):
    sender_id = str(interaction.user.id)
    receiver_id = str(user.id)

    if amount <= 0:
        await interaction.response.send_message("⚠️ 金額は1以上にしてください", ephemeral=True)
        return

    if balance_data.get(sender_id, 0) < amount:
        await interaction.response.send_message("💸 所持GOLDが足りません", ephemeral=True)
        return

    # 送金処理
    balance_data[sender_id] -= amount
    balance_data[receiver_id] = balance_data.get(receiver_id, 0) + amount

    await interaction.response.send_message(
        f"✅ {amount:,} GOLD を {user.mention} に送金しました！", ephemeral=True
    )
    
@tree.command(name="GOLD付与", description="ユーザーにGOLDを付与します（管理者限定）")
@app_commands.describe(user="対象ユーザー", amount="付与する金額")
async def add_gold(interaction: discord.Interaction, user: discord.User, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 管理者専用コマンドです", ephemeral=True)
        return

    user_id = str(user.id)
    balance_data[user_id] = balance_data.get(user_id, 0) + amount

    await interaction.response.send_message(
        f"✅ {user.mention} に {amount:,} GOLD を付与しました", ephemeral=True
    )
    
@tree.command(name="GOLD減少", description="ユーザーのGOLDを減らします（管理者限定）")
@app_commands.describe(user="対象ユーザー", amount="減らす金額")
async def subtract_gold(interaction: discord.Interaction, user: discord.User, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 管理者専用コマンドです", ephemeral=True)
        return

    user_id = str(user.id)
    balance_data[user_id] = max(balance_data.get(user_id, 0) - amount, 0)

    await interaction.response.send_message(
        f"💸 {user.mention} から {amount:,} GOLD を減らしました", ephemeral=True
    )


keep_alive()
bot.run(os.environ['TOKEN'])  # ← TOKENはRenderで設定する

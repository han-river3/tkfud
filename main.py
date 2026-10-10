import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env 파일에서 환경 변수(토큰) 로드
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ---------------- [ 설정 부분 ] ----------------
# 봇을 사용할 수 있는 허용된 관리자 디스코드 ID 목록
ALLOWED_USER_IDS = [1533983071794233354, 1546780529331015745]
# -----------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"로그인 성공! 봇 이름: {bot.user.name} (ID: {bot.user.id})")
    print("=" * 40)

@bot.command(name="DM")
async def send_dm_notice(ctx, *, text: str):
    if ctx.author.id not in ALLOWED_USER_IDS:
        await ctx.send("❌ 이 명령어를 사용할 권한이 없습니다.")
        return

    success_count = 0
    fail_count = 0

    status_msg = await ctx.send("📢 서버의 모든 멤버에게 DM을 전송하는 중입니다...")

    for member in ctx.guild.members:
        if member.bot:
            continue

        try:
            dm_content = f"{member.mention} {text}"
            await member.send(dm_content)
            success_count += 1
        except discord.Forbidden:
            fail_count += 1
        except Exception:
            fail_count += 1

    await status_msg.edit(
        content=f"✅ **공지 전송 완료!**\n"
                f"- 성공: {success_count}명\n"
                f"- 실패 (DM 차단 등): {fail_count}명"
    )

bot.run(TOKEN)
import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv

load_dotenv()
bot   = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = os.environ.get("token")
print(TOKEN)

@bot.event
async def on_ready():
    print("bot is up and ready!!")
    await bot.load_extension("modules.combomanager.bot")
    await bot.load_extension("modules.auth.bot")
    await bot.load_extension("modules.auth.tasks")


    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command[s]")
    except Exception as e:
        print(e)

bot.run(token=TOKEN)
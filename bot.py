import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# For debugging purposes ------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_message(message):
    print(f"Received: {message.content}")
    await bot.process_commands(message)
#------------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f"Joined as {bot.user.name}!")

@bot.command()
async def Vandalized(ctx):
    print("Command Triggered!")
    await ctx.send("Hello SouL!")

bot.run(bot_token)
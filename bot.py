import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from services.gemini import gen_roast
from aiohttp import web
import asyncio
from services.valorant_api import get_recent_match_stats

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

@bot.command()
async def roast(ctx, name: str = None, tag: str = None):
    if not name or not tag:
        await ctx.send("⚠️ You need to provide both a Riot ID and a Tag! Example: `!roast Jett 1234` or `!roast \"SouL 死\" Cold`")
        return 

    # Show the "bot is typing..." indicator in Discord
    async with ctx.typing():
        try:
            out = await gen_roast(name, tag, "ap")
            
            chunk_size = 2000
            for i in range(0, len(out), chunk_size):
                await ctx.send(out[i:i+chunk_size])
                
        except Exception as e:
            await ctx.send("Something went wrong while cooking up the roast. Try again later.")
            print(f"Error: {e}")

@commands.command()
async def fetch(ctx, name: str = None, tag: str = None):
    if not name or not tag:
        await ctx.send("Give a name and tag")
        return

    async with ctx.typing():
        out = await get_recent_match_stats(name, tag, "ap")
        await ctx.send(out)

bot.add_command(fetch)

# PSEUDOSERVER----------------------------------------------------------------------------------
async def handle_ping(request):
    return web.Response(text="Valorant Roaster is online.")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()


async def main():
    await start_dummy_server()
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
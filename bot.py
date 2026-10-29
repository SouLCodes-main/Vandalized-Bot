import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from services.gemini import gen_roast
from aiohttp import web
import asyncio

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
            
            # Slice the output into 2000-character chunks to avoid the Discord limit
            chunk_size = 2000
            for i in range(0, len(out), chunk_size):
                await ctx.send(out[i:i+chunk_size])
                
        except Exception as e:
            await ctx.send("Something went wrong while cooking up the roast. Try again later.")
            print(f"Error: {e}")



# 1. The fake web server response
async def handle_ping(request):
    return web.Response(text="Valorant Roaster is online.")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render assigns a dynamic port via the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# 2. Run both the web server and the bot concurrently
async def main():
    # Start the web server to satisfy Render
    await start_dummy_server()
    # Start the Discord bot
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    # Remove your old bot.run() and replace it with this
    asyncio.run(main())
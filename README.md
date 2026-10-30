# Vandalized - Bot

**Vandalized** is a custom Discord bot that analyzes your recent competitive Valorant matches and uses Google's Gemini AI to deliver a brutal, customized roast based on your agent pool, K/D/A, and headshot percentage—topped off with one piece of genuine, actionable mechanical advice.

## Features
* **Live Stat Tracking:** Fetches real-time competitive match data using HenrikDev's Unofficial Valorant API.
* **AI-Powered Roasts:** Uses Google Gemini (Flash-Lite) to analyze stats and generate contextual, unique roasts.
* **Async Architecture:** Built with `discord.py` and `aiohttp` for non-blocking, lightning-fast responses.
* **Cloud-Ready:** Includes an embedded `aiohttp.web` dummy server, making it ready for free-tier 24/7 deployment on platforms like Render.

## Tech Stack
* **Python 3.10+**
* **discord.py** (Discord API wrapper)
* **google-genai** (Google Gemini AI SDK)
* **aiohttp** (Asynchronous HTTP requests)

## Installation & Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/Vandalized-Bot.git
cd Vandalized-Bot
```

**2. Install dependencies**
```bash
uv sync
```

**3. Set up your Environment Variables**
Create a `.env` file in the root directory of the project and add your API keys:
```env
BOT_TOKEN=your_discord_bot_token_here
VALORANT_API_KEY=your_henrikdev_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```
* *Get a Discord Token from the [Discord Developer Portal](https://discord.com/developers/applications).*
* *Get a HenrikDev API key from the [HenrikDev Discord](https://discord.com/invite/X3GaVkX2YN) (`#get-a-key` channel).*
* *Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).*

**4. Run the bot**
```bash
python bot.py
```

## ⚖️ Legal Disclaimer
*Vandalized-Bot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.*
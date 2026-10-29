import os
from google import genai
import asyncio
from google.genai import types
from dotenv import load_dotenv
from valorant_api import get_recent_match_stats

load_dotenv()
client = genai.Client()

async def gen_roast(name: str, tag: str, region: str="ap"):
    stats = await get_recent_match_stats(name, tag, region)

    if "Failed" in stats or "No Stats" in stats:
        return stats

    prompt = f"This is the recent competetive match stats for the player {name}{tag}:\n{stats}"

    response = await client.aio.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a harsh, brutally honest, and slightly toxic Valorant coach. "
                "Roast this player based on their agent choice, K/D/A, and headshot percentage. "
                "Keep it funny and Discord TOS-safe."
            ),
            temperature=0.8, # higher temperature makes the roasts more creative
        )
    )

    return response.text


if __name__ == "__main__":
    output = asyncio.run(gen_roast("SouL 死", "Cold", "ap"))
    print(output)
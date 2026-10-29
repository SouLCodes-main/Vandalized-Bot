import os
from google import genai
import asyncio
from google.genai import types
from dotenv import load_dotenv
from services.valorant_api import get_recent_match_stats
import socket
from google.genai.types import HttpOptions

# DEBUGGING BLOCK---------------------------------------------------------------------------------------------------------------------------

# Overrides the default infinite wait time
client = genai.Client(
    http_options=HttpOptions(timeout=15.0)
)

# Force Python's socket to only return IPv4 addresses (AF_INET)
_orig_getaddrinfo = socket.getaddrinfo

def _ipv4_only(*args, **kwargs):
    responses = _orig_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]

socket.getaddrinfo = _ipv4_only
#----------------------------------------------------------------------------------------------------------------------------------------------

load_dotenv()
client = genai.Client()

async def gen_roast(name: str, tag: str, region: str = "ap"):
    stats = await get_recent_match_stats(name, tag, region)
    
    if "Failed" in stats or "No recent" in stats:
        return stats
        
    prompt = f"Here are the recent competitive Valorant matches for {name}#{tag}:\n{stats}"
    
    try:
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a harsh, brutally honest, and slightly toxic Valorant pro. "
                        "Roast this player based on their agent choice, K/D/A, and headshot percentage. "
                        "Keep it funny and Discord TOS-safe. End the roast with one piece of genuine, "
                        "actionable mechanical advice. "
                        "CRITICAL RULE: Keep your entire response under 1500 characters and no more than 3 paragraphs."
                    ),
                    max_output_tokens=300,
                )
            ),
            timeout=30.0  # Absolute hard kill after 8 seconds
        )
        return response.text
        
    except asyncio.TimeoutError:
        # This triggers immediately when the 8 seconds are up
        return "The AI generation timed out. The network connection was likely dropped."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    output = asyncio.run(gen_roast("LOKEY", "6699", "ap"))
    print(output)
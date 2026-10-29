import os
import aiohttp
import asyncio
from dotenv import load_dotenv

# 1. Load the variables from .env
load_dotenv()

async def get_recent_match_stats(name: str, tag: str, region: str = "ap"):
    # 2. Use the dynamic variables in the f-string
    url = f"https://api.henrikdev.xyz/valorant/v1/stored-matches/{region}/{name}/{tag}?mode=competitive&size=4"
    
    headers = {
        "Authorization": os.getenv("VALORANT_API_KEY") 
    }
    
    async with aiohttp.ClientSession() as session:
        # 3. Pass the headers into the get request
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return f"Failed to fetch match data. Error: {response.status}"
                
            json_data = await response.json()
            matches = json_data.get('data', [])
            
            if not matches:
                return "No recent competitive matches found."
            
            match_summaries = []
            
            for match in matches:
                map_name = match['meta']['map']['name']
                agent = match['stats']['character']['name']
                
                kills = match['stats']['kills']
                deaths = match['stats']['deaths']
                assists = match['stats']['assists']
                
                headshots = match['stats']['shots']['head']
                bodyshots = match['stats']['shots']['body']
                legshots = match['stats']['shots']['leg']
                total_shots = headshots + bodyshots + legshots
                
                hs_percent = round((headshots / total_shots * 100), 1) if total_shots > 0 else 0
                
                summary = f"Played {agent} on {map_name}: {kills}/{deaths}/{assists} (HS%: {hs_percent}%)"
                match_summaries.append(summary)
                
            return "\n".join(match_summaries) 

# 4. Create an entry point to run the async function and print the output
if __name__ == "__main__":
    # Pass your Riot ID and Tag here. Use "ap" for Mumbai/Asia servers.
    output = asyncio.run(get_recent_match_stats("LOKEY", "6699", "ap"))
    print(output)
import aiohttp

session = aiohttp.ClientSession()


async def fetch_json(link):
    async with session.get(link) as resp:
        return await resp.json()

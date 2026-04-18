import asyncio
import aiohttp
import json

GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
TOKEN = "YOUR_BOT_TOKEN"


async def connect_to_gateway():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(GATEWAY_URL) as ws:
            hello = await ws.receive_json()
            heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000

            identify_payload = {
                "op": 2,
                "d": {
                    "token": TOKEN,
                    "intents": 513,
                    "properties": {
                        "os": "linux",
                        "browser": "my_bot",
                        "device": "my_bot"
                    }
                }
            }
            await ws.send_json(identify_payload)

            async def send_heartbeat():
                while True:
                    await asyncio.sleep(heartbeat_interval)
                    await ws.send_json({"op": 1, "d": None})

            asyncio.create_task(send_heartbeat())

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data.get("t") == "MESSAGE_CREATE":
                        content = data["d"].get("content", "")
                        author = data["d"]["author"]["username"]
                        print(f"[{author}]: {content}")


asyncio.run(connect_to_gateway())

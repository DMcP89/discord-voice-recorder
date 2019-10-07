import discord
import asyncio
import MyClient

from threading import Thread

print("Discord.py Voice Recorder POC")

DISCORD_TOKEN = ""

client = MyClient.MyClient()
client.run(DISCORD_TOKEN)


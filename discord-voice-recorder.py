import discord
import asyncio
import MyClient

from threading import Thread

print("Discord.py Voice Recorder POC")

DISCORD_TOKEN = "NTYzNTA4ODYwNjY5Nzg4MTcx.XKveqQ.nTylpkpb9IlkvwbeePRN2Ei22PQ"

client = MyClient.MyClient()
client.run(DISCORD_TOKEN)


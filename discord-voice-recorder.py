import discord
import asyncio
from threading import Thread

print("Discord.py Voice Recorder POC")

DISCORD_TOKEN = "NTYzNTA4ODYwNjY5Nzg4MTcx.XKveqQ.nTylpkpb9IlkvwbeePRN2Ei22PQ"

class BufSink(discord.reader.AudioSink):
    def __init__(self):
        self.bytearr_buf = bytearray()
        self.sample_width = 2
        self.sample_rate = 96000
        self.bytes_ps = 192000


    def write(self, data):
        self.bytearr_buf += data.data

    def freshen(self, idx):
        self.bytearr_buf = self.bytearr_buf[idx:]


close_flag = False


class MyClient(discord.Client):
    
    
    def __init__(self):
        super().__init__()
        self.target_channel = None
        self.post_thread = None
        self.buffer = BufSink()


    async def on_ready(self):
        print()
	print("Logged in as")
	print(self.user.name)
	print(self.user.id)
	print("----------")
	print("Discord.py version")
	print(discord.__version__)
	print("----------")
	print()

    async def on_message(self, message):


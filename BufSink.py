import discord

print("BufSink Class")

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
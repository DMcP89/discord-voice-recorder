import discord
import asyncio
import MyClient
import speech_recognition as sr
from threading import Thread

print("Discord.py Voice Recorder POC")

DISCORD_TOKEN = "NTYzNTA4ODYwNjY5Nzg4MTcx.XKveqQ.nTylpkpb9IlkvwbeePRN2Ei22PQ"

close_flag = False


def poster(bot, buffer, target_channel):
    global close_flag

    # we don't want the thread to end, so just loop forever
    while True:
        # useless to try anything if we don't have anything in the buffer
        # wait until we have enough data for a 5-second voice clip in the buffer
        if len(buffer.bytearr_buf) > 960000:
            # get 5 seconds worth of data from the buffer
            idx = buffer.bytes_ps * 5
            slice = buffer.bytearr_buf[:idx]

            # if the slice isn't all 0s, create an AudioData instance with it,
            # needed by the speech_recognition lib
            if any(slice):
                # trim leading zeroes, should be more accurate
                idx_strip = slice.index(next(filter(lambda x: x!=0, slice)))
                if idx_strip:
                    buffer.freshen(idx_strip)
                    slice = buffer.bytearr_buf[:idx]
                # create the AudioData object
                audio = sr.AudioData(bytes(slice), buffer.sample_rate,
                    buffer.sample_width)

                with open("recording-results.wav", "wb") as f:
                    f.write(audio.get_wav_data())
            # cut the part we just read from the buffer
            buffer.freshen(idx)

        # since it's an infinite loop, we need some way to break out, once the
        # program shuts down
        if close_flag:
            break

client = MyClient.MyClient()
client.run(DISCORD_TOKEN)


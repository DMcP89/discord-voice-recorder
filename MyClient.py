import discord
import BufSink

print("MyClient Class")

class MyClient(discord.Client):
    
    
    def __init__(self):
        super().__init__()
        self.target_channel = None
        self.post_thread = None
        self.buffer = BufSink()


    # post some sanity messages on start-up
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

    # wait for a message to interact with the user
    async def on_message(self, message):
        # notify the thread we're closing
        global close_flag
        
        # don't respond to ourselves
        if message.author == self.user:
            return False

        # handle closing
        if message.content.lower().startswith("$close"):
            # send a message to ack the command
            await message.channel.send("Got it, shutting down...")

            # the polite thing to do is close any active voice connections properly
            if self.voice_clients:
                for vc in self.voice_clients:
                    await vc.disconnect()
            # set the flag and wait for the thread to end
            close_flag = True
            self.post_thread.join()

            # shut down the bot, then quit the program
            await self.close()
            quit()

        # handle disconnecting
        if message.content.lower().startswith("$leave"):
            # close any active voice connections. in theory, there's only one, but
            # could be extended for more
            if self.voice_clients:
                for vc in self.voice_clients:
                    await vc.disconnect()
                # set the flag and wait for the thread to end
                close_flag = True
                self.post_thread.join()
            else:
                await message.channel.send("Sorry, you're not in a voice channel.")

        # handle summoning
        if message.content.lower().startswith("$here"):
            # if the user is not connect to a voice channel, but tries to summon,
            # just send a message and exit
            if message.author.voice is None:
                await message.channel.send("Sorry, you're not in a voice channel.")
            else:
                # check if we already have an active voice connection, and use that
                # one instead of creating another one
                if self.voice_clients:
                    # store the channel we need to post our output to
                    self.target_channel = message.channel
                    # ack the command and inform the user
                    await message.channel.send("Got it, moving to voice channel " +
                        message.author.voice.channel.name + " and directing output to " +
                        self.target_channel.name + ".")
                    # use the existing voice connection to move to the new voice channel
                    await self.voice_clients[0].move_to(message.author.voice.channel)
                    # start a thread that will handle voice analysis
                    # if it doesn't exist already
                    if self.post_thread is None:
                        self.post_thread = Thread(target=poster,
                                                  args=(self, self.buffer, self.target_channel))
                        self.post_thread.start()
                    # start listening - user filter just listens to a certain user
                    self.voice_clients[0].listen(discord.reader.UserFilter(
                        self.buffer, message.author))
                else:
                    # if we don't have an already active connection, create a new one
                    self.target_channel = message.channel
                    await message.channel.send("Got it, moving to voice channel " +
                        message.author.voice.channel.name + " and directing output to " +
                        self.target_channel.name + ".")
                    # create a new voice client
                    await message.author.voice.channel.connect()
                    # start a thread that will handle voice analysis,
                    # if it doesn't exist already
                    if self.post_thread is None:
                        self.post_thread = Thread(target=poster,
                                                  args=(self, self.buffer, self.target_channel))
                        self.post_thread.start()
                    # start listening - user filter just listens to a certain user
                    self.voice_clients[0].listen(discord.reader.UserFilter(
                        self.buffer, message.author))
from .common import *

# ping() - Entrypoint for !ping command
# message[required]: discord.Message
# This function is the main entrypoint of the !ping command
# and will a user's wager value to the amount passed between 1-25
async def ping(message:discord.Message):
  await message.channel.send("Pong! {}ms".format(round(client.latency * 1000)))
  
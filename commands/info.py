from .common import *

# info() - Entrypoint for !info command
# message[required]: discord.Message
# This function is the main entrypoint of the !info command
# and will a user's wager value to the amount passed between 1-25
async def info(message:discord.Message):
  await message.channel.send("Pong! {}ms".format(round(client.latency * 1000)))
  
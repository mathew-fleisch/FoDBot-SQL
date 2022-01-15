from .common import *
QUIZ_EPISODE = False

# quiz() - Entrypoint for !quiz command
# message[required]: discord.Message
# This function is the main entrypoint of the !quiz command
# and will a user's wager value to the amount passed between 1-25
async def quiz(message:discord.Message):
  await message.channel.send("Not implemented")
  
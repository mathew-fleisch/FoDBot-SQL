from commands.common import *
from commands.buy import buy
from commands.categories import categories
from commands.dustbuster import dustbuster
from commands.fmk import fmk
from commands.help import help
from commands.jackpot import jackpot, jackpots
from commands.poker import *
from commands.ping import ping
from commands.profile import profile
from commands.scores import scores
from commands.setwager import setwager
from commands.shop import shop
from commands.slots import slots, testslots
from commands.triv import *
from commands.trekduel import trekduel
from commands.trektalk import trektalk
from commands.tuvix import tuvix
print("> ENVIRONMENT VARIABLES AND COMMANDS LOADED")

print("> CONNECTING TO DATABASE")
seed_db()
ALL_PLAYERS = get_all_players()
print("> DATABASE CONNECTION SUCCESSFUL")

@client.event
async def on_message(message:discord.Message):
  # Ignore messages from bot itself
  if message.author == client.user:
    return
  all_channels = uniq_channels(config)
  if message.channel.id not in all_channels:
    # print(f"<! ERROR: This channel '{message.channel.id}' not in '{all_channels}' !>")
    return
  if int(message.author.id) not in ALL_PLAYERS:
    print("> New Player!!!")
    ALL_PLAYERS.append(register_player(message.author))
  print(message)
  if message.content.startswith("!"):
    print("> PROCESSING USER COMMAND")
    await process_command(message)

async def process_command(message:discord.Message):
  # Split the user's command by space and remove "!"
  user_command=message.content.lower().split(" ")
  user_command[0] = user_command[0].replace("!","")
  # If the user's first word matches one of the commands in configuration
  if user_command[0] in config.keys():
    if config[user_command[0]]["enabled"]:
      # TODO: Validate user's command
      await eval(user_command[0] + "(message)")
    else:
      print(f"<! ERROR: This function has been disabled: '{user_command[0]}' !>")
  else:
    print("<! ERROR: Unknown command !>")

EMOJI = {}
@client.event
async def on_ready():
  global EMOJI
  random.seed()
  EMOJI["shocking"] = discord.utils.get(client.emojis, name="qshocking")
  EMOJI["chula"] = discord.utils.get(client.emojis, name="chula_game")
  EMOJI["allamaraine"] = discord.utils.get(client.emojis, name="allamaraine")
  EMOJI["love"] = discord.utils.get(client.emojis, name="love_heart_tgg")
  print('> LOGGED IN AS {0.user}'.format(client))
  ALL_PLAYERS = get_all_players()
  print(f"> ALL_PLAYERS[{len(ALL_PLAYERS)}] - {ALL_PLAYERS}")
  print("> BOT STARTED AND LISTENING FOR COMMANDS!!!")


@client.event
async def on_raw_reaction_add(payload:discord.RawReactionActionEvent):
  global TRIVIA_ANSWERS, POKER_GAMES
  if payload.user_id != client.user.id:
    # poker reacts
    if payload.message_id in POKER_GAMES:
      if payload.user_id == POKER_GAMES[payload.message_id]["user"]:
        if payload.emoji.name == "✅":
          await resolve_poker(payload.message_id)
      else:
        user = await client.fetch_user(payload.user_id)
        await POKER_GAMES[payload.message_id]["message"].remove_reaction(payload.emoji,user)
    # trivia reacts
    if TRIVIA_MESSAGE and payload.message_id == TRIVIA_MESSAGE.id:
      #emoji = await discord.utils.get(TRIVIA_MESSAGE.reactions, emoji=payload.emoji.name)
      user = await client.fetch_user(payload.user_id)
      await TRIVIA_MESSAGE.remove_reaction(payload.emoji, user)
      TRIVIA_ANSWERS[payload.user_id] = payload.emoji.name

# Engage!
client.run(DISCORD_TOKEN)

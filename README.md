# Friends of DeSoto Bot

The Friends of DeSoto are a group of fans of Star Trek and [The Greatest Generation podcast](http://gagh.biz).

## Usage

This discord bot is built with python using the [discord.py library](https://discordpy.readthedocs.io/en/stable/api.html) and requires a mysql db with credentials stored in a .env file ([.env example](.env-example)). To develop locally, docker is used to standardize infrastructure and dependencies.

```bash
# Clone FoDBot source
git clone https://github.com/mathew-fleisch/FoDBot-SQL.git && cd FoDBot-SQL

# Fill out .env vars...
cp .env-example .env

# Start mysql container (~30 second startup time)
make db-start

# (optional) Load sql dump into database
make db-load

# Build local container to run bot in
make build

# Start bot (ctrl+c to stop)
make start-docker

# Mysql session with database
make db-mysql

# Bash session in mysql container
make db-bash

# Mysql dump to file
make db-dump

# Stop mysql container
make db-stop

# Blatent cheating
UPDATE users SET score=42069, spins=420, jackpots=69, wager=25, high_roller=1 WHERE id=1;
```

## Permissions

First you will need a discord app and bot token to send messages. See this youtube playlist to learn how: https://www.youtube.com/playlist?list=PLRqwX-V7Uu6avBYxeBSwF48YhAnSn_sA4

Additional [discord role permissions](https://support.discord.com/hc/en-us/articles/206029707-Setting-Up-Permissions-FAQ):

- View channels
- Send messages
- Send messages in thread
- Add reaction
- Manage messages

## Commands

Bot commands are triggered by typing command keys followed by an exclamation point. Commands must be defined in the [configuration.json](configuration.json) file, a python file in the [commands directory](commands), and an import line added to [main.py](main.py).

### configuration.json

The configuration.json file defines metadata about each command like what channel they can be executed in, what parameters can be passed, if the command requires additional data loaded, or if it should be enabled/disabled.

```json
"setwager": {
  "channels": [821892686201094154],
  "enabled": true,
  "data": null,
  "parameters": [{
    "name": "wager_value",
    "allowed": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
    "required": true
  }]
}
```

### commands/command.py

Each command requires a python script that accepts a discord message as input where the first word matches the filename (Example: `!setwager 25` => `commands/setwager.py`)

```python
from .common import *

# setwager() - Entrypoint for !setwager command
# message[required]: discord.Message
# This function is the main entrypoint of the !setwager command
# and will a user's wager value to the amount passed between 1-25
async def setwager(message:discord.Message):
  min_wager = 1
  max_wager = 25
  wager_val = message.content.lower().replace("!setwager ", "")
  player = get_player(message.author.id)
  current_wager = player["wager"]
  if wager_val.isnumeric():
    wager_val = int(wager_val)
    if wager_val >= min_wager and wager_val <= max_wager:
      set_player_wager(message.author.id, wager_val)
      msg = f"{message.author.mention}: Your default wager has been changed from `{current_wager}` to `{wager_val}`"
      await message.channel.send(msg)
    else:
      msg = f"{message.author.mention}: Wager must be a whole number between `{min_wager}` and `{max_wager}`\nYour current wager is: `{current_wager}`"
      await message.channel.send(msg)
  else:
    msg = f"{message.author.mention}: Wager must be a whole number between `{min_wager}` and `{max_wager}`\nYour current wager is: `{current_wager}`"
    await message.channel.send(msg)


# set_player_wager(discord_id, amt)
# discord_id[required]: int
# amt[required]: int
# This function takes a player's discord ID
# and a positive integer and updates the wager
# value for that user in the db
def set_player_wager(discord_id, amt):
  db = getDB()
  amt = max(amt, 0)
  query = db.cursor()
  sql = "UPDATE users SET wager = %s WHERE discord_id = %s"
  vals = (amt, discord_id)
  query.execute(sql, vals)
  db.commit()
  query.close()
  db.close()
```

### main.py

Each command requires an explicit import in the [main.py](main.py) script.

```python
from commands.setwager import setwager
```
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
# Friends of DeSoto Bot

The Friends of DeSoto are a group of fans of Star Trek and [The Greatest Generation podcast](http://gagh.biz).

## Usage

This discord bot is built with python using the [discord.py library](https://discordpy.readthedocs.io/en/stable/api.html) and requires a mysql db with credentials stored in a .env file ([.env example](.env-example)). To develop locally, docker is used to standardize infrastructure and dependencies.

```bash
# Clone FoDBot source
git clone https://github.com/mathew-fleisch/FoDBot-SQL.git && cd FoDBot-SQL

# Build docker container to run python
docker build -t fodbot .


# Start up mysql db in a docker container
source .env
docker run \
  --rm \
  -dit \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=${DB_PASS} \
  --name ${DB_CONTAINER_NAME} \
  mysql:latest


# Run FoDBot as container
docker run \
  --rm \
  -it \
  --name FoD \
  -v ${PWD}:/root/FoDBot-SQL \
  -w /root/FoDBot-SQL \
  fodbot

# Blatent cheating
UPDATE users SET score=42069, spins=420, jackpots=69, wager=25, high_roller=1 WHERE id=1;
```
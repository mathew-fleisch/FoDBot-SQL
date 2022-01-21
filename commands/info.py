from .common import *
import re

# info() - Entrypoint for !info command
# message[required]: discord.Message
# This function is the main entrypoint of the !info command
async def info(message:discord.Message):
  f = open("./data/episodes/tng.json")
  show_data = json.load(f)
  f.close()
  user_command = message.content.lower().replace("!info ", "").split()
  found = False
  if len(user_command) == 2:
    show = user_command[0]
    season = re.sub(r'e.*', '', user_command[1]).replace("s","")
    episode = re.sub(r'.*e', '', user_command[1])
    print(f"{show} {season}x{episode}")
    show_index = -1
    for ep in show_data["episodes"]:
      show_index = show_index + 1
      if ep["season"] == season and ep["episode"] == episode:
        found = True
        break
  if found:
    display_embed = await get_show(show_data, show_index)
    embed=discord.Embed(title=display_embed["title"], \
      url=display_embed["url"], \
      description=display_embed["description"], \
      color=0xFFFFFF)
    embed.set_thumbnail(url=display_embed["still"])
    await message.channel.send(embed=embed)
  else:
    await message.channel.send("Could not find this episode.\n" \
      + "Usage: `!info [show] [s##e##]`\n" \
      + "If this episode should exist, or is incorrect, help fix the source data here:\n" \
      + "https://github.com/jp00p/FoDBot-SQL/tree/main/data/episodes")


async def get_show(show_data, show_index):
  print(f"get_show(show_data, {show_index})")
  # print(f"{show_data}")
  pods = "TGG: N/A\n"
  tep = show_data["episodes"][show_index]
  if len(tep["podcasts"]) > 0:
    pods = "TGG: [" + tep["podcasts"][0]["episode"] + "]" \
      +"(" + tep["podcasts"][0]["link"] + ")\n"
  display_title = "TNG[s" + tep["season"] + "e" + tep["episode"] + "] - " \
    + tep["title"]
  display_url = "https://memory-alpha.fandom.com/wiki/" + tep["memoryalpha"]
  display_description = \
    "[imdb](https://www.imdb.com/title/" + tep["imdb"] + ") | " \
    + "[memory alpha](" + display_url + ")\n" \
    + pods \
    + "Airdate: " + tep["airdate"] + "\n" \
    + tep["description"]
  display_random_image = random.choice(tep["stills"])
  ret = {
    "title": display_title,
    "url": display_url,
    "description": display_description,
    "still": display_random_image
  }
  return ret


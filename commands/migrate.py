from .common import *
import inspect

# migrate() - Entrypoint for !migrate command
# message[required]: discord.Message
# This function is the main entrypoint of the !migrate command
async def migrate(message:discord.Message):
  # episode = tmdb.TV_Episodes(655,1,3).info()
  # print(f">>> Info: {episode}")
  # # episode = tmdb.TV_Episodes(655,1,1).credits()
  # # print(f">>> credits: {episode}")
  # episode = tmdb.TV_Episodes(655,1,1).images()
  # print(f">>> images: {episode}")

  f = open("./data/tgg_tng.json")
  tgg = json.load(f)
  f.close()
  tng_eps = load_file_into_array("./data/episodes/tng_eps")
  tshow = 655
  episodes = []
  track = 0
  max = 200
  for ep in tng_eps:
    # print(f"Ep: {ep}")
    this_episode = {}
    eps = ep.split("|")
    tseason = eps[2]
    if int(eps[2]) < 10:
      tseason = "0" + eps[2]
    tepisode = eps[3]
    if int(eps[3]) < 10:
      tepisode = "0" + eps[3]
    tgg_key = "s" + tseason + "e" + tepisode
    print(f'Title[{eps[1]}][s{tseason}e{tepisode}]: {eps[0]}')
    # await message.channel.send('Migrating[' + eps[1] + '][s' + tseason + 'e' + tepisode + ']:' + eps[0])
    this_episode["title"] = eps[0]
    this_episode["season"] = tseason
    this_episode["episode"] = tepisode
    this_episode["tvdb"] = eps[1]
    
    this_episode["memoryalpha"] = ""
    this_episode["podcasts"] = []
    if tgg_key in tgg:
      this_episode["memoryalpha"] = tgg[tgg_key]["memoryalpha"]
      this_episode["podcasts"] = tgg[tgg_key]["podcasts"]
    episode = tmdb.TV_Episodes(tshow,int(tseason),int(tepisode)).external_ids()
    # print(f">>> external: {episode}")
    this_episode["imdb"]=episode["imdb_id"]

    episode = tmdb.TV_Episodes(tshow,int(tseason),int(tepisode)).info()
    # print(f">>> Info: {episode}")
    this_episode["airdate"] = episode["air_date"].replace("-", ".")
    this_episode["description"] = episode["overview"]

    episode = tmdb.TV_Episodes(tshow,int(tseason),int(tepisode)).images()
    # print(f">>> images: {episode}")
    tstills = []
    for s in episode["stills"]:
      tstills.append(TMDB_IMG_PATH + s["file_path"])
    this_episode["stills"] = tstills

    episodes.append(this_episode)
    await asyncio.sleep(.1)
    if track > max:
      break
    track=track+1
  print(f"Episodes: {episodes}")
  show = {
    "title": "Star Trek: The Next Generation",
    "tvdb": 655,
    "imdb": "tt0092455",
    "episodes": episodes
  }
  with open('./data/episodes/tng.json', 'w') as f:
    json.dump(show, f)
  # print(f"{inspect.getmembers(episode)}")
  # await message.channel.send("<https://www.imdb.com/title/{}/> {}ms".format(imdb, round(client.latency * 1000)))

def load_file_into_array(file_name):
  file_obj = open(file_name, "r") 
  lines = file_obj.read().splitlines()
  file_obj.close()
  return lines
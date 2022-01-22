from .common import *
import inspect
from os.path import exists

def load_file_into_array(file_name):
  file_obj = open(file_name, "r") 
  lines = file_obj.read().splitlines()
  file_obj.close()
  return lines


# NON_TREK_SHOWS = [
#   ["Friends", 1668, friends_eps],
#   ["Firefly", 1437, ff_eps],
#   ["The Simpsons", 456, simpsons_eps],
#   ["Community", 18347, community_eps],
#   ["Futurama", 615, futurama_eps],
#   ["Buffy the Vampire Slayer", 95, buffy_eps],
#   ["Supernatural", 1622, supernatural_eps],
#   ["Seinfeld", 1400, seinfeld_eps],
#   ["Babylon 5", 3137, bab5_eps],
#   ["It's Always Sunny in Philidelphia", SUNNY_ID, sunny_eps]
# ]




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


  # tng_eps = load_file_into_array("./data/episodes/tng_eps")
  # ds9_eps = load_file_into_array("./data/episodes/ds9_eps")
  # friends_eps = load_file_into_array("./data/episodes/friends_eps")
  # firefly_eps = load_file_into_array("./data/episodes/firefly_eps")
  # simpsons_eps = load_file_into_array("./data/episodes/simpsons_eps")
  # # community_eps = load_file_into_array("./data/episodes/community_eps")
  # # buffy_eps = load_file_into_array("./data/episodes/buffy_eps")
  # # futurama_eps = load_file_into_array("./data/episodes/futurama_eps")
  # # supernatural_eps = load_file_into_array("./data/episodes/supernatural_eps")
  # # seinfeld_eps = load_file_into_array("./data/episodes/seinfeld_eps")
  # # bab5_eps = load_file_into_array("./data/episodes/bab5_eps")
  # sunny_eps = load_file_into_array("./data/episodes/sunny_eps")

  shows = {
    "tng": {
      "tvdb":655,
      "title": "Star Trek: The Next Generation",
      "trek": True,
      "animated": False,
      "imdb": "tt0092455"
    },
    "voy": {
      "tvdb":1855,
      "title": "Star Trek: Voyager",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "ds9": {
      "tvdb":580,
      "title": "Star Trek: Deep Space Nine",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "friends": {
      "tvdb":1668,
      "title": "Friends",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "firefly": {
      "tvdb":1437,
      "title": "Firefly",
      "trek": False,
      "animated": False,
      "imdb": ""
    },
    "simpsons": {
      "tvdb":456,
      "title": "The Simpsons",
      "trek": False,
      "animated": True,
      "imdb": ""
    },
    "enterprise": {
      "tvdb":314,
      "title": "Star Trek: Enterprise",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "tos": {
      "tvdb":253,
      "title": "Star Trek: The Original Series",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "lowerdecks": {
      "tvdb":85948,
      "title": "Star Trek: Lower Decks",
      "trek": True,
      "animated": True,
      "imdb": ""
    },
    "disco": {
      "tvdb":67198,
      "title": "Star Trek: Discovery",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "picard": {
      "tvdb":85949,
      "title": "Star Trek: Picard",
      "trek": True,
      "animated": False,
      "imdb": ""
    },
    "tas": {
      "tvdb":1992,
      "title": "Star Trek: The Animated Series",
      "trek": True,
      "animated": True,
      "imdb": ""
    },
    "sunny": {
      "tvdb":2710,
      "title": "It's Always Sunny in Philidelphia",
      "trek": False,
      "animated": False,
      "imdb": ""
    },
  }
  migrate_spl = message.content.lower().replace("!migrate ", "").split()
  this_show = migrate_spl[0]
  this_show_id = shows[this_show]["tvdb"]
  episodes = []
  track = 0
  max = 200
  eps = load_file_into_array("./data/episodes/" + this_show + "_eps")
  tgg = {}
  if exists("./data/tgg_" + this_show + ".json"):
    f = open("./data/tgg_" + this_show + ".json")
    tgg = json.load(f)
    f.close()
  for ep in eps:
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
    logger.info(f'Title[{eps[1]}][s{tseason}e{tepisode}]: {eps[0]}')
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
    this_episode["imdb"] = ""
    this_episode["airdate"] = ""
    this_episode["description"] = ""
    this_episode["stills"] = []
    tmdb_episode = tmdb.TV_Episodes(this_show_id,int(tseason),int(tepisode))
    try:
      episode_external_ids = tmdb_episode.external_ids()
      logger.info(f">>> external: {episode_external_ids}")
      this_episode["imdb"]=episode_external_ids["imdb_id"]

      episode_details = tmdb_episode.info()
      logger.info(f">>> Info: {episode_details}")
      this_episode["airdate"] = episode_details["air_date"].replace("-", ".")
      this_episode["description"] = episode_details["overview"]

      episode_stills = tmdb_episode.images()
      logger.info(f">>> images: {episode_stills}")
      tstills = []
      for s in episode_stills["stills"]:
        tstills.append(TMDB_IMG_PATH + s["file_path"])
      this_episode["stills"] = tstills
    except:
        pass

    episodes.append(this_episode)
    await asyncio.sleep(.1)
    if track > max:
      break
    track=track+1
  logger.info(f"Episodes: {episodes}")
  show = {
    "title": shows[this_show]["title"],
    "tvdb": this_show_id,
    "trek": shows[this_show]["trek"],
    "animated": shows[this_show]["animated"],
    "imdb": shows[this_show]["imdb"],
    "episodes": episodes
  }
  with open('./data/episodes/' + this_show + '.json', 'w') as f:
    json.dump(show, f, indent=4)
  # print(f"{inspect.getmembers(episode)}")
  # await message.channel.send("<https://www.imdb.com/title/{}/> {}ms".format(imdb, round(client.latency * 1000)))


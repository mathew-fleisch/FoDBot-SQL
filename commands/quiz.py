from .common import *
QUIZ_EPISODE = False
LAST_SHOW = False
TMDB_IMG_PATH = "https://image.tmdb.org/t/p/original"
PREVIOUS_EPS = {}
CORRECT_ANSWERS = {}
FUZZ = {}
LOG = []

def load_file_into_array(file_name):
  file_obj = open(file_name, "r") 
  lines = file_obj.read().splitlines()
  file_obj.close()
  return lines
tng_eps = load_file_into_array("./data/episodes/tng_eps")
ds9_eps = load_file_into_array("./data/episodes/ds9_eps")
friends_eps = load_file_into_array("./data/episodes/friends_eps")
ff_eps = load_file_into_array("./data/episodes/firefly_eps")
simpsons_eps = load_file_into_array("./data/episodes/simpsons_eps")
community_eps = load_file_into_array("./data/episodes/community_eps")
buffy_eps = load_file_into_array("./data/episodes/buffy_eps")
futurama_eps = load_file_into_array("./data/episodes/futurama_eps")
supernatural_eps = load_file_into_array("./data/episodes/supernatural_eps")
seinfeld_eps = load_file_into_array("./data/episodes/seinfeld_eps")
bab5_eps = load_file_into_array("./data/episodes/bab5_eps")
tas_eps = load_file_into_array("./data/episodes/tas_eps")
tos_eps = load_file_into_array("./data/episodes/tos_eps")
enterprise_eps = load_file_into_array("./data/episodes/enterprise_eps")
ldx_eps = load_file_into_array("./data/episodes/lowerdecks_eps")
picard_eps = load_file_into_array("./data/episodes/picard_eps")
disco_eps = load_file_into_array("./data/episodes/disco_eps")
voy_eps = load_file_into_array("./data/episodes/voy_eps")
sunny_eps = load_file_into_array("./data/episodes/sunny_eps")

TNG_ID = 655
VOY_ID = 1855
DS9_ID = 580
XFILES_ID = 4087
FRIENDS_ID = 1668
FF_ID = 1437
SIMPSONS_ID = 456
ENTERPRISE_ID = 314
TOS_ID = 253
LDX_ID = 85948
DISCO_ID = 67198
PICARD_ID = 85949
TAS_ID = 1992
SUNNY_ID = 2710

TREK_SHOWS = [
  ["The Next Generation", TNG_ID, tng_eps],
  ["Deep Space Nine", DS9_ID, ds9_eps],
  ["Voyager", VOY_ID, voy_eps],
  ["Enterprise", ENTERPRISE_ID, enterprise_eps],
  ["Discovery", DISCO_ID, disco_eps],
  ["Picard", PICARD_ID, picard_eps],
  ["The Original Series", TOS_ID, tos_eps],
  ["Lower Decks", LDX_ID, ldx_eps],
  ["The Animated Series", TAS_ID, tas_eps]
]

TREK_WEIGHTS = []
for i in range(len(TREK_SHOWS)):
  # weights are how many eps in the total show (favors 90s trek)
  TREK_WEIGHTS.append(len(TREK_SHOWS[i][2]))

NON_TREK_SHOWS = [
  ["Friends", 1668, friends_eps],
  ["Firefly", 1437, ff_eps],
  ["The Simpsons", 456, simpsons_eps],
  ["Community", 18347, community_eps],
  ["Futurama", 615, futurama_eps],
  ["Buffy the Vampire Slayer", 95, buffy_eps],
  ["Supernatural", 1622, supernatural_eps],
  ["Seinfeld", 1400, seinfeld_eps],
  ["Babylon 5", 3137, bab5_eps],
  ["It's Always Sunny in Philidelphia", SUNNY_ID, sunny_eps]
]

# quiz() - Entrypoint for !quiz command
# message[required]: discord.Message
# This function is the main entrypoint of the !quiz command
# and will a user's wager value to the amount passed between 1-25
async def quiz(message:discord.Message):
  if not QUIZ_EPISODE:
    await message.channel.send("Getting episode image, please stand by...")
    episode_quiz.start()
  else:
    threshold = 72  # fuzz threshold
    # lowercase and remove trailing spaces
    correct_answer = QUIZ_EPISODE[0].lower().strip()
    guess = message.content.lower().replace("!quiz ", "").strip()
    # remove all punctuation
    correct_answer = "".join(l for l in correct_answer if l not in string.punctuation).split()
    guess = "".join(l for l in guess if l not in string.punctuation).split()
    # remove common words
    stopwords = ["the", "a", "of", "is", "teh", "th", "eht", "eth", "of", "for", "part 1", "part 2", "part ii", "part i", "in", "are", "an", "as", "and"]
    resultwords  = [word for word in correct_answer if word.lower() not in stopwords]
    guesswords = [word for word in guess if word.lower() not in stopwords]
    # rejoin the strings
    correct_answer = ' '.join(resultwords)
    guess = ' '.join(guesswords)
    # check ratios
    ratio = fuzz.ratio(correct_answer, guess)
    pratio = fuzz.partial_ratio(correct_answer, guess)
    # arbitrary single-number score
    normalness = round((ratio + pratio) / 2)
    # add message to the log for reporting
    if (ratio != 0) and (pratio != 0):
      LOG.append([guess, ratio, pratio])
    # check answer
    if (ratio >= threshold and pratio >= threshold) or (guess == correct_answer):
      # correct answer      
      award = 1
      bonus = False
      if (ratio < 80 and pratio < 80):
        # bonus
        bonus = True
        award = 2
      id = message.author.id
      if id not in CORRECT_ANSWERS:
        if not CORRECT_ANSWERS:
          award *= 10
        else:
          award *= 5
        set_player_score(message.author, award)
        if id not in FUZZ:
          score_str = "`Correctitude: " + str(normalness) +"`"
          if not bonus:
            score_str += " <:combadge:867891664886562816>"
          else:
            score_str += " <a:combadge_spin:867891818317873192>"
          FUZZ[id] = score_str
        CORRECT_ANSWERS[id] = { "name": message.author.mention, "points":award }
    else:
      if (ratio >= threshold-6 and pratio >= threshold-6):
        await message.add_reaction(EMOJI["shocking"])

@tasks.loop(seconds=31,count=1)
async def episode_quiz(non_trek=False, simpsons=False):
  global QUIZ_EPISODE, TMDB_IMG_PATH, LAST_SHOW, QUIZ_SHOW, PREVIOUS_EPS, LOG
  quiz_channel = client.get_channel(config["commands"]["quiz"]["channels"][0])
  headers = {'user-agent': 'Mozilla/5.0'}
  if non_trek:
    print("TV quiz!")
    shows = NON_TREK_SHOWS
  else:
    print("Trek quiz!")
    shows = TREK_SHOWS
  # todo: why did i do this
  if simpsons:
    selected_show = shows[2]
  else:
    if non_trek:
      selected_show = random.choice(shows)
    else:
      selected_show = random.choices(shows, tuple(TREK_WEIGHTS), k=1)
      selected_show = selected_show[0]
    # dont pick the same show again
    while selected_show == LAST_SHOW:
      if non_trek:
        selected_show = random.choice(shows)
      else:
        selected_show = random.choices(shows, tuple(TREK_WEIGHTS), k=1)
        selected_show = selected_show[0]
    LAST_SHOW = selected_show
  # for displaying to users
  show_name = selected_show[0]
  if not non_trek:
    show_name = "Star Trek: " + show_name
  show_id = selected_show[1]
  show_eps = selected_show[2]
  # don't pick the same episode as last time
  episode = random.choice(show_eps)
  if selected_show[0] in PREVIOUS_EPS.keys():
    while episode == PREVIOUS_EPS[selected_show[0]]:
      episode = random.choice(show_eps)
  PREVIOUS_EPS[selected_show[0]] = episode
  episode = episode.split("|")
  QUIZ_EPISODE = episode
  QUIZ_SHOW = selected_show[0] # current show
  print(f"Correct answer: {episode}")
  episode_images = tmdb.TV_Episodes(show_id, episode[2], episode[3]).images()
  image = random.choice(episode_images["stills"])
  r = requests.get(TMDB_IMG_PATH + image["file_path"], headers=headers)
  with open('./images/ep.jpg', 'wb') as f:
    f.write(r.content)
  LOG = [] # reset the log
  await quiz_channel.send(file=discord.File("./images/ep.jpg"))
  await quiz_channel.send("Which episode of **__"+str(show_name)+"__** is this? <a:horgahn_dance:844351841017921597>\nTo answer type: `!quiz [your guess]`")


@episode_quiz.after_loop
async def quiz_finished():
  global QUIZ_EPISODE, CORRECT_ANSWERS, FUZZ, QUIZ_SHOW, PREVIOUS_EPS
  #await asyncio.sleep(1)
  print("Ending quiz...")
  quiz_channel = client.get_channel(config["commands"]["quiz"]["channels"][0])
  # quiz_channel = client.get_channel(891412585646268486)
  msg = "The episode title was: **{0}** (Season {1} Episode {2})\n".format(QUIZ_EPISODE[0].strip(), QUIZ_EPISODE[2], QUIZ_EPISODE[3])
  if len(CORRECT_ANSWERS) == 0:
    roll = random.randint(5,10)
    #todo: add random lose msgs
    msg += "Did you win? Hardly! Adding `{} point(s)` to the jackpot.".format(roll)
    increase_jackpot(roll)
  else:
    #todo: add random win msgs
    msg += "Chula! These crewmembers got it:\n"
    for c in CORRECT_ANSWERS:
      msg += "{} - {} points - {}\n".format(CORRECT_ANSWERS[c]["name"], CORRECT_ANSWERS[c]["points"], FUZZ[c])
  await quiz_channel.send(msg)
  # update the quiz stuff
  CORRECT_ANSWERS = {} # winners
  FUZZ = {} # fuzz report
  QUIZ_SHOW = False 
  QUIZ_EPISODE = False # the current episode
  print("Quiz finished!")
import os
import time
import re
import datetime
from slackclient import SlackClient
from random import sample, choice, random, randint
import configparser

# TUTORIAL:
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

config = configparser.ConfigParser()
if os.path.isfile('../config/settings.ini'):
    config.read('../config/settings.ini')
else:
    print("Error: no \"config/settings.ini\" file. Use \"config/settings.ini.sample\" as template.")
    exit()

# instantiate Slack client
slack_client = SlackClient(config.get("global", "slack_token"))
# starterbot's user ID in Slack: value is assigned after the bot starts up
BOT_ID = None


money_raised = random() * 100
global_alive = True

channel_Ids = {
    "charity-tree-project": "GCDNZ6VND",
    "cruisecares": "C52GLMRC7",
}

exclaims = [
    "",
    "Wow!",
    "Incredible!",
    "Horray!",
    "Yay!",
    "Nice work!",
    "So generous!",
    "Oh yea!",
    "BOOM...",
    "Fantastic!",
    "This. Is. Amazing.",
    "Holy smokes...",
    "HOT DIGGIDY!",
    "Shiver me timbers!",
    "Love it!",
    "Jumpin jack rabits!",
    "Holy shit, batman!",  # is this ok?
]

anounce = [
    "We have raised",
    "We have gathered",
    "We have reached",
    "We've raised",
    "We've gathered",
    "We've reached",
    "We're up to",
    "The fund has reached",
    "So far, we've raised",
    "Thus far we have raised",
    "It's reached",
    "It's up to",
]

encouragement = [
    "",
    "Lets keep it up!",
    "Way to go everyone!",
    "Nice work everyone!",
    "Great work everyone!",
    "Woohoo!",
    "Lets keep going!",
    "Lets keep it up!",
    "I'm impressed!",
    "We must construct aditional pylons!",
    "Soon we'll be... OVER NINE THOUSAND!!!",
]

emoji_heart = [
    "heart",
    "two_hearts",
    "heartpulse",
    "blue_heart",
    "green_heart",
    "purple_heart",
    "heart_rainbow",
    "rainbow_heart",
    "sparkling_heart",
]

emoji_tree = [
    "xmastree",
    "aspen_tree",
    "deciduous_tree",
    "minecrafttree",
    "palm_tree",
    "tanabata_tree",
]

emoji_dance = [
    "party-parrot",
    "rainbowsheep",
    "chardance",
    "otter-dance",
    "brakedance",
    "aaw_yeah",
    "party-dinosaur",
    "flossing_avocado",
    "party",
    "yay-megaman",
]

emoji_parrot = [
    "aussieparrot",
    "aussiereversecongaparrot",
    "bananaparrot",
    "blacklistparrot",
    "bluescluesparrot",
    "ci_parrot",
    "climbingparrot",
    "coffeeparrot",
    "conga_parrot",
    "construction_parrot",
    "cpp_parrot",
    "deal_with_it_parrot",
    "devil_parrot",
    "donutparrot",
    "downclimbingparrot",
    "dreidel_parrot",
    "emv-parrot",
    "explody-parrot",
    "eyes_parrot",
    "fiesta_parrot",
    "fire_parrot",
    "garrett_parrot",
    "gmparrot",
    "hocho_parrot",
    "invisible_parrot",
    "jira-parrot",
    "laserparrot",
    "lava-parrot",
    "map_parrot",
    "nyanparrot",
    "parrot_dad",
    "partier-parrot",
    "partiest-parrot",
    "party-parrot",
    "pizza_parrot",
    "portalblueparrot",
    "portalorangeparrot",
    "portalparrot",
    "python-parrot",
    "qparrot",
    "rotatingparrot",
    "sad_parrot",
    "shipit-parrot",
    "shuffle_parrot",
    "ski_parrot",
    "slow_parrot",
    "soon_parrot",
    "thumbs_up_parrot",
    "trollparrot",
    "uwot-parrot",
    "vault_parrot",
    "velodyneparrot",
    "wendyparrot",
]

emoji_think = [
    "activated-my-think-card",
    "bolshethink",
    "es-thinking",
    "fidget-thinker",
    "hr_thinkinglation",
    "imthinking",
    "ingthink",
    "think",
    "think_drops",
    "thinkberry",
    "thinking",
    "thinking-and-dragons",
    "thinking-left",
    "thinking_duck",
    "thinking_helmet",
    "thinking_zone",
    "thinkinger",
    "thinkingest",
    "thinkingwithportals",
    "thinkplant",
    "thinksmart",
    "thinkspector",
    "thinkspin",
    "thinkspintilt",
    "triplethink",
    "triplethinkfast",
    "triplethinkslow",
]

emoji_all = emoji_heart + emoji_tree + emoji_dance + [
    "cruise",
    "herky-jerky",
    "madkrooze",
    "dancing-penguin",
    "hamsterdance",
    "badger-dance",
    "tada",
    "hands",
    "krooze",
    "allthethings",
    "woohoo",
]


def get_random_emojis(emojis, max_len):
    return " ".join([":%s:" % x for x in sample(emojis, randint(1, min(max_len, len(emojis) - 1)))])


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            matches = re.findall("<@(|[WU].+?)>", event["text"])
            if BOT_ID in matches:
                return event["text"], event["channel"]
    return None, None


def send_response(text, channel):
    slack_client.api_call("chat.postMessage", channel=channel, text=text)


def chat_amount_raised(channel):
    message = "{} {} ${:2.2f}\n{}\n{}".format(
        choice(exclaims),
        choice(anounce),
        money_raised,
        choice(encouragement),
        "" if randint(0, 3) else get_random_emojis(emoji_all, 10),
    )
    send_response(message, channel)


def chat_info(channel):
    message = "I am a <#C52GLMRC7|cruisecares> project that is raising funds for http://www.thearcsf.org/ \nGrab a card and make a donation to a fellow San Franciscan in need! {}"
    send_response(message.format(get_random_emojis(emoji_heart + emoji_tree, 2)), channel)


def chat_help(channel):
    send_response("Ask me how much money we've raised or about the `charity-tree` project.", channel)


def thread_run(callback):
    global global_alive
    global BOT_ID

    if slack_client.rtm_connect(with_team_state=False):
        print("Charity-tree Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        BOT_ID = slack_client.api_call("auth.test")["user_id"]
        while global_alive:
            message, channel = parse_bot_commands(slack_client.rtm_read())
            if message:
                message = message.lower()
                callback(message, channel)
                print("{} : Channel {} : \"{}\"".format(datetime.datetime.now(), channel, message))
                # how much money has been raised
                if any(x in message for x in ["how much", "given", "raise", "amount", "up to"]):
                    chat_amount_raised(channel)

                # general info
                elif any(x in message for x in ["how does", "this work", "what is", "what do", "who is", "who are you", "tell me", "whoami", "info"]):
                    chat_info(channel)

                # fun stuff
                elif any(x in message for x in ["emoji"]):
                    send_response(get_random_emojis(emoji_all, randint(5, 30)), channel)
                elif any(x in message for x in ["love", "heart"]):
                    send_response(get_random_emojis(emoji_heart, randint(1, 20)), channel)
                elif any(x in message for x in ["dance", "party"]):
                    send_response(get_random_emojis(emoji_dance, randint(10, 30)), channel)
                elif any(x in message for x in ["parrot"]):
                    send_response(get_random_emojis(emoji_parrot, randint(10, 20)), channel)
                elif any(x in message for x in ["think", "toby"]):
                    send_response(get_random_emojis(emoji_think, randint(10, 20)), channel)

                # default response
                else:
                    chat_help(channel)
            time.sleep(1)
    else:
        print("Connection failed. Exception traceback printed above.")

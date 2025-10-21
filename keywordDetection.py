from os import getenv as env
from dotenv import load_dotenv
import re


load_dotenv()



def hasBadge(badgesList, badgeName):
    try:
        badge = badgesList[badgeName]
        print(badge)
        return (int(badge) > 0.5)
    except TypeError:
        print('hasBadge type error (debuging only)')
        return False
    except Exception as e:
        return False
    

def stripToLeters(string):
    abc = "abcdefghijklmnopqrstuvwxyzæøå"
    text = []
    for i in string.lower():
        if i in abc:
            text.append(i)
        else:
            text.append(" ")
    string = ("".join(text))
    return string


async def icon(msg):
    msgIcon = ""
    message = (" "+stripToLeters(msg.text)+" ")
    print(msg.text[-1:])
    #print("https://discord.gg/fwxZNJy" in msg.text)
    if re.search(f'{env('discord_link')}', msg.text):
        msgIcon = '<img class="msgIcon" src="/SVG/Discord.svg">'
    elif re.search('https://www.twitch.tv/*/clip/', msg.text.lower()):
        msgIcon = '<img class="msgIcon" src="/SVG/Clip.svg">'
    elif re.search(' job ', message):
        msgIcon = '<img class="msgIcon" src="/SVG/application.svg">'
    elif re.search('j\*b', msg.text.lower()):
        msgIcon = '<img class="msgIcon" src="/SVG/application.svg">'
    elif re.search('application', message):
        msgIcon = '<img class="msgIcon" src="/SVG/application.svg">'
    elif re.search(' trans*', message):
        msgIcon = '<img class="msgIcon" src="SVG/Transformer.svg">'
    elif re.search(' optimus pri.e ', message):
        msgIcon = '<img class="msgIcon" src="SVG/Transformer.svg">'
    elif re.search(' still cis ', message):
        msgIcon = '<img class="msgIcon" src="SVG/Transformer.svg">'
    elif re.search(' transphobe', message):
        msgIcon = '<img class="msgIcon" src="SVG/Decepticon.svg">'
    elif re.search(' decepticon', message):
        msgIcon = '<img class="msgIcon" src="SVG/Decepticon.svg">'
    elif re.search(' fish*', message):
        msgIcon = '<img class="msgIcon" src="SVG/Fish.svg">'
    elif re.search(' fisk*', message):
        msgIcon = '<img class="msgIcon" src="SVG/Fish.svg">'
    elif (hasBadge(msg.user['user_badges'], 'staff')):
        msgIcon = '<img class="msgIcon" src="/SVG/Staff.svg">'
    elif (hasBadge(msg.user['user_badges'], 'bot-badge')):
        msgIcon = '<img class="msgIcon" src="/SVG/Bot.svg">'
    elif (hasBadge(msg.user['user_badges'], 'artist-badge')):
        msgIcon = '<img class="msgIcon" src="/SVG/Artist.svg">'
    elif (msg.user['is_mod']):
        msgIcon = '<img class="msgIcon" src="/SVG/Mod.svg">'
    elif (msg.text[-2:] == "!?"):
        msgIcon = '<img class="msgIcon" src="SVG/exclamation-question-mark.svg">'
    elif (msg.text[-1:] == "!"):
        msgIcon = '<img class="msgIcon" src="/SVG/exclamation-mark.svg">'
    elif (msg.text[-1:] == "?"):
        msgIcon = '<img class="msgIcon" src="/SVG/question-mark.svg">'
    return msgIcon
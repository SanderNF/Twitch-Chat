from os import getenv as env
import os
from dotenv import load_dotenv
from random import randrange
from reformat import reformatMsg
from deleteMsg import deleteById, deleteByUser
from GlobalStore import Global



import json

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from twitchAPI.helper import first
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent
from obs_squish import trigger_squish, half_height_temporarily

import asyncio, threading


load_dotenv()
APP_ID = env('client_id')
APP_SECRET = env('client_secret')
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_READ_REDEMPTIONS]
TARGET_CHANNEL = env('channel_name')
#print(APP_ID)



REWARD_TITLE = "SQUISH THE CATGIRL INTO 4:3"  # must match reward name EXACTLY


async def on_channel_point_redeem(event: ChannelPointsCustomRewardRedemptionAddEvent):
    print(f"redemed: {event.event.reward.title}")
    if event.event.reward.title == REWARD_TITLE:
        print("Channel point redeemed: triggering squish")
        half_height_temporarily()



# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here

    



# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    

    
    
    class z:
        text = msg.text
        emotes = msg.emotes
        chat = msg.chat
        id = msg.id
        source_id = msg.source_id
        user = {
        'user_badge_info':msg.user.badge_info,
        'user_badges':msg.user.badges,
        'user_source_badge_info':msg.user.source_badge_info,
        'user_source_badges':msg.user.source_badges,
        'user_chat':msg.user.chat,
        'user_color':msg.user.color,
        'user_display_name':msg.user.display_name,
        'is_mod':msg.user.mod,
        'is_vip':msg.user.vip,
        'is_turbo':msg.user.turbo,
        'is_subscriber':msg.user.subscriber,
        'user_user_type':msg.user.user_type,
        'user_name':msg.user.name
        }
    print(z.user['user_badges'])
    #print(z.user)
    await reformatMsg(z, Global.GlobalBadges, Global.ChannelBadges)
    

async def on_message_delete(msg: ChatMessage):
    print(msg)
    msgId = msg.message_id
    deleteById(msgId)
async def on_chat_cleared(event: ChatEvent):
    print(f'purgeing {event.user_name}')
    deleteByUser(event.user_name)





    


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')

async def EventSubRedems():
    print("starting eventsub redems")
    eventsub = Global.eventsub
    user = Global.user
    try:
        eventsub.start()

        await eventsub.listen_channel_points_custom_reward_redemption_add(
            broadcaster_user_id=user.id,
            callback=on_channel_point_redeem
        )
        print("eventsub redems: runing")
    except Exception as e:
        print("failed to add channel points redemption:")
        print(e)

async def startEventSubRedems():
    threading.Thread(
        target=asyncio.run,
        daemon=True,
        args=[EventSubRedems()]
    ).start()


# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
    user = await first(twitch.get_users(logins=TARGET_CHANNEL))
    print(user)


    eventsub = EventSubWebsocket(twitch)
    

    # create chat instance
    chat = await Chat(twitch, no_shared_chat_messages=False)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE_DELETE, on_message_delete)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.CHAT_CLEARED, on_chat_cleared)
    # listen to channel subscriptions
    # chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    
    

    # we are done with our setup, lets start this bot up!
    chat.start()

    await startEventSubRedems()
    

    Global.twitch = twitch
    Global.user = user
    Global.eventsub = eventsub
    Global.GlobalBadges.append(await Twitch.get_global_chat_badges(twitch)) 
    Global.ChannelBadges.append(await Twitch.get_chat_badges(twitch,user.id))

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop \n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        eventsub.stop()
        await twitch.close()








# lets run our setup
asyncio.run(run())
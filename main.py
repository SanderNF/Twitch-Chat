from os import getenv as env
import os
from dotenv import load_dotenv


from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio


load_dotenv()
APP_ID = env('app_id')
APP_SECRET = env('app_secret')
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = 'sandernf__'
print(APP_ID)


MesageList = []

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    message = msg.text
    print(msg.emotes)
    EmotesList = []
    for i in msg.emotes:
        ii = msg.emotes[i]
        print('stage I')
        print(i)
        print(ii)
        for j in ii:
            print('stage J')
            print(j)
            #jj = ii[j]
            #print(jj)

            print(j['start_position'])
            #message[j['start_position']] = '§'
            #message[j['end_position']] = '§'
            #message.split('§')
            #message = f'{message[0]} <img></img> {message[2]}'
            a = int(j['start_position'])
            b = int(j['end_position'])+1
            c = b-a
            
            EmotesList.append([a,i])
            start = message[0:a]
            end = message[(b):]
            print(start)
            print(end)
            message = f'{start}{'§'*c}{end}'






    def x(e):
        return (e[0])
    EmotesList.sort(key=x)
    print(EmotesList)



    print(message)
    MesageList.append(message)

    print(f'in {msg.room.name}, {msg.user.name} said: {message}, emotes: {msg.emotes}')


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')




# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation



    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


# lets run our setup
asyncio.run(run())
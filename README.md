# Twitch-Chat
A web server that reads twitch chat and displays whit custom styling


# setup 
Make sure Python is installed

In CMD run 
```batch
pip install twitchAPI
pip install dotenv
pip install asyncio
```

at: https://dev.twitch.tv/console \
Create a Application set to Confidential 

From Your dev dashboard grab your "Client ID" and "Client Secret"

Create a flie called ".env" and insert your "Client ID" and "Client Secret" like this:

```dotenv
app_id=<your-app-id>
app_secret=<your-app-secret>
channel_name=<your-channel-name>
```

Run "start.bat" 
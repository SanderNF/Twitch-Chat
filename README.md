# Twitch-Chat
A simple application that reads twitch chat and displays it in a broweser with aditional CSS styling


# setup 
Make sure Python is installed

at: https://dev.twitch.tv/console \
Create a Application set to Confidential 

From Your dev dashboard grab your `Client ID` and `Client Secret`

Create a flie called `.env` and format it like this:

```dotenv
app_id=<your-app-id>
app_secret=<your-app-secret>
channel_name=<your-channel-name>
```

Run `Quick_setup.ps1` 
> [!NOTE]
> this will setup the venv and prompt to install as a startup program

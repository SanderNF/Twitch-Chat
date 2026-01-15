
hap run .venv/bin/python web_server.py -n "twitch-chat-web-server"
hap run .venv/bin/python main.py -n "twitch-chat-api-module"
hap logs -f "twitch-chat-api-module"
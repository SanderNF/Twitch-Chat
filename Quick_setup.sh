
if [[ -z "${ENV_Twitch_ID}" ]]; then
    read -r -p "Twitch client id: " Twitch_ID
else
    Twitch_ID="${ENV_Twitch_ID}"
fi
if [[ -z "${ENV_Twitch_Secret}" ]]; then
    echo "this will be hidden when you type"
    read -r -s -p "Twitch client secret: " Twitch_Secret
else
    Twitch_Secret="${ENV_Twitch_Secret}"
fi

if [[ -z "${ENV_Channel_Name}" ]]; then
    read -r -p "Twitch channel name: " Channel_Name
else
    Channel_Name="${ENV_Channel_Name}"
fi
if [[ -z "${ENV_Max_Large_Emotes}" ]]; then
    read -r -p "Max number of large emotes: " Max_Large_Emotes
else
    Max_Large_Emotes="${ENV_Max_Large_Emotes}"
fi  
if [[ -z "${ENV_Discord_Link}" ]]; then
    read -r -p "Your discord invite link: " Discord_Link
else
    Discord_Link="${ENV_Discord_Link}"
fi

BASEDIR=$(dirname $0)
echo "Script location: ${PWD}"

python -m venv "${PWD}/.venv"

pip install hapless

.venv/bin/pip install -r requirements.txt

(
    echo client_id=$Twitch_ID
    echo client_secret=$Twitch_Secret
    echo channel_name=$Channel_Name
    echo max_large_emotes=$Max_Large_Emotes
    echo discord_link=$Discord_Link
) > .env
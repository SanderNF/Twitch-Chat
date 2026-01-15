# input1="USER INPUT"
read -p "Twitch client id: " input1
# input2="USER INPUT"
read -p "Twitch client secret: " input2
# input3="USER INPUT"
read -p "your channel name: " input3
# input4="USER INPUT"
read -p "max number big emotes: " input4
# input5="USER INPUT"
read -p "Your discord invite link: " input5


BASEDIR=$(dirname $0)
echo "Script location: ${PWD}"

python -m venv "${PWD}/.venv"

pip install hapless

.venv/bin/pip install -r requirements.txt

(
    echo client_id=$input1
    echo client_secret=$input2
    echo channel_name=$Input3
    echo max_large_emotes=$Input4
    echo discord_link=$Input5
) > .env
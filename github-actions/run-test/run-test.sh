echo "Twitch client id: $ENV_Twitch_ID"
curl --location 'https://id.twitch.tv/oauth2/device' \
    --form "client_id=\"$ENV_Twitch_ID\"" \
    --form 'scopes="chat:read chat:edit"' | jq -r '. | "\(.device_code) \(.user_code) \(.verification_uri) \(.expires_in)"' > var.txt

cat var.txt
read var1 var2 var3 var4 < var.txt
echo "Device code: $var1"
echo "User code: $var2"
echo "Verification URI: $var3"
echo "Expires in: $var4 seconds"

WEBHOOK_URL="https://discord.com/api/webhooks/1471123147175624785/4dqTstPouOnMF_yjPt3qM5hthybu6cNujAGjL_KI9um362oKuXp81yxp5Xooe0bzaoIV"
BODY="{\"username\": \"test\", \"content\": \"code:\n\`\`\`\n$var2\n\`\`\`\n>>> **or click [here]($var3 )**\n-# expires in $var4 seconds\"}"
echo "Webhook body: $BODY"
curl \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  $WEBHOOK_URL

waiting=true
while $waiting; do
    sleep 5
    RESPONSE=$(curl --location 'https://id.twitch.tv/oauth2/token' \
    --form "client_id=\"$ENV_Twitch_ID\"" \
    --form 'scopes="chat:read chat:edit"' \
    --form "device_code=\"$var1\"" \
    --form 'grant_type="urn:ietf:params:oauth:grant-type:device_code"')
    echo "Response from Twitch token endpoint: $RESPONSE"
    if [[ "$RESPONSE" == *"access_token"* ]]; then
        echo "$RESPONSE" | jq -r '. | "\(.device_code) \(.user_code) \(.verification_uri) \(.expires_in)"' > user-auth.txt
        read access_token refresh_token < user-auth.txt
        export access_token="$access_token"
        export refresh_token="$refresh_token"
        echo "Authentication successful!"
        break
    elif [[ "$RESPONSE" == *"authorization_pending"* ]]; then
        echo "Authorization pending, waiting..."
    elif [[ "$RESPONSE" == *"missing device_code"* ]]; then
        echo "Error: missing device_code."
    else
        echo "Error during authentication: $RESPONSE"
        exit 1
    fi
done

export ENV_Channel_Name="sandernf__"
export ENV_Max_Large_Emotes="5"
export ENV_Discord_Link="no"

sh ./../../Quick_setup.sh
./../../.venv/bin/python ./../../main.py 
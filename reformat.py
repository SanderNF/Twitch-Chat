import json



class test:
    text = "test  arelevFISH    arelevFISH   and  arelevHeart    arelevHeart   potato" 
    emotes = {'emotesv2_87368d5d04464b66bd69f761b0116775': [{'start_position': '38', 'end_position': '48'}, {'start_position': '53', 'end_position': '63'}], 'emotesv2_09b2c36f1d6f490a9fdca84e61aad090': [{'start_position': '6', 'end_position': '15'}, {'start_position': '20', 'end_position': '29'}]} 
    chat = '<twitchAPI.chat.Chat object at 0x0000023201EA3A10>' 
    id = 'edb49e56-2fe8-4024-81ff-32d526c0afce'
    user = {'user_badge_info': None, 'user_badges': {'broadcaster': '1', 'glhf-pledge': '1'}, 'user_chat': '<twitchAPI.chat.Chat object at 0x00000244FE60B8C0>', 'user_color': '#2E8B57', 'user_display_name': 'sandernf__', 'user_mod': False, 'user_vip': False, 'user_turbo': False, 'user_subscriber': False, 'user_user_type': None, 'user_name': 'sandernf__'}


def reformatMsg(msg):
    EmotesList = []
    try:
        for i in msg.emotes:
            print(i)
            ii = msg.emotes[i]
            for j in ii:
                EmotesList.append([j['start_position'],j['end_position'],i])
    except TypeError:
        print('no emotes')
    except Exception as e:
        print(f'Shits Fucked: {e}')
    
    print(EmotesList)

    def x(e):
        a = int(e[0])
        print(e, a)
        return a
    EmotesList.sort(key=x)
    print(f'Sorted list \n {EmotesList}')


    out = [
            '<div>',
            f'<code style="color:{msg.user['user_color']};">{msg.user['user_display_name']}</code>',
            '<p>'
           ]
    end = [
            '</p>',
            '</div>'
           ]
    EmoteIndex = 0
    EmoteSpace = False
    tempMsg = []
    for i in range(len(msg.text)):
        
        if EmoteIndex < len(EmotesList):
            print(f' index: {EmoteIndex , len(EmotesList)}')
            if int(i) >= int(EmotesList[EmoteIndex][0]):
                print('emote')
                EmoteSpace = True
                if len(tempMsg)!=0:
                    out.append("".join(tempMsg))
                    a = EmotesList[EmoteIndex][2]
                    EmoteElement = str(f'<img alt="Emote" class="chat-image chat-line__message--emote" src="https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/1.0" srcset="https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/1.0 1x,https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/2.0 2x,https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/3.0 4x">')
                    print(EmoteElement)
                    out.append(EmoteElement)
                    tempMsg = []
                if i >= int(EmotesList[EmoteIndex][1]):
                    print('end emote')
                    EmoteSpace = False
                    EmoteIndex += 1

            else:
                tempMsg.append(msg.text[i])
        else:
            tempMsg.append(msg.text[i])
        print(i)
    out.append("".join(tempMsg))
    out.append("".join(end))
    print(f'<code style="color:{msg.user['user_color']};">{msg.user['user_display_name']}</code>:')
    print(" ".join(out))
    with open('Chat.json', 'r') as f:
        b = json.load(f)
    print(b)
    b.append(" ".join(out))
    while len(b) > 5:
        for k in range(len(b)-1):
            b[k] = b[k+1]
        b.pop(len(b)-1)
    with open('Chat.json', 'w', encoding='utf-8') as f:
        json.dump(b, f, ensure_ascii=False, indent=4)
    print(b)


reformatMsg(test)
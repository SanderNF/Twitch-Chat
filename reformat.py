import json



class test:
    text = "test  arelevFISH    arelevFISH   and  arelevHeart    arelevHeart   potato <test>" 
    emotes = {'emotesv2_87368d5d04464b66bd69f761b0116775': [{'start_position': '38', 'end_position': '48'}, {'start_position': '53', 'end_position': '63'}], 'emotesv2_09b2c36f1d6f490a9fdca84e61aad090': [{'start_position': '6', 'end_position': '15'}, {'start_position': '20', 'end_position': '29'}]} 
    chat = '<twitchAPI.chat.Chat object at 0x0000023201EA3A10>' 
    id = 'edb49e56-2fe8-4024-81ff-32d526c0afce'
    user = {'user_badge_info': None, 'user_badges': {'broadcaster': '1', 'glhf-pledge': '1'}, 'user_chat': '<twitchAPI.chat.Chat object at 0x00000244FE60B8C0>', 'user_color': '#2E8B57', 'user_display_name': 'sandernf__', 'user_mod': False, 'user_vip': False, 'user_turbo': False, 'user_subscriber': False, 'user_user_type': None, 'user_name': 'sandernf__'}


    

with open('Chat.json', 'w',  encoding='utf-8') as f:
        json.dump(['<div><code>System</code><p>Chabox Started</p></div>'], f, ensure_ascii=False, indent=4)

def EscapeText(T):
    #print(f'pre Escape: ', T)
    a = []
    for i in T:
        if i == '<':
            a.append('&lt;')
        elif i == '>':
            a.append('&gt;')
        elif i == '&':
            a.append('&amp;')
        elif i == '"':
            a.append('&quot;')
        elif i == "'":
            a.append('&apos;')
        else:
            a.append(i)

    a = ''.join(a)
        
    #print(f'post Escape: ', a)
    return a


def formatBadges(data):
    #print(f'formating badges: {data}')
    out = []
    for i in data:
        j = i
        #print(j)
        out.append(f'<img alt="badge" aria-label="badge" class="chat-badge" src="{j.image_url_1x}" tabindex="0" srcset="{j.image_url_1x} 1x, {j.image_url_2x} 2x, {j.image_url_4x} 4x">')
    return "".join(out)



def reformatMsg(msg, GlobalBadges, ChannelBadges):
    print(msg.text)
    #print(GlobalBadges)
    try:
        Badges = []
        PreBadges = []
        #print('starting badge reading')
        for i in msg.user['user_badges']:
            #print(f'creating badge list: {i}')
            PreBadges.append([i, msg.user['user_badges'][i]])
            Badges.append([])
        #print(PreBadges)
        #print('start scrubing badges')
        for i in range(len(PreBadges)):
            if len(PreBadges[i][0]) <= 0:
                PreBadges[i][0] = 1
                print('fixed one badge value')
        for i in GlobalBadges[0]:
            #print(i)
            for j in range(len(PreBadges)):
                #print(j)
                jj = PreBadges[j][0]
                jjj = int(PreBadges[j][1])-1
                #print(jj)
                #print((i.set_id == jj))
                if (i.set_id == jj):
                    #print(j, jj, jjj)
                    try:
                        #print(i.versions[jjj])
                        Badges[j] = (i.versions[jjj])
                    except Exception as e:
                        print(f'Badge internal error: {e}')
                    #print(Badges)
                #print(GlobalBadges[0][i])
        for i in ChannelBadges[0]:
            #print(i)
            for j in range(len(PreBadges)):
                #print(j)
                jj = PreBadges[j][0]
                jjj = int(PreBadges[j][1])
                #print(jj)
                #print((i.set_id == jj))
                if (i.set_id == jj):
                    #print(j, jj, jjj)
                    #print(i)
                    for k in range(len(i.versions)):
                        kk = i.versions[k]
                        try:
                            #print(kk.id, jjj)
                            if int(kk.id) == (jjj):
                                Badges[j] = kk
                                break
                        except:
                            print('sander you stupid fuck')
                    
                    #print(Badges)
                #print(GlobalBadges[0][i])
        
    except Exception as e:
        print(f'get badges failed: {e}')
    #print(Badges)
    EmotesList = []
    try:
        for i in msg.emotes:
            #print(i)
            ii = msg.emotes[i]
            for j in ii:
                EmotesList.append([j['start_position'],j['end_position'],i])
    except TypeError:
        print('no emotes')
    except Exception as e:
        print(f'Shits Fucked: {e}')
    
    #print(EmotesList)

    def x(e):
        a = int(e[0])
        print(e, a)
        return a
    EmotesList.sort(key=x)
    #print(f'Sorted list \n {EmotesList}')


    out = [
            '<div>',
            f'<code style="color:{msg.user['user_color']};">',
            f'{formatBadges(Badges)}'
            f'{msg.user['user_display_name']}</code>',
            '<p>'
           ]
    end = [
            '</p>',
            '</div>'
           ]
    #print(out)
    EmoteIndex = 0
    EmoteSpace = False
    tempMsg = []
    for i in range(len(msg.text)):
        
        if EmoteIndex < len(EmotesList):
            #print(f' index: {EmoteIndex , len(EmotesList)}')
            if int(i) >= int(EmotesList[EmoteIndex][0]):
                #print('emote')
                if ((EmoteSpace) != True):
                    tempMsg = "".join(tempMsg)
                    out.append(EscapeText(tempMsg))
                    a = EmotesList[EmoteIndex][2]
                    EmoteElement = str(f'<img alt="Emote" class="chat-image chat-line__message--emote" src="https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/1.0" srcset="https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/1.0 1x,https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/2.0 2x,https://static-cdn.jtvnw.net/emoticons/v2/{a}/default/dark/3.0 4x">')
                    #print(EmoteElement)
                    out.append(EmoteElement)
                    tempMsg = []
                EmoteSpace = True
                if i >= int(EmotesList[EmoteIndex][1]):
                    #print('end emote')
                    EmoteSpace = False
                    EmoteIndex += 1

            else:
                tempMsg.append(msg.text[i])
        else:
            tempMsg.append(msg.text[i])
        #print(i)
    out.append(EscapeText("".join(tempMsg)))
    out.append("".join(end))
    #print(f'<code style="color:{msg.user['user_color']};">{msg.user['user_display_name']}</code>:')
    #print(" ".join(out))
    with open('Chat.json', 'r',  encoding='utf-8') as f:
        b = json.load(f)
    #print(b)
    b.append(" ".join(out))
    while len(b) > 5:
        for k in range(len(b)-1):
            b[k] = b[k+1]
        b.pop(len(b)-1)
    try:
        with open('Chat.json', 'w',  encoding='utf-8') as f:
            json.dump(b, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'JSON save failed with error: {e} reseting chat')
        with open('Chat.json', 'w', encoding='utf-8') as f:
            json.dump([f'<p> JSON save failed with error: {e} reseting chat </p>'], f, ensure_ascii=False, indent=4)
    #print(b)


#reformatMsg(test, [])
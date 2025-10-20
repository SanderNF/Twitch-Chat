import json


def deleteById(id):
    with open('Chat.json', 'r',  encoding='utf-8') as f:
        ChatJson = json.load(f)
    for i in range(len(ChatJson)):
        print(f'i: {ChatJson[i]["id"]}')
        if (ChatJson[i]["id"] == id):
            print(f'found msg with id: {i}')
            ChatJson[i]["msg"] = "deleted"
            ChatJson[i]["id"] += "-deleted"

    try:
        with open('Chat.json', 'w',  encoding='utf-8') as f:
            json.dump(ChatJson, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Delete message failed with error: {e} reseting chat')
        with open('Chat.json', 'w', encoding='utf-8') as f:
            json.dump([{"msg":f'<p> Delete message failed with error: {e} reseting chat </p>',"id":"error"}], f, ensure_ascii=False, indent=4)


def deleteByUser(username):
    with open('Chat.json', 'r',  encoding='utf-8') as f:
        ChatJson = json.load(f)
    for i in range(len(ChatJson)):
        print(f'i: {ChatJson[i]["id"]}')
        if (f'{username}</code>' in ChatJson[i]["msg"]):
            print(f'found msg with id: {i}')
            ChatJson[i]["msg"] = "deleted"
            ChatJson[i]["id"] += "-deleted"

    try:
        with open('Chat.json', 'w',  encoding='utf-8') as f:
            json.dump(ChatJson, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Delete message failed with error: {e} reseting chat')
        with open('Chat.json', 'w', encoding='utf-8') as f:
            json.dump([{"msg":f'<p> Delete message failed with error: {e} reseting chat </p>',"id":"error"}], f, ensure_ascii=False, indent=4)


deleteById('none')
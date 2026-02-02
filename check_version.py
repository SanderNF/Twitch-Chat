import json


def runVersionCheck():
    gitVersion = version()
    with open('Chat.json', 'r',  encoding='utf-8') as f:
        b = json.load(f)
    #print(b)
    b.append({"msg":f'<div style="display: flex;"><div class="chatMsg"><code>Curent Git Branch:</code><div class="msgContent"><p>{gitVersion}</p></div></div></div>', "id": "version"})
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


def version():
    try:
        with open('.git/FETCH_HEAD', 'r',  encoding='utf-8') as f:
            return str(f.read(7))
    except FileNotFoundError:
        return "no git HEAD"
    except Exception as err:
        #print(err.__traceback__.__dict__)
        return err
    




if __name__ == "__main__":
    print(version())
    runVersionCheck()
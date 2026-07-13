import json, os


async def runVersionCheck(reply):
    """run to check the curent commit version"""
    gitVersion = version()
    await reply(gitVersion)
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
    """the function for checking the commit version"""
    #gitLog = os.system(f'git log -1')
    gitLog = os.popen(f'git log -1').read()
    #print(gitLog)
    #print(gitLog.split("\n")[0])
    return gitLog.split("\n")[0][:14]
    

async def runStatusCheck(reply):
    """run to check the curent git status"""
    gitStatus = status()
    await reply(gitStatus)
    with open('Chat.json', 'r',  encoding='utf-8') as f:
        b = json.load(f)
    #print(b)
    b.append({"msg":f'<div style="display: flex;"><div class="chatMsg"><code>Curent Git Status:</code><div class="msgContent"><p>{gitStatus}</p></div></div></div>', "id": "status"})
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

def status():
    """the function for checking the git status"""
    os.system(f'git fetch')
    gitStatus = os.popen(f'git status').read()
    #print(gitLog)
    #print(gitLog.split("\n")[0])
    return "\n".join(gitStatus.split("\n")[:2][:14])


if __name__ == "__main__":
    print()
    print(version())
    runVersionCheck()
    print(status())
    runStatusCheck()
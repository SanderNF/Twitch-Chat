import os, time
dir_path = os.path.dirname(os.path.realpath(__file__))

startTime = time.time()

def runUpdate(callbackFile):
    if time.time()-startTime < 5:
        print("Update called too soon")
        return
    print("running update")
    print(f"time since start {time.time()-startTime}")
    os.system("git fetch")
    os.system("git pull")
    #os.system("ls")
    print(dir_path)
    os.system(f'"{dir_path}/Scripts/python.exe" {callbackFile}')
    os.system(f'"{dir_path}/.venv/bin/python" {callbackFile}')
    exit()

    




if __name__ == "__main__":
    runUpdate("gitUpdate.py")
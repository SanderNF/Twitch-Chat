import os, time
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
    os.system("python3 gitUpdate.py")
    exit()

    




if __name__ == "__main__":
    runUpdate("gitUpdate.py")
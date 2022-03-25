import os

def Count(direct="", extention=".py", topLayer = True):
    localCount = 0

    if direct == "":
        allFiles = os.listdir()
    else:
        allFiles = os.listdir(direct)

    for file in allFiles:
        if "." in file:
            if extention in file and not "__" in file and file != "countLines.py":

                if direct == "":
                    f = open(f"{file}", "r")
                else:
                    f = open(f"{direct}/{file}", "r")

                numLines = len(f.readlines())

                print(str(numLines) + " in " + str(file))
                localCount += numLines
                f.close()

        elif not "__" in file:
            if direct == "":
                localCount += Count(file, topLayer=False)
            else:
                localCount += Count(direct + "/" + file, topLayer=False)
    
    if topLayer:
        print(f" - TOTAL = {localCount}")

    return localCount

Count(extention=".py")
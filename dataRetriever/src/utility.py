def info(message):
    print("[INFO] %s" % message)


def error(message):
    print("[ERROR] %s" % message)


def warn(message):
    print("[WARN] %s" % message)


def writeToFile(Name, Body):
    statusFile = open('status.json', 'w')
    statusFile.write(statusJson)
    statusFile.close()

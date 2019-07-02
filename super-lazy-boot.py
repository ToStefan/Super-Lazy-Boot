import sys

from writers import writer
from generators import setSettings
from utils import clear

classMap = {}
enumMap = {}
settingsMap = {}

def main():
    parser()
    print("")
    syntaxCheck()
    print("")
    confirm = raw_input("y/n >> ")
    if(confirm == "y" or confirm == "Y"):
        setSettings(settingsMap)
        writer(classMap, enumMap)
    else:
        pass

def syntaxCheck():
    print(">> Syntax check...\n")

    def classCheck():
        for key, values in classMap.items():
            print("    " + key + " (class)")
            for value in values:
                print("      -> " + value.split(":")[0] + " " + value.split(":")[1])
            print("")

    def enumCheck():
        for key, values in enumMap.items():
            print("    " + key + " (enum)")
            for value in values:
                print("      -> " + value)
            print("")

    def settingsCheck():
        for key, value in settingsMap.items():
            print("    " + key + " -> " + value[0])
            if(key != "security"):
                try:
                    eval(value[0].capitalize())
                except NameError as e:
                    raise SyntaxError(key + " value must be True or False")
            elif(key == "security"):
                if(value[0] != "jwt" and value[0] != "basic"):
                    raise SyntaxError(key + " authentication must be jwt or basic")
        print("")

    try:
        settingsCheck()
        classCheck()
        enumCheck()
    except SyntaxError as e:
        print("        ERROR: " + str(e))
        raise SystemExit(0)


def parser():
    with open(sys.argv[1], 'r') as file:
        data = file.read().replace(" ", "").replace("\n", "").replace("\t", "").rstrip()

    classes = data.split("Class{")[1].split("}")[0].split(",")
    print(">> Parsing classes...")
    for eachClass in classes:
        if(eachClass == ""):
            print("    Comma at end of Class declaration detected")
        else:
            eachClass = eachClass.split("->")
            classMap[eachClass[0]] = eachClass[1:]

    enums = data.split("Enum{")[1].split("}")[0].split(",")
    print(">> Parsing enums...")
    for eachEnum in enums:
        if(eachEnum == ""):
            print("    Comma at end of Enum declaration detected")
        else:
            eachEnum = eachEnum.split("->")
            enumMap[eachEnum[0]] = eachEnum[1:]

    settings = data.split("Settings{")[1].split("}")[0].split(",")
    print(">> Parsing settings...")
    for eachSetting in settings:
        if(eachSetting == ""):
            print("    Comma at end of Settings declaration detected")
        else:
            eachSetting = eachSetting.split(":")
            settingsMap[eachSetting[0]] = eachSetting[1:]

if __name__ == "__main__":
    clear()
    main()
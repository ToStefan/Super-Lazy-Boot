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
    print(">> Syntax check...")

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
                    raise SyntaxError(key + " value must be true or false")
            elif(key == "security"):
                if(value[0] != "jwt" and value[0] != "basic"):
                    raise SyntaxError(key + " authentication must be 'jwt' or 'basic'")
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

    def classParser(data):
        try:
            classes = data.split("Class{")[1].split("}")[0].split(",")
            for eachClass in classes:
                if(eachClass == ""):
                    print("    INFO: Comma at end of class declaration detected")
                else:
                    eachClass = eachClass.split("->")
                    classMap[eachClass[0]] = eachClass[1:]
        except IndexError:
            print("    INFO: No classes specified")
            raise SystemExit(0)
        

    def enumParser(data):
        try:
            enums = data.split("Enum{")[1].split("}")[0].split(",")
            for eachEnum in enums:
                if(eachEnum == ""):
                    print("    INFO: Comma at end of enum declaration detected")
                else:
                    eachEnum = eachEnum.split("->")
                    enumMap[eachEnum[0]] = eachEnum[1:]
        except IndexError:
            print("    INFO: No enums specified")
        

    def settingsParser(data):
        try:
            settings = data.split("Settings{")[1].split("}")[0].split(",")
            if(settings[0] == ""):
                print("    INFO: No settings specified")
            else:
                for eachSetting in settings:
                    if(eachSetting == ""):
                        print("    INFO: Comma at end of settings declaration detected")
                    else:
                        eachSetting = eachSetting.split(":")
                        settingsMap[eachSetting[0]] = eachSetting[1:]
        except IndexError:
            print("    INFO: No settings specified")

    print(">> Parsing classes...")
    classParser(data)
    print(">> Parsing enums...")
    enumParser(data)
    print(">> Parsing settings...")
    settingsParser(data)
    

if __name__ == "__main__":
    clear()
    main()
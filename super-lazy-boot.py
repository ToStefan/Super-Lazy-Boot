import sys

from generators import generator
from utils import clear

classMap = {}
enumMap = {}
settingsMap = {}

def syntaxCheck():
    pass

def parser():

    with open(sys.argv[1], 'r') as file:
        data = file.read().replace(" ", "").replace("\n", "").replace("\t", "").rstrip()

    classes = data.split("Class{")[1].split("}")[0].split(",")
    print(">> Parsing classes...")
    for eachClass in classes:
        eachClass = eachClass.split("->")
        classMap[eachClass[0]] = eachClass[1:]

    enums = data.split("Enum{")[1].split("}")[0].split(",")
    print(">> Parsing enums...")
    for eachEnum in enums:
        eachEnum = eachEnum.split("->")
        enumMap[eachEnum[0]] = eachEnum[1:]

    settings = data.split("Settings{")[1].split("}")[0].split(",")
    print(">> Parsin settings...\n")
    for eachSetting in settings:
        eachSetting = eachSetting.split(":")
        settingsMap[eachSetting[0]] = eachSetting[1]

if __name__ == "__main__":
    clear()
    parser()
    generator(classMap, enumMap, settingsMap)
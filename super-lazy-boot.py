import fileinput
import os
import sys

from generators import generateMapperInteface, generateEntities, generateRepositories, generateDtos, \
generateMappers, generateServiceInterface, generateServices, generateControllers, generateEnumeration
from structure import generateProject
from utils import getPrimaryKeyType

classMap = {}
enumMap = {}
lombok = False

def syntaxCheck():
    pass

def parser():

    with open(sys.argv[1], 'r') as file:
        data = file.read().replace(" ", "").replace("\n", "").replace("\t", "").rstrip()

    classes = data.split("Class{")[1].split("}")[0].split(",")
    for eachClass in classes:
        eachClass = eachClass.split("->")
        classMap[eachClass[0]] = eachClass[1:]

    enums = data.split("Enum{")[1].split("}")[0].split(",")
    for eachEnum in enums:
        eachEnum = eachEnum.split("->")
        enumMap[eachEnum[0]] = eachEnum[1:]

    settings = data.split("Settings{")[1].split("}")[0].split(",")
    for eachSetting in settings:
        eachSetting = eachSetting.split(":")
        if(eachSetting[0] == "lombok"):
            global lombok
            lombok = eachSetting[1].capitalize()

def generateMain():
    generateProject()
    generateMapperInteface()

    for key, values in classMap.items():
        generateEntities(key, values)
        generateRepositories(key, getPrimaryKeyType(values))
        generateDtos(key, values)
        generateMappers(key, values)
        generateServiceInterface(key, values)
        generateServices(key, values)
        generateControllers(key, values)
        print("")

    for key, values in enumMap.items():
        generateEnumeration(key, values)


if __name__ == "__main__":
    os.system("cls")    
    parser()
    generateMain()
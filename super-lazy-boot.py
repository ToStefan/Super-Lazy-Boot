import fileinput
import os

from generators import generateMapperInteface, generateEntities, generateRepositories, generateDtos, \
generateMappers, generateServiceInterface, generateServices, generateControllers, generateEnumeration
from structure import generateProject
from utils import getPrimaryKeyType

def generateMain():
    generateProject()
    generateMapperInteface()
    for line in fileinput.input():
        data = line.replace(" ", "").rstrip().split("->")
        classEnum = data[0].split(":")
        if(classEnum[0] == "enum"):
            enumValues = []
            for enum in data[1:]:
                enumValues.append(enum)
            generateEnumeration(classEnum[1], enumValues)
        else:
            attributes = []
            for el in data[1:]:
                attributes.append(el)

            generateEntities(classEnum[1], attributes)
            generateRepositories(classEnum[1], getPrimaryKeyType(attributes))
            generateDtos(classEnum[1], attributes)
            generateMappers(classEnum[1], attributes)
            generateServiceInterface(classEnum[1], attributes)
            generateServices(classEnum[1], attributes)
            generateControllers(classEnum[1], attributes)
            print("")

if __name__ == "__main__":
    os.system("cls")    
    generateMain()
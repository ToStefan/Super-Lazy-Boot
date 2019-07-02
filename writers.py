import structure
import generators

from utils import getPrimaryKeyType

writeReadType = "w+"

def writer(classMap, enumMap):

	structure.generateProject()
	print(">> Generating Mapper Interface...\n")
	mapperInterface = generators.generateMapperInteface()
	write(structure.mapper + "/Mapper.java", mapperInterface)

	for key, values in classMap.items():
		print(">> Generating class: {key} -> attributes: {values}".format(key=key, values=values))
		javaEntity = generators.generateEntities(key, values)
		write(structure.entity + key + ".java", javaEntity)
		print(">> Generating repository for " + key)
		javaRepository = generators.generateRepositories(key, getPrimaryKeyType(values))
		write(structure.repository + key + "Repository.java", javaRepository)
		print(">> Generating service interface for " + key)
		serviceInterface = generators.generateServiceInterface(key, values)
		write(structure.service + key + "Service.java", serviceInterface)
		print(">> Generating service for " + key)
		serviceImpl = generators.generateService(key, values)
		write(structure.serviceImpl + key + "ServiceImpl.java", serviceImpl)
		print(">> Generating controller for " + key)
		controllerClass = generators.generateControllers(key, values)
		write(structure.controller + key + "Controller.java", controllerClass)
		print(">> Generating DTO: {key}DTO -> attributes: {values}".format(key=key, values=values))
		javaDto = generators.generateDtos(key, values)
		write(structure.dto + key + "DTO.java", javaDto)
		print(">> Generating mapper for " + key)
		mapperClass = generators.generateMappers(key, values)
		write(structure.mapper + key + "Mapper.java", mapperClass)
		print("")

	for key, values in enumMap.items():
		print(">> Generating enum: " + key)
		javaEnum = generators.generateEnumeration(key, values)
		write(structure.entity + key + ".java", javaEnum)


def write(fileLocation, content):
	file = open(fileLocation, writeReadType)
	file.write(content)
	file.close()
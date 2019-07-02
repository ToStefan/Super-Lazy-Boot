import structure
import generators

from utils import getPrimaryKeyType

writeReadType = "w+"


def writer(classMap, enumMap):

	structure.generateProject()
	mapperInterface = generators.generateMapperInteface()
	write(structure.mapper + "/Mapper.java", mapperInterface)

	for key, values in classMap.items():
		javaEntity = generators.generateEntities(key, values)
		write(structure.entity + key + ".java", javaEntity)
		javaRepository = generators.generateRepositories(key, getPrimaryKeyType(values))
		write(structure.repository + key + "Repository.java", javaRepository)
		serviceInterface = generators.generateServiceInterface(key, values)
		write(structure.service + key + "Service.java", serviceInterface)
		serviceImpl = generators.generateService(key, values)
		write(structure.serviceImpl + key + "ServiceImpl.java", serviceImpl)
		controllerClass = generators.generateControllers(key, values)
		write(structure.controller + key + "Controller.java", controllerClass)
		javaDto = generators.generateDtos(key, values)
		write(structure.dto + key + "DTO.java", javaDto)
		mapperClass = generators.generateMappers(key, values)
		write(structure.mapper + key + "Mapper.java", mapperClass)
		print("")

	for key, values in enumMap.items():
		javaEnum = generators.generateEnumeration(key, values)
		write(structure.entity + key + ".java", javaEnum)


def write(fileLocation, content):
	file = open(fileLocation, writeReadType)
	file.write(content)
	file.close()
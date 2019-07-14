import structure
import generators

from utils import get_primary_key_type

write_read_type = "w+"

def writer(class_map, enum_map):

	structure.generate_project()
	print(">> Generating Mapper Interface...\n")
	mapperInterface = generators.generate_mapper_inteface()
	write(structure.mapper + "/Mapper.java", mapperInterface)

	for key, values in enum_map.items():
		print(">> Generating enum: " + key)
		javaEnum = generators.generate_enumeration(key, values)
		write(structure.entity + key + ".java", javaEnum)


	for key, values in class_map.items():
		print(">> Generating class: {key} -> attributes: {values}".format(key=key, values=values))
		java_entity = generators.generate_entities(key, values)
		write(structure.entity + key + ".java", java_entity)
		print(">> Generating repository for " + key)
		java_repository = generators.generate_repositories(key, get_primary_key_type(values))
		write(structure.repository + key + "Repository.java", java_repository)
		print(">> Generating service interface for " + key)
		service_interface = generators.generate_service_interface(key, values)
		write(structure.service + key + "Service.java", service_interface)
		print(">> Generating service for " + key)
		service_impl = generators.generate_service(key, values)
		write(structure.service_impl + key + "ServiceImpl.java", service_impl)
		print(">> Generating controller for " + key)
		controller_class = generators.generate_controllers(key, values)
		write(structure.controller + key + "Controller.java", controller_class)
		print(">> Generating DTO: {key}DTO -> attributes: {values}".format(key=key, values=values))
		enums_import = generators.generate_enums_import(key, class_map, enum_map)
		java_dto = generators.generate_dtos(key, values, enums_import)
		write(structure.dto + key + "DTO.java", java_dto)
		print(">> Generating mapper for " + key)
		mapper_class = generators.generate_mappers(key, values)
		write(structure.mapper + key + "Mapper.java", mapper_class)
		print("")

def write(file_location, content):
	file = open(file_location, write_read_type)
	file.write(content)
	file.close()
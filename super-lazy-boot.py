import sys
import generators
from utils import *

class_list_of_tupples = []
enum_list_of_tupples = []
settings_map = {}

def parse_classes(classes_json_list):
    for each in classes_json_list:
        class_name = each["name"]
        primary_key = ""
        atributes = []
        for attr in (each["atributes"]):
            atributes.append(attr + ":" + each["atributes"][attr].replace("ENUM_", "").replace("CLASS_", ""))
            if(attr == each["primaryKey"]): primary_key = each["atributes"][attr]
        class_tupple = (class_name, primary_key, atributes)
        class_list_of_tupples.append(class_tupple)

def parse_enums(enums_json_list):
    for each in enums_json_list:
        enum_tupple = (each["name"], each["values"])
        enum_list_of_tupples.append(enum_tupple)

def parser():
    global settings_map
    json_model = load_json(sys.argv[1])
    for each in json_model:
        if(each["type"] == "Class"):
            parse_classes(each["classes"])
        if(each["type"] == "Enum"):
            parse_enums(each["enums"])
        if(each["type"] == "Settings"):
            settings_map = each["settings"]

def generator():
    lombok = settings_map["lombok"]
    root_package = settings_map["rootPackage"]
    root_package_path = root_package.replace(".", "/")

    print("... GENERATING >> project structure")
    generators.generate_project(root_package_path)

    print("... GENERATING >> mapper interface")
    mapper_interface = generators.generate_mapper_inteface(root_package)
    write(switch_package("mapper", root_package_path) + "/Mapper.java", mapper_interface)

    for enum in enum_list_of_tupples:
        print("... GENERATING >> Enum (" + enum[0] + ")")
        javaEnum = generators.generate_enumeration(root_package, enum[0], enum[1])
        write(switch_package("entity", root_package_path) + enum[0] + ".java", javaEnum)

    for each in class_list_of_tupples:
        print("\n... GENERATING >> Entity (" + each[0] + ")")
        java_entity = generators.generate_entities(root_package, lombok, each[0], each[2])
        write(switch_package("entity", root_package_path) + each[0] + ".java", java_entity)

        print("... GENERATING >> " + each[0] + "Repository")
        java_repository = generators.generate_repositories(root_package, each[0], each[1])
        write(switch_package("repository", root_package_path) + each[0] + "Repository.java", java_repository)

        print("... GENERATING >> " + each[0] + "Service")
        service_interface = generators.generate_service_interface(root_package, each[0], each[2])
        write(switch_package("service", root_package_path) + each[0] + "Service.java", service_interface)

        print("... GENERATING >> Implementation of " + each[0] + "Service")
        service_impl = generators.generate_service(root_package, lombok, each[0], each[2])
        write(switch_package("service_impl", root_package_path) + each[0] + "ServiceImpl.java", service_impl)

        print("... GENERATING >> " + each[0] + "Controller")
        controller_class = generators.generate_controllers(root_package, lombok, each[0], each[2])
        write(switch_package("controller", root_package_path) + each[0] + "Controller.java", controller_class)

        print("... GENERATING >> DTO (" + each[0] + ")")
        java_dto = generators.generate_dtos(root_package, lombok, each[0], each[2])
        write(switch_package("dto", root_package_path) + each[0] + "DTO.java", java_dto)

        print("... GENERATING >> " + each[0] + "Mapper")
        mapper_class = generators.generate_mappers(root_package, each[0], each[2])
        write(switch_package("mapper", root_package_path) + each[0] + "Mapper.java", mapper_class)  

if __name__ == "__main__":
    clear()
    parser()
    generator()
import sys
from utils import clear, generate_project, write, set_packages, get_file_loc
from json_parser import parser
from templates import *

CLASSES = {} # key = class name, value = list of tupples (each tupple = each attribute of class), n = 8
ENUMS = [] # list of tupples (enum_name, list of enum values), n = 2
SETTINGS = {} # key = setting, value = value

if __name__ == "__main__":
    clear()
    SETTINGS, ENUMS, CLASSES = parser(sys.argv[1])

    lombok = SETTINGS["lombok"]
    root_package = SETTINGS["rootPackage"]
    root_package_path = root_package.replace(".", "/")
    collection = SETTINGS["serviceCollection"].split(":")[0]
    collection_impl = SETTINGS["serviceCollection"].split(":")[1]

    set_packages(root_package_path)
    generate_project()
    
    write(get_file_loc("mapper", "Mapper"), mapper_interface_template(root_package, collection))

    for enum in ENUMS:
        print("GENERATING ... Enum: " + enum[0] + " / enum values: " + ", ".join(enum[1]))
        write(get_file_loc("entity", enum[0]), generate_enumeration(root_package, enum[0], enum[1]))

    for each in CLASSES.items():
        e = each[0]
        print("\nEntity: " + e)
        atts = ""
        for att in each[1]:
            atts = atts + att[0] + " / "
        print("Attributes: " + atts)

        print("GENERATING ... Entity")
        write(get_file_loc("entity", e), generate_entity(root_package, e, each[1], lombok))

        print("GENERATING ... Repository")
        write(get_file_loc("repository", e + "Repository"), repository_template(root_package, e, "Long"))

        print("GENERATING ... Service")
        write(get_file_loc("service", e + "Service"), service_template(root_package, e, collection))

        print("GENERATING ... Service")
        write(get_file_loc("service_impl", e + "ServiceImpl"), service_impl_template(root_package, e, collection, lombok))

        print("GENERATING ... Controller")
        write(get_file_loc("controller", e + "Controller"), controller_template(root_package, e, collection, lombok))

        print("GENERATING ... DTO")
        write(get_file_loc("dto", e + "DTO"), generate_dto(root_package, e, each[1], lombok))

        print("GENERATING ... Mapper")
        write(get_file_loc("mapper", e + "Mapper"), generate_mapper(root_package, e, each[1], collection))
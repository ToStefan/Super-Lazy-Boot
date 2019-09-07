import os
import json


def clear():
	if(os.system == "nt"):
		os.system("clear")
	else:
		os.system("cls")

def cap_first(s):
    return s[:1].upper() + s[1:]

def load_json(file_name):
    file = open(file_name, encoding="utf-8")
    json_model = json.load(file)
    return json_model

def write(file_location, content):
    file = open(file_location, "w+")
    file.write(content)
    file.close()

def switch_package(identifier, root_package):
    src_main = "src/main/java/" + root_package
    src_test = "src/test/java/" + root_package
    web = src_main + "/web"
    entity = src_main + "/entity/"
    service = src_main + "/service/"
    service_impl = service + "impl/"
    repository = src_main + "/repository/"
    dto = web + "/dto/"
    controller = web + "/controller/"
    mapper = web + "/mapper/"
    switcher = {
        "src_main": src_main,
        "src_test": src_test,
        "web": web,
        "entity": entity,
        "service": service,
        "service_impl": service_impl,
        "repository": repository,
        "dto": dto,
        "controller": controller,
        "mapper": mapper
    }
    return switcher.get(identifier, "")
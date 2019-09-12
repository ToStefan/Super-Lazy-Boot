import os
import json

PACKAGES = {}

def get_file_loc(key, file_name):
    return PACKAGES[key] + file_name + ".java"

def set_packages(root_package):
    root = "src/main/java/" + root_package
    PACKAGES["entity"] =  root + "/entity/"
    PACKAGES["service"] = root + "/service/"
    PACKAGES["service_impl"] = root + "/service/impl/"
    PACKAGES["repository"] = root + "/repository/"
    PACKAGES["controller"] = root + "/web/controller/"
    PACKAGES["mapper"] = root + "/web/mapper/"
    PACKAGES["dto"] = root + "/web/dto/"

def generate_project():
    if not os.path.exists(PACKAGES["entity"]): os.makedirs(PACKAGES["entity"])
    if not os.path.exists(PACKAGES["service"]): os.makedirs(PACKAGES["service"])
    if not os.path.exists(PACKAGES["service_impl"]): os.makedirs(PACKAGES["service_impl"])
    if not os.path.exists(PACKAGES["repository"]): os.makedirs(PACKAGES["repository"])
    if not os.path.exists(PACKAGES["controller"]): os.makedirs(PACKAGES["controller"])
    if not os.path.exists(PACKAGES["mapper"]): os.makedirs(PACKAGES["mapper"])
    if not os.path.exists(PACKAGES["dto"]): os.makedirs(PACKAGES["dto"])

def clear():
	if(os.system == "nt"):
		os.system("clear")
	else:
		os.system("cls")

def cap_first(s):
    return s[:1].upper() + s[1:]

def remove_char_at_end(string, char):
    if(string.endswith(char)):
        return string[:-1]
    return string

def load_json(file_name):
    file = open(file_name, encoding="utf-8")
    json_model = json.load(file)
    return json_model

def write(file_location, content):
    file = open(file_location, "w+")
    file.write(content)
    file.close()

def switch_relation(identifier):
    switcher = {
        "1:1": "OneToOne",
        "1:n": "OneToMany",
        "n:1": "ManyToOne",
        "n:n": "ManyToMany",
    }
    return switcher.get(identifier, "")

def generate_sql_field_name(name):
    char_list = []
    ret_val = name
    for char in name:
        if(char.isupper()): char_list.append("_" + char)
        else: char_list.append(char)
    return "".join(char_list).lower()
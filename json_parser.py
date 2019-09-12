from utils import load_json, switch_relation, generate_sql_field_name, remove_char_at_end

def parser(json_file):
    classes = {}
    enums = []
    settings = {}
    json_model = load_json(json_file)
    for each in json_model:
        if(each["type"] == "Class"):
            classes = parse_classes(each["classes"])
        if(each["type"] == "Enum"):
            enums = parse_enums(each["enums"])
        if(each["type"] == "Settings"):
            settings = parse_setings(each["settings"])
    return settings, enums, classes

def parse_classes(classes_json_list):
    classes = {}
    for each in classes_json_list:
        class_name = each["name"]
        primary_key = ""
        attr_tupple_list = []
        for a in (each["atributes"]):

            try: nullable = a["nullable"]
            except KeyError: nullable = "false"
            
            try: relation = switch_relation(a["relation"].lower())
            except KeyError: relation = False
            
            try: fetch = a["fetch_type"].upper()
            except KeyError: fetch = "LAZY"
            
            try: cascade = a["cascade_type"].upper()
            except KeyError: cascade = "ALL"

            if(relation == "ManyToMany") : sql_field_name = class_name.lower() + "_" + remove_char_at_end(a["field"], "s")
            else: sql_field_name = generate_sql_field_name(a["field"])

            attr_tupple = (a["field"], sql_field_name, \
                a["field_type"], a["type"],  nullable, relation, fetch, cascade)
            attr_tupple_list.append(attr_tupple)
        classes[class_name] = attr_tupple_list
    return classes

def parse_enums(enums_json_list):
    enums = []
    for each in enums_json_list:
        enum_tupple = (each["name"], each["values"])
        enums.append(enum_tupple)
    return enums

def parse_setings(settings_json_list):
    return settings_json_list
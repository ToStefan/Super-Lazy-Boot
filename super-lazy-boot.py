import sys

from writers import writer
from generators import set_settings
from utils import clear, cap_first

class_map = {}
enum_map = {}
settings_map = {}

def main():
    parser()
    print("")
    syntax_check()
    print("")
    confirm = raw_input("y/n >> ")
    if(confirm == "y" or confirm == "Y"):
        set_settings(settings_map)
        writer(class_map, enum_map)
    else:
        pass

def syntax_check():
    print(">> Syntax check...")

    def class_check():
        for key, values in class_map.items():
            print("    " + key + " (class)")
            for value in values:
                print("      -> " + value.split(":")[0] + " " + value.split(":")[1])
            print("")

    def enum_check():
        for key, values in enum_map.items():
            print("    " + key + " (enum)")
            for value in values:
                print("      -> " + value)
            print("")

    def settings_check():
        for key, value in settings_map.items():
            print("    " + key + " -> " + value[0])
            if(key != "security" and key != "rootPackage"):
                try:
                    eval(cap_first(value[0]))
                except NameError as e:
                    raise SyntaxError(key + " value must be true or false")
            elif(key == "security"):
                if(value[0] != "jwt" and value[0] != "basic"):
                    raise SyntaxError(key + " authentication must be 'jwt' or 'basic'")
        print("")

    try:
        settings_check()
        class_check()
        enum_check()
    except SyntaxError as e:
        print("        ERROR: " + str(e))
        raise SystemExit(0)


def parser():
    with open(sys.argv[1], 'r') as file:
        data = file.read().replace(" ", "").replace("\n", "").replace("\t", "").rstrip()

    def class_parser(data):
        try:
            classes = data.split("Class{")[1].split("}")[0].split(",")
            for each_class in classes:
                if(each_class == ""):
                    print("    INFO: Comma at end of class declaration detected")
                else:
                    each_class = each_class.split("->")
                    class_map[each_class[0]] = each_class[1:]
        except IndexError:
            print("    INFO: No classes specified")
            raise SystemExit(0)
        

    def enum_parser(data):
        try:
            enums = data.split("Enum{")[1].split("}")[0].split(",")
            for each_enum in enums:
                if(each_enum == ""):
                    print("    INFO: Comma at end of enum declaration detected")
                else:
                    each_enum = each_enum.split("->")
                    enum_map[each_enum[0]] = each_enum[1:]
        except IndexError:
            print("    INFO: No enums specified")
        

    def settings_parser(data):
        root_package_exist = False
        try:
            settings = data.split("Settings{")[1].split("}")[0].split(",")
            if(settings[0] == ""):
                print("    INFO: No settings specified")
            else:
                for each_setting in settings:
                    if(each_setting == ""):
                        print("    INFO: Comma at end of settings declaration detected")
                    else:
                        each_setting = each_setting.split(":")
                        settings_map[each_setting[0]] = each_setting[1:]
                        if(each_setting[0] == "rootPackage"):
                            root_package_exist = True
                if(root_package_exist == False):
                    print("    ERROR: No 'rootPackage' in Settings found!")
                    raise SystemExit(0)
        except IndexError:
            print("    ERROR: No settings specified")
            raise SystemExit(0)

    print(">> Parsing classes...")
    class_parser(data)
    print(">> Parsing enums...")
    enum_parser(data)
    print(">> Parsing settings...")
    settings_parser(data)
    

if __name__ == "__main__":
    clear()
    main()
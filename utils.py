import os

def getPrimaryKeyType(attributes):
    for att in attributes:
        attribute = att.split(":")
        try:
            if(attribute[2] == "primary"):
                return attribute[0]
        except:
            pass

def clear():
	if(os.system == "nt"):
		os.system("clear")
	else:
		os.system("cls")
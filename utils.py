def getPrimaryKeyType(attributes):
    for att in attributes:
        attribute = att.split(":")
        try:
            if(attribute[2] == "primary"):
                return attribute[0]
        except:
            pass
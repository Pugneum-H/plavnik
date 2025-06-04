def from_plavnik(pile : str) -> dict:
    def __typechanger(value : str):
        if value == "null": return None
        elif value == "true": return True
        elif value == "false": return False
        else:
            if value.startswith("[") and value.endswith("]"):
                return [__typechanger(i) for i in list(__token_split(value.removeprefix("[").removesuffix("]")))]
            elif (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')): 
                return str(value.removeprefix('"').removesuffix('"').removeprefix("'").removesuffix("'"))
            elif all(i in "-.0123456789" for i in list(value)):
                if value.count(".") == 1 and value.find(".") != len(value)-1:
                    if (value.count("-") == 1 and value.find("-") == 0) or value.count("-") == 0: return float(value) 
                    else: raise TypeError(f"Incorrect float - {value}")
                elif value.count(".") == 0:
                    if (value.count("-") == 1 and value.find("-") == 0) or value.count("-") == 0: return int(value) 
                    else: raise TypeError(f"Incorrect int - {value}")
            else:  raise TypeError(f"Incorrect type - {value}")

    def __token_split(string : str) -> list:
        result = []
        current = ""
        inside = None
        for token in string.split():
            if inside != None:
                current += token + " "
                if token.endswith(inside):
                    result.append(current.strip())
                    current = ""
                    inside = None
            elif token.startswith(("'", '"', "[")):
                current = token + " "
                inside = token[0] if token[0] in ("'", '"') else "]"
                if token.endswith(inside) and len(token) > 1:
                    result.append(current.strip())
                    current = ""
                    inside = None
            else:
                result.append(token)

        if current:
            result.append(current.strip())

        return result


    def __set_innerdict(keys: list, value):
        res = dictionary
        for key in keys[:-1]:
            if key not in res or not isinstance(res[key], dict):
                res[key] = {}
            res = res[key]
        if keys[-1] not in res or not isinstance(res[keys[-1]], dict):
            res[keys[-1]] = {}
        res[keys[-1]].update(value)

        
    lines = pile.splitlines()
    line = 0
    container = ""
    dictionary = {}
    while line < len(lines):
        if lines[line].strip().startswith("#"): line += 1
        elif lines[line].strip() == "": line += 1; container = "default"
        else:
            if not lines[line].startswith("  "): 
                if len(lines[line].strip().split(" ")) == 1: container = lines[line].strip().split(" ")[0]; line += 1
                else: 
                    container = "default"
                    __set_innerdict(container.split("."), {lines[line].strip().split(" ", 1)[0].strip() : __typechanger(lines[line].strip().split(" ", 1)[1].strip())})
                    line += 1
            else:
                if len(lines[line].strip().split(" ", 1)) == 2: 
                    __set_innerdict(container.split("."), {lines[line].strip().split(" ", 1)[0].strip() : __typechanger(lines[line].strip().split(" ", 1)[1].strip())})
                    line += 1
                else: raise TypeError(f"Impossible to construct - {lines[line]}") 

    return dictionary

def to_plavnik(data_dict : dict) -> str:
    def __walk(data : dict, path : str):
        result = []
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    result.extend(__walk(value, new_path))
                else:
                    result.append((new_path, value))
                    
        return result
    

    def __values(value):
        def __val(val):
            if val is True: return "true"
            elif val is False: return "false"
            elif val is None: return "null"
            elif isinstance(val, str): return f"'{val}'"
            elif isinstance(val, list): return "[" + " ".join(__val(v) for v in val) + "]"
            else:
                if not type(val) in [list, str, int, float, bool, None]: raise TypeError(f"Incompatible type of value - {val}")
                else: return str(val)

        return __val(value)

    

    path = ""
    cranky = ""
    values = __walk(data_dict, path)
    process = []
    for path_data in values:    
        if not "".join(str(path_data[0]).split(".")[0:-1]) in cranky and str(path_data[0]).split(".")[0] != "default":
            cranky = cranky +  ".".join(str(path_data[0]).split(".")[0:-1]).removeprefix("default") + "\n"
        if str(path_data[0]).split(".")[0] != "default":
            cranky = cranky + "    " + str(path_data[0]).split(".")[-1] + " " + __values(path_data[1]) + "\n"
        else:
             cranky = cranky + str(path_data[0]).split(".")[-1] + " "  + __values(path_data[1]) + "\n"
            

    return cranky

from pprint import pprint

RESERVED = {"bool":1, "break":1, "case":1, "char":1, "class":1, "const":1,"continue":1, "default":1, "do":1, "double":1, "else":1, 
            "enum":1, "float":1, "for":1, "if":1, "int":1, "long":1, "main":1, "namespace":1, "new":1, "or":1, "private":1, "protected":1, 
            "public":1, "return":1, "short":1, "signed":1, "sizeof":1, "static":1, "struct":1, "switch":1, "this":1, "unsigned":1,
            "using":1, "void":1, "while":1, "#include":1}
LOGIC = {"==":1, "!=":1, ">":1, "<":1, ">=":1, "<=":1, "&&":1, "||":1, "!":1}
OPERATOR = {"=":1, "+":1, "-":1, "/":1, "*":1, "%":1, "+=":1, "-=":1, "/=":1, "*=":1, "++":1, "--":1}
BLOCK = {"(":1, ")":1, "{":1, "}":1, "[":1, "]":1}
LITERAL = {"\"":1, "\'":1}
SEPARATORS = {";":1, ",":1, ":":1}

variable_table = {'identifier':[], 'reserved':[], 'logic':[], 'operator':[], 'block':[], 'literal':[], 'separator':[], 'number':[]}

def get_word(symbol, line, position):
    """Searches for the end of a literal.

    Args:
        symbol (str): The literal symbol that started the str.
        line (str): The line in which the symbol was found.
        position (int): The starting position of the literal symbol.

    Returns:
        str: The word found.
        int: The position after the word found.
    """

    word = ""
    count = 0
    for pos, char in enumerate(line[position:]):
        word += char
        if char == symbol: count += 1
        if count == 2: return word, position + pos + 1
    return word, len(line)

def get_number(line, position):
    """Searches for the end of a number.

    Args:
        line (str): The line in which the number was found.
        position (int): The starting position of the number.

    Returns:
        str: The number found.
        int: The position after the number found.
    """

    word = ""
    for pos, char in enumerate(line[position:]):
        if char.isdigit() or char == ".": word += char
        else: return word, position + pos
    return word, len(line)

def is_from(category, symbol):
    """Checks if the symbol is from the category given.

    Args:
        category (dict): The dictionary of the category to check.
        symbol (str): The symbol or word given to analyze.

    Returns:
        bool: Whether the symbol is part of the category given.
    """
    
    try:
        category[symbol]
        return True
    except:
        return False

def categorize(symbol):
    """Checks the category of a word or symbol.

    Args:
        symbol (str): The symbol to be categorized.

    Returns:
        str: The key to a dictionary with all the categories.
    """

    try:
        float(symbol)
        category = "number"
    except:
        category = "identifier"

    if is_from(RESERVED, symbol): category = "reserved"
    elif is_from(LOGIC, symbol): category = "logic"
    elif is_from(OPERATOR, symbol): category = "operator"
    elif is_from(BLOCK, symbol): category = "block"
    elif is_from(LITERAL, symbol[0]): category = "literal"
    elif is_from(SEPARATORS, symbol): category = "separator"
        
    return category

def read_next(line, position):
    """Reads the next word from the line.

    Args:
        line (str): A line of the code given.
        position (int): The starting position of the next word.

    Returns:
        str: The word, its separated depending on the possible categories.
        int: The starting position of the next word to read.
    """

    word = ""
    total_pos = position
    for pos, char in enumerate(line[position:]):
        global_pos = position + pos
        total_pos = global_pos
        if char == " ":
            for temp_pos, temp_char in enumerate(line[global_pos:]):
                if not temp_char == " ":
                    total_pos += temp_pos
                    break
            break
        elif char == "\n" or (char == "/" and line[global_pos+1] == "/"):
            total_pos = len(line)
            break
        else:
            if is_from(SEPARATORS, char) or is_from(BLOCK, char):
                if word == "":
                    word = char
                    total_pos += 1
                break
            elif is_from(LITERAL, char):
                if word == "": word, total_pos = get_word(char, line, global_pos)
                break
            elif is_from(OPERATOR, char):
                if word == "":
                    word = char
                    total_pos += 1
                    temp_word = char + line[global_pos+1]
                    if is_from(OPERATOR, temp_word) or is_from(LOGIC, temp_word): 
                        word = temp_word
                        total_pos += 2
                break
            elif is_from(LOGIC, char):
                if word == "":
                    word = char
                    total_pos += 1
                    temp_word = char + line[global_pos+1]
                    if is_from(LOGIC, temp_word): 
                        word = temp_word
                        total_pos += 2
                break
            elif char.isdigit():
                if word == "": 
                    word, total_pos = get_number(line, global_pos)
                    break
                elif not categorize(word) == "identifier": break
        word += char
    return word, total_pos

code = open("Input.txt", "r").read().split("\n")
code = [line + "\n" for line in code]
for line in code:
    pos = 0
    while not pos == len(line):
        word, pos = read_next(line, pos)
        if not word == "": variable_table[categorize(word)].append(word)

for key in variable_table.keys():
    print(key.capitalize())
    pprint(variable_table[key])
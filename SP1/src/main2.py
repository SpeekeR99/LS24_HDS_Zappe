import json

V = ["a", "A", "e", "E", "i", "I", "y", "Y", "o", "O", "u", "U", "y", "Y", "F"]
K = ["b", "c", "C", "d", "D", "f", "g", "h", "x", "j", "k", "l", "m", "n", "J", "p", "r", "R", "s", "S", "t", "T", "v",
      "z", "Z", "w", "W", "N", "M", "G", "Q", "P", "L", "H"]
Krl = ["b", "c", "C", "d", "D", "f", "g", "h", "x", "j", "k", "m", "n", "p", "R", "s", "S", "t", "T", "v",
      "z", "Z", "w", "W", "N", "M", "G", "Q", "H"]  # TODO: ň (J) ???
ZPK = ["b", "d", "D", "g", "v", "z", "Z", "h", "w", "W", "R"]
NPK = ["p", "t", "T", "k", "f", "s", "S", "x", "c", "C", "Q"]
JK = ["m", "n", "J", "l", "r", "j"]
NP = ["k", "s", "v", "z"]
JPZ = ["bez", "nad", "ob", "od", "pod", "pRed", "pQed", "pRez", "pQez"]

with open("../data/rules.json", "r", encoding="utf-8") as file:
    rules = json.load(file)

print(rules)

data = []
with open("../data/ukazka_HDS.ortho.txt", "r", encoding="utf-8") as file:
    for line in file:
        data.append(line.lower().strip())
answers = []
with open("../data/ukazka_HDS.phntrn.txt", "r", encoding="utf-8") as file:
    for line in file:
        answers.append(line.strip())

correct = 0


def apply_symbolic_rule(sentence, lvalue, rvalue):
    symbols = []
    symbols_values = []
    # symbols are between "<" and ">"
    for i in range(len(lvalue)):
        if lvalue[i] == "<":
            start = i
        if lvalue[i] == ">":
            end = i
            symbols.append(lvalue[start + 1:end])
    for i in range(len(rvalue)):
        if rvalue[i] == "<":
            start = i
        if rvalue[i] == ">":
            end = i
            symbols_values.append(rvalue[start + 1:end])
    # substitute symbols with possible values
    if len(symbols) == 0 or symbols[0] == "COM":
        return sentence
    substitutions = []
    substitutions_values = []
    for symbol in symbols:
        if symbol == "V":
            temp = []
            for v in V:
                temp.append(v)
            substitutions.append(temp)
        if symbol == "K":
            temp = []
            for k in K:
                temp.append(k)
            substitutions.append(temp)
        if symbol == "ZPK":
            temp = []
            for zpk in ZPK:
                temp.append(zpk)
            substitutions.append(temp)
        if symbol == "NPK":
            temp = []
            for npk in NPK:
                temp.append(npk)
            substitutions.append(temp)
        if symbol == "JK":
            temp = []
            for jk in JK:
                temp.append(jk)
            substitutions.append(temp)
        if symbol == "NP":
            temp = []
            for np in NP:
                temp.append(np)
            substitutions.append(temp)
        if symbol == "JPZ":
            temp = []
            for jpz in JPZ:
                temp.append(jpz)
            substitutions.append(temp)
        if symbol == "Krl":
            temp = []
            for krl in Krl:
                temp.append(krl)
            substitutions.append(temp)

    for symbol_value in symbols_values:
        if symbol_value == "V":
            temp = []
            for v in V:
                temp.append(v)
            substitutions_values.append(temp)
        if symbol_value == "K":
            temp = []
            for k in K:
                temp.append(k)
            substitutions_values.append(temp)
        if symbol_value == "ZPK" or symbol_value == "¬NPK":
            temp = []
            for zpk in ZPK:
                temp.append(zpk)
            substitutions_values.append(temp)
        if symbol_value == "NPK" or symbol_value == "¬ZPK":
            temp = []
            for npk in NPK:
                temp.append(npk)
            substitutions_values.append(temp)
        if symbol_value == "JK":
            temp = []
            for jk in JK:
                temp.append(jk)
            substitutions_values.append(temp)
        if symbol_value == "NP":
            temp = []
            for np in NP:
                temp.append(np)
            substitutions_values.append(temp)
        if symbol_value == "JPZ":
            temp = []
            for jpz in JPZ:
                temp.append(jpz)
            substitutions_values.append(temp)
        if symbol_value == "Krl":
            temp = []
            for krl in Krl:
                temp.append(krl)
            substitutions_values.append(temp)
    # generate all possible combinations of symbols
    import itertools
    combinations = list(itertools.product(*substitutions))
    combinations_values = list(itertools.product(*substitutions_values))
    substituted_rules = []
    for combination in combinations:
        temp = lvalue
        for i in range(len(combination)):
            # replace first occurrence of symbol with value
            temp = temp.replace("<" + symbols[i] + ">", combination[i], 1)
        substituted_rules.append(temp)
    substituted_values = []
    for combination in combinations_values:
        temp = rvalue
        for i in range(len(combination)):
            temp = temp.replace("<" + symbols_values[i] + ">", combination[i], 1)
        substituted_values.append(temp)

    for i in range(len(substituted_rules)):
        sentence = sentence.replace(substituted_rules[i], substituted_values[i])

    return sentence

for sentence in data:
    orig = sentence

    sentence = "|$|" + sentence.lower().replace(" ", "|").replace(",", "|#").replace(".", "") + "|$|"

    for rule in rules["2.8.3"]:
        if rule == "y" or rule == "ý":
            continue
        sentence = sentence.replace(rule, rules["2.8.3"][rule])

    for rule in rules["2.8.5"]:
        if rule == "symbolic":
            for sym_rule in rules["2.8.5"][rule]:
                sym_value = rules["2.8.5"][rule][sym_rule]
                sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
        else:
            sentence = sentence.replace(rule, rules["2.8.5"][rule])

    for rule in rules["2.8.6"]:
        if rule == "symbolic":
            for sym_rule in rules["2.8.6"][rule]:
                sym_value = rules["2.8.6"][rule][sym_rule]
                sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
        else:
            sentence = sentence.replace(rule, rules["2.8.6"][rule])

    for rule in rules["2.8.7.1"]:
        for i in range(5):
            if rule == "symbolic":
                for sym_rule in rules["2.8.7.1"][rule]:
                    sym_value = rules["2.8.7.1"][rule][sym_rule]
                    sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
            else:
                sentence = sentence.replace(rule, rules["2.8.7.1"][rule])

    for rule in rules["2.8.7.2"]:
        if rule == "symbolic":
            for sym_rule in rules["2.8.7.2"][rule]:
                sym_value = rules["2.8.7.2"][rule][sym_rule]
                sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
        else:
            sentence = sentence.replace(rule, rules["2.8.7.2"][rule])

    for rule in rules["2.8.7.3"]:
        if rule == "symbolic":
            for sym_rule in rules["2.8.7.3"][rule]:
                sym_value = rules["2.8.7.3"][rule][sym_rule]
                sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
        else:
            sentence = sentence.replace(rule, rules["2.8.7.3"][rule])

    for rule in rules["2.8.7.4"]:
        if rule == "symbolic":
            for sym_rule in rules["2.8.7.4"][rule]:
                sym_value = rules["2.8.7.4"][rule][sym_rule]
                sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
        else:
            sentence = sentence.replace(rule, rules["2.8.7.4"][rule])

    for rule in rules["2.8.3"]:
        sentence = sentence.replace(rule, rules["2.8.3"][rule])

    for rule in rules["2.8.4"]:
        if rule == "symbolic":
            for sym_rule in rules["2.8.4"][rule]:
                sym_value = rules["2.8.4"][rule][sym_rule]
                sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)
        else:
            sentence = sentence.replace(rule, rules["2.8.4"][rule])

    if sentence.strip() == answers[data.index(orig)].strip():
        correct += 1
    else:
        print(orig)
        print(sentence)
        print(answers[data.index(orig)])

print(correct / len(data))


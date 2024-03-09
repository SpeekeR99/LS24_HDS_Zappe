import json
import itertools

with open("../data/epa.json", "r", encoding="utf-8") as fp:
    epa = json.load(fp)

with open("../data/rules.json", "r", encoding="utf-8") as fp:
    rules = json.load(fp)

print(rules)

data = []
with open("../data/vety_HDS.ortho.txt", "r", encoding="utf-8") as file:
    for line in file:
        data.append(line.lower().strip())
answers = []
with open("../data/kniha.phntrn.txt", "r", encoding="utf-8") as file:
    for line in file:
        answers.append(line.strip())

correct = 0
data = ["dcera dceřinný dceřino srdce srdečný srdíčko srdcový"]


def apply_symbolic_rule(sentence, lvalue, rvalue):
    l_symbols = []
    r_symbols = []
    # symbols are between "<" and ">"
    for i in range(len(lvalue)):
        if lvalue[i] == "<":
            start = i
        if lvalue[i] == ">":
            end = i
            l_symbols.append(lvalue[start + 1:end])
    for i in range(len(rvalue)):
        if rvalue[i] == "<":
            start = i
        if rvalue[i] == ">":
            end = i
            r_symbols.append(rvalue[start + 1:end])

    if len(l_symbols) == 0 or l_symbols[0] == "COM":
        return sentence

    # substitute symbols with possible values
    l_subs = []
    r_subs = []
    for symbol in l_symbols:
        l_subs.append(epa[symbol])
    for symbol in r_symbols:
        r_subs.append(epa[symbol])

    # generate all possible combinations of symbols
    l_comb = list(itertools.product(*l_subs))
    r_comb = list(itertools.product(*r_subs))

    l_subs = []
    r_subs = []
    for combination in l_comb:
        temp = lvalue
        for i in range(len(combination)):
            # replace first occurrence of symbol with value
            temp = temp.replace("<" + l_symbols[i] + ">", combination[i], 1)
        l_subs.append(temp)
    for combination in r_comb:
        temp = rvalue
        for i in range(len(combination)):
            temp = temp.replace("<" + r_symbols[i] + ">", combination[i], 1)
        r_subs.append(temp)

    for i in range(len(l_subs)):
        sentence = sentence.replace(l_subs[i], r_subs[i])

    return sentence


def apply_rule(sentence, rules, rule_name, repeat_rule=1, ignore_y_rule=True):
    for rule in rules[rule_name]:
        for _ in range(repeat_rule):
            if (rule == "y" or rule == "ý") and ignore_y_rule:
                continue

            if rule == "symbolic":
                for sym_rule in rules[rule_name][rule]:
                    sym_value = rules[rule_name][rule][sym_rule]
                    sentence = apply_symbolic_rule(sentence, sym_rule, sym_value)

            else:
                sentence = sentence.replace(rule, rules[rule_name][rule])

    return sentence


for sentence in data:
    orig = sentence

    sentence = "|$|" + sentence.lower().replace(" ", "|").replace(",", "|#").replace(".", "") + "|$|"

    sentence = apply_rule(sentence, rules, "2.8.3")
    sentence = apply_rule(sentence, rules, "2.8.5")
    sentence = apply_rule(sentence, rules, "2.8.6")
    sentence = apply_rule(sentence, rules, "2.8.7.1", repeat_rule=5)
    sentence = apply_rule(sentence, rules, "2.8.7.2")
    sentence = apply_rule(sentence, rules, "2.8.7.3")
    sentence = apply_rule(sentence, rules, "2.8.7.4")
    sentence = apply_rule(sentence, rules, "2.8.3", ignore_y_rule=False)
    sentence = apply_rule(sentence, rules, "2.8.4")

    # with open("../data/vety_HDS.phntrn.txt", "a", encoding="utf-8") as fp:
    #     fp.write(sentence + "\n")

    # if sentence.strip() == answers[data.index(orig)].strip():
    #     correct += 1
    # else:
    #     print(orig)
    print(sentence)
    #     print(answers[data.index(orig)])

# print(correct / len(data))


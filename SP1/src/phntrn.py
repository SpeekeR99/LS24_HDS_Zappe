import itertools


def apply_rule(sentence, epa, rules, rule_name):
    """
    Applies a rule to a sentence
    :param sentence: Sentence to apply the rule to
    :param epa: EPA dictionary from epa.json
    :param rules: Rules dictionary from rules.json
    :param rule_name: Rule to apply
    :return: Changed sentence
    """
    while True:
        original = sentence

        for rule in rules[rule_name]:  # For each rule in the set of rules
            if rule == "symbolic":  # Special case of symbolic rules
                for sym_rule in rules[rule_name][rule]:  # For each symbolic rule in the set of symbolic rules
                    sym_value = rules[rule_name][rule][sym_rule]
                    sentence = _apply_symbolic_rule(sentence, sym_rule, sym_value, epa)

            else:  # Normal rules
                sentence = sentence.replace(rule, rules[rule_name][rule])

        if sentence == original:
            break

    return sentence


def _apply_symbolic_rule(sentence, lvalue, rvalue, epa):
    """
    Applies a symbolic rule to a sentence
    :param sentence: Sentence to apply the rule to
    :param lvalue: Left side of the rule
    :param rvalue: Right side of the rule
    :param epa: EPA dictionary from epa.json
    :return: Changed sentence
    """
    l_symbols = []
    r_symbols = []

    # Symbols are between "<" and ">", parse them
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

    # If there are no symbols or the first symbol is "COM" (for comments), do nothing
    if len(l_symbols) == 0 or l_symbols[0] == "COM":
        return sentence

    # Substitute symbols with possible values (from EPA)
    l_subs = []
    r_subs = []
    for symbol in l_symbols:
        l_subs.append(epa[symbol])
    for symbol in r_symbols:
        r_subs.append(epa[symbol])

    # Generate all possible combinations of symbols
    l_comb = list(itertools.product(*l_subs))
    r_comb = list(itertools.product(*r_subs))

    # Replace symbols with values from the combinations
    # This works because the symbols in the left and right side are in the same order
    # eg. "b" has the same index as "p", thus making a pair
    l_subs = []
    r_subs = []
    for combination in l_comb:
        temp = lvalue
        for i in range(len(combination)):
            temp = temp.replace("<" + l_symbols[i] + ">", combination[i], 1)
        l_subs.append(temp)
    for combination in r_comb:
        temp = rvalue
        for i in range(len(combination)):
            temp = temp.replace("<" + r_symbols[i] + ">", combination[i], 1)
        r_subs.append(temp)

    # Replace the left side with the right side in the sentence
    for i in range(len(l_subs)):
        sentence = sentence.replace(l_subs[i], r_subs[i])

    return sentence

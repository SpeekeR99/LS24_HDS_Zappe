import json

with open("../data/epa.json", "r", encoding="utf-8") as file:
    rules = json.load(file)

print(list(rules.keys()))

data = []
with open("../data/kniha.ortho.txt", "r", encoding="utf-8") as file:
    for line in file:
        data.append(line.lower().strip())
answers = []
with open("../data/kniha.phntrn.txt", "r", encoding="utf-8") as file:
    for line in file:
        answers.append(line.strip())

correct = 0

for sentence in data:
    print(sentence)

    result = sentence.lower()
    result = result.replace(" ", "|")
    result = result.replace(",", "|#")
    result = result.replace(".", "")
    result = "|$|" + result + "|$|"

    for rule in rules["zakladni_pravidla"]:
        if rule == "y" or rule == "ý":
            continue
        result = result.replace(rule, rules["zakladni_pravidla"][rule])

    for rule in rules["spojeni_souhlasky_a_samohlasky"]:
        if rule == "symbolic_rules":
            continue
        result = result.replace(rule, rules["spojeni_souhlasky_a_samohlasky"][rule])

    for rule in rules["asimilace_artikulacni"]:
        result = result.replace(rule, rules["asimilace_artikulacni"][rule])

    for rule in rules["zjendodusena_vyslovnost_souhlaskovych_skupin"]:
        result = result.replace(rule, rules["zjendodusena_vyslovnost_souhlaskovych_skupin"][rule])

    for rule in rules["zakladni_pravidla"]:
        if rule == "y" or rule == "ý":
            result = result.replace(rule, rules["zakladni_pravidla"][rule])

    for rule in rules["spojeni_samohlasek"]:
        result = result.replace(rule, rules["spojeni_samohlasek"][rule])

    vowels_phn = rules["symbols_phn"]["V"]
    if "$" in result:
        index = result.index("$")
        if result[index + 2] in vowels_phn:
            result = result[:index + 2] + "!" + result[index + 2:]
    if "#" in result:
        index = result.index("#")
        if result[index + 2] in vowels_phn:
            result = result[:index + 2] + "!" + result[index + 2:]

    # TODO: asimilace_znelosti, slabikotvorne_souhlasky

    print(result)
    print(answers[data.index(sentence)])

    if result.strip() == answers[data.index(sentence)].strip():
        correct += 1

print(correct / len(data))

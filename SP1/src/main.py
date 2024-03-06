import json

with open("../data/epa.json", "r", encoding="utf-8") as file:
    rules = json.load(file)

print(list(rules.keys()))

data = []
with open("../data/kniha.ortho.txt", "r", encoding="utf-8") as file:
    for line in file:
        data.append(line.lower().strip())

sentence = data[0]

result = "|$|"
for word in sentence.split(" "):
    word = word.replace(",", "|#")

    # do all the magic here

    result += word + "|"
result += "$|"

print(sentence)
print(result)

for rule in rules["zakladni_pravidla"]:
    if rule == "y" or rule == "ý":
        continue
    result = result.replace(rule, rules["zakladni_pravidla"][rule])

for rule in rules["spojeni_samohlasek"]:
    result = result.replace(rule, rules["spojeni_samohlasek"][rule])

for rule in rules["spojeni_souhlasky_a_samohlasky"]:
    if rule == "symbolic_rules":
        continue
    result = result.replace(rule, rules["spojeni_souhlasky_a_samohlasky"][rule])

for rule in rules["zakladni_pravidla"]:
    if rule == "y" or rule == "ý":
        result = result.replace(rule, rules["zakladni_pravidla"][rule])

print(result)

print("|$|vZdicki|si|pQAl|mId|hospodu|#|!ale|nemJel|rAt|liDi|$|")

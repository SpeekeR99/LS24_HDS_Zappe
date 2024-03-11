import json
from phntrn import apply_rule


def load_files(epa_path="../data/epa.json", rules_path="../data/rules.json", data_path="../data/vety_HDS.ortho.txt"):
    with open(epa_path, "r", encoding="utf-8") as fp:
        epa = json.load(fp)

    with open(rules_path, "r", encoding="utf-8") as fp:
        rules = json.load(fp)

    data = []
    with open(data_path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(line.lower().strip())

    return epa, rules, data


def main(output_path="../data/vety_HDS.phntrn.txt"):
    epa, rules, data = load_files()


    phntrn = []
    for sentence in data:
        sentence = "|$|" + sentence.lower() + "|$|"

        sentence = apply_rule(sentence, epa, rules, "basic")
        sentence = apply_rule(sentence, epa, rules, "2.8.3")
        sentence = apply_rule(sentence, epa, rules, "2.8.5")
        sentence = apply_rule(sentence, epa, rules, "2.8.6")
        sentence = apply_rule(sentence, epa, rules, "2.8.7.1", repeat_rule=5)
        sentence = apply_rule(sentence, epa, rules, "2.8.7.2")
        sentence = apply_rule(sentence, epa, rules, "2.8.7.3")
        sentence = apply_rule(sentence, epa, rules, "2.8.7.4")
        sentence = apply_rule(sentence, epa, rules, "2.8.3", ignore_y_rule=False)
        sentence = apply_rule(sentence, epa, rules, "2.8.4")

        phntrn.append(sentence)

    with open(output_path, "w", encoding="utf-8") as fp:
        for sentence in phntrn:
            fp.write(sentence + "\n")


if __name__ == "__main__":
    main()

import sys
import json
from phntrn import apply_rule


EPA_FP = "../data/epa.json"
RULES_FP = "../data/rules.json"
INPUT_FP = "../data/vety_HDS.ortho.txt"
OUTPUT_FP = "../data/vety_HDS.phntrn.txt"


def load_files(epa_path=EPA_FP, rules_path=RULES_FP, data_path=INPUT_FP):
    """
    Load all the necessary files (epa.json, rules.json and a file with orthographic sentences to transform)
    :param epa_path: File path to epa.json
    :param rules_path: File path to rules.json
    :param data_path: File path to orthographic sentences (to be transformed)
    :return: EPA dictionary, Rules dictionary, List of orthographic sentences
    """
    # Load epa.json
    with open(epa_path, "r", encoding="utf-8") as fp:
        epa = json.load(fp)

    # Load rules.json
    with open(rules_path, "r", encoding="utf-8") as fp:
        rules = json.load(fp)

    # Load orthographic sentences
    data = []
    with open(data_path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(line.lower().strip())

    return epa, rules, data


def main(input_path=INPUT_FP, output_path=OUTPUT_FP):
    """
    Main function to do all the transformation and hard work
    :param input_path: Input file path for the orthographic sentences
    :param output_path: Output file path for the phonetically transcribed sentences
    """
    # Load all the necessary files
    epa, rules, data = load_files(data_path=input_path)
    print("Phonetic transcription in progress...")

    # Apply all the rules to the orthographic sentences
    phntrn = []
    for sentence in data:  # For each orthographic sentence
        # Add start and end symbols and make sure the sentence is lower case
        sentence = "|$|" + sentence.lower() + "|$|"

        # Apply all the rules
        sentence, _ = apply_rule(sentence, epa, rules, "preprocess")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.3.1")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.9.2")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.3.2")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.5")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.6")
        sentence, changed = apply_rule(sentence, epa, rules, "2.8.7.1")
        while changed:  # Keep applying the assimilation rule until it does not change the sentence anymore
            sentence, changed = apply_rule(sentence, epa, rules, "2.8.7.1")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.7.2")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.7.3")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.3.3")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.7.4")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.4")
        sentence, _ = apply_rule(sentence, epa, rules, "2.8.9.1")

        phntrn.append(sentence)

    # Save the phonetically transcribed sentences into an output file
    with open(output_path, "w", encoding="utf-8") as fp:
        for sentence in phntrn:
            fp.write(sentence + "\n")

    print("Phonetically transcribed sentences saved to " + output_path)


if __name__ == "__main__":
    if len(sys.argv) == 1:  # No arguments
        print("Using default file paths...")
        print("\t - EPA: " + EPA_FP)
        print("\t - Rules: " + RULES_FP)
        print("\t - Input: " + INPUT_FP)
        print("\t - Output: " + OUTPUT_FP)
        main()
    elif len(sys.argv) == 3:  # Two arguments
        print("Using specified file paths...")
        print("\t - EPA: " + EPA_FP)
        print("\t - Rules: " + RULES_FP)
        print("\t - Input: " + sys.argv[1])
        print("\t - Output: " + sys.argv[2])
        main(input_path=sys.argv[1], output_path=sys.argv[2])
    else:  # Anything else
        print("Invalid number of arguments!")
        print("Usage: python " + sys.argv[0])
        print("Usage: python " + sys.argv[0] + " <input_file> <output_file>")
        print("\t - <input_file>: File path to orthographic sentences")
        print("\t - <output_file>: File path to save phonetically transcribed sentences to")
        print("\t - If no arguments are given, default file paths are used")
        print("\t   (" + INPUT_FP + " and " + OUTPUT_FP + ")")
        print("Exiting...")
        sys.exit(377813111)

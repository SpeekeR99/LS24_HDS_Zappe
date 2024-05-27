# Load the base phrases, where the first 9 phrases are just classes in "<" ">"
with open("base_phrases.txt", "r", encoding="utf-8") as file:
    phrases = file.read().splitlines()
    base_phrases = phrases[:10]
    extra_phrases = phrases[10:]

print(len(extra_phrases))
final_phrases = extra_phrases.copy()

for phrase in extra_phrases:
    # Place is optional
    new_phrase_1 = phrase.replace("v <kraj>", "")
    final_phrases.append(new_phrase_1)
    # Day is optional
    new_phrase_2 = phrase.replace("v <den>", "")
    final_phrases.append(new_phrase_2)
    # Day can also be a date
    new_phrase_3 = phrase.replace("v <den>", "<cislo> <cislo> <cislo> set <cislo>")
    final_phrases.append(new_phrase_3)
    new_phrase_4 = phrase.replace("v <den>", "<cislo> <cislo> <cislo> tisíc <cislo> set <cislo>")
    final_phrases.append(new_phrase_4)
    new_phrase_5 = phrase.replace("v <den>", "<cislo> <cislo>")
    final_phrases.append(new_phrase_5)
    new_phrase_6 = phrase.replace("v <den>", "<cislo> <mesic> <cislo> set <cislo>")
    final_phrases.append(new_phrase_6)
    new_phrase_7 = phrase.replace("v <den>", "<cislo> <mesic> <cislo> tisíc <cislo> set <cislo>")
    final_phrases.append(new_phrase_7)
    new_phrase_8 = phrase.replace("v <den>", "<cislo> <mesic>")
    final_phrases.append(new_phrase_8)
    # Day and Place can be swapped
    new_phrase_9 = phrase.replace("v <den>", "<temp>")
    new_phrase_9 = new_phrase_9.replace("v <kraj>", "v <den>")
    new_phrase_9 = new_phrase_9.replace("<temp>", "v <kraj>")
    final_phrases.append(new_phrase_9)
    # <nehoda> and Day can be swapped
    new_phrase_10 = phrase.replace("v <den>", "<temp>")
    new_phrase_10 = new_phrase_10.replace("<nehoda>", "v <den>")
    new_phrase_10 = new_phrase_10.replace("<temp>", "<nehoda>")
    final_phrases.append(new_phrase_10)
    # <nehoda> and Place can be swapped
    new_phrase_11 = phrase.replace("v <kraj>", "<temp>")
    new_phrase_11 = new_phrase_11.replace("<nehoda>", "v <kraj>")
    new_phrase_11 = new_phrase_11.replace("<temp>", "<nehoda>")
    final_phrases.append(new_phrase_11)
    # v can be ve
    new_phrase_12 = phrase.replace("v", "ve")
    final_phrases.append(new_phrase_12)
    # v can be na
    new_phrase_13 = phrase.replace("v", "na")
    final_phrases.append(new_phrase_13)

print(len(final_phrases))

new_phrases = []
for phrase in final_phrases:
    # Day can be decorated with "last" etc.
    new_phrase = phrase.replace("<den>", "<den_dekorator> <den>")
    new_phrases.append(new_phrase)
for phrase in new_phrases:
    final_phrases.append(phrase)
    
print(len(final_phrases))

new_phrases = []
for phrase in final_phrases:
    # Each phrase can start with a greeting
    new_phrase_1 = "<pozdrav> " + phrase
    new_phrases.append(new_phrase_1)
    # Each phrase can start with "and" if the user is asking further questions
    new_phrase_2 = "a " + phrase
    new_phrases.append(new_phrase_2)
    # Each phrase can start with "zacatek"
    new_phrase_3 = "<zacatek> " + phrase
    new_phrases.append(new_phrase_3)
    new_phrase_4 = "<pozdrav> <zacatek> " + phrase
    new_phrases.append(new_phrase_4)
    new_phrase_5 = "a <zacatek> " + phrase
    new_phrases.append(new_phrase_5)

for phrase in new_phrases:
    final_phrases.append(phrase)

print(len(final_phrases))
final_phrases = set(final_phrases)
print(len(final_phrases))

with open("extra_phrases.txt", "w", encoding="utf-8") as file:
    for phrase in base_phrases:
        file.write(phrase + "\n")
    for phrase in final_phrases:
        file.write(phrase + "\n")
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

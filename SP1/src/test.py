from main import main


def test_main(input_path, output_path, reference_output_path):
    print(" - - - Start of test - - - ")

    main(input_path, output_path)

    with open(output_path, "r", encoding="utf-8") as file:
        output = file.readlines()
    with open(reference_output_path, "r", encoding="utf-8") as file:
        reference_output = file.readlines()

    if len(output) != len(reference_output):
        print("Lengths of output and reference output are different")
    else:
        print("Lengths of output and reference output are the same")

    correct = 0
    for i in range(len(output)):
        if output[i] == reference_output[i]:
            correct += 1
        else:
            print(f"Output and reference output differ at line {i + 1}")
            print(output[i])
            print(reference_output[i])

    print(f"Correct: {correct}/{len(output)}")
    print(" - - - End of test - - - ")


test_main(
    input_path="../data/kniha.ortho.txt",
    output_path="../data/kniha.phntrn.out.txt",
    reference_output_path="../data/kniha.phntrn.txt"
)
test_main(
    input_path="../data/ukazka_HDS.ortho.txt",
    output_path="../data/ukazka_HDS.phntrn.out.txt",
    reference_output_path="../data/ukazka_HDS.phntrn.txt"
)

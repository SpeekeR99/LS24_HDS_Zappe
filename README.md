# Phonetic Transcription Tool, Neural Voice Synthesis and Dialogue System

## Overview

This repository contains three projects developed as part of academic coursework:

1. **Phonetic Transcription Tool**: A Python-based application for converting text into the Extended Phonetic Alphabet (EPA).
2. **Neural Voice Synthesis**: A project focused on creating a neural model of the author's voice using deep learning techniques.
3. **Dialogue System**: A conversational agent that interacts with users to provide information and answer questions.

Each project is detailed below, including implementation details, challenges faced, and instructions for usage.

---

## Project 1: Phonetic Transcription Tool

### Description
The phonetic transcription tool processes input text and converts it into the Extended Phonetic Alphabet (EPA) using a series of predefined rules. The tool implements various phonetic rules, including preprocessing, assimilation, and handling of special cases like diphthongs and soft consonants.

### Key Features
- **Rule-Based Parsing**: Implements phonetic rules defined in `rules.json` and `epa.json`.
- **Symbolic Rules**: Supports symbolic replacements (e.g., `<V>` for vowels).
- **Iterative Application**: Rules are applied iteratively, where the output of one rule serves as the input for the next.
- **Customizable**: Allows users to modify rules for specific use cases.

### Challenges
- Handling rule precedence and exceptions.
- Addressing inconsistencies in the provided rulebook.
- Limited test data for validation.

### Usage
1. Ensure Python 3.x is installed (tested with Python 3.9).
2. Run the main script:

```bash
python main.py [input_file] [output_file]
```

Example:

```bash
python main.py ../data/input.txt ../data/output.txt
```

3. The program outputs the phonetic transcription to the specified output file.

---

## Project 2: Neural Voice Synthesis

### Description
This project involves training a neural network to synthesize speech that mimics the author's voice. The process includes recording audio samples, implementing loss functions, and training a VITS-based model.

### Key Features
- **Extensive Dataset**: Utilizes 1,024 recorded sentences for training.
- **Custom Loss Functions**: Implements generator loss, feature loss, and MEL loss.
- **Voice Similarity**: Outputs speech resembling the author's voice.

### Challenges
- Debugging issues with loss functions (e.g., improper use of `detach`).
- Misalignment between documentation and provided code.
- Lack of clarity in some model components (e.g., discriminator outputs).

### Usage
1. Prepare the dataset by recording audio samples.
2. Train the model using the provided scripts.
3. Evaluate the synthesized audio for quality and similarity to the original voice.

---

## Project 3: Dialogue System

### Description
The dialogue system is a conversational agent that interacts with users to provide information on various topics. The system uses a rule-based approach to understand user queries and generate appropriate responses.

### Key Features
- **Intent Recognition**: Identifies user intent based on predefined rules.
- **Response Generation**: Generates responses using templates and content retrieval.
- **Context Management**: Maintains conversation context for coherent interactions.

### Usage
1. Run the dialogue system using the provided script:

```bash
python dialog_manager.py
```

from random import random

# A function to remove vowels from and randomly add spaces to a string.
def vowelsPuzzle(clue: str):
    nospaces = ''.join(ch.upper() for ch in clue if ch.isalpha())
    vowels = ['A', 'E', 'I', 'O', 'U']
    novowels = ''.join(ch for ch in nospaces if ch not in vowels)
    finalOutput = ''
    spaceProb = 0.00
    for ch in novowels:
        finalOutput += ch
        spaceProb += 0.15
        if random() < spaceProb:
            finalOutput += ' '
            spaceProb = 0.00
    return finalOutput
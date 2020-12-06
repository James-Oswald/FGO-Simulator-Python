
import json
import numpy as np

numberOfPulls = 10
characterStarRates = [0.28, 0.28, 0.4, 0.03, 0.01] 
characterDataFile = open("fgo.json", "r")
characterData = characterDataFile.read()
characterList = json.loads(characterData) 
characterProbList = []
for rarity in range(1, 6):
    characterProbList.append([char for char in characterList if char["rarity"] == rarity])
    
for _ in range(0, 10):
    dropTable = np.random.choice(characterProbList, p=characterStarRates)
    pull = np.random.choice(dropTable)
    stars = "✯" * pull["rarity"]
    print("You pulled a " + stars + " " + pull["name"])




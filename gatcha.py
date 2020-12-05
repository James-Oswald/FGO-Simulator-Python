
# ============= Includes ==============================
import json                                     # use this to read fgo.json fgo data
import tarfile                                  # use this to read the compressed fgoImages.tgz images
import tkinter as tk                            # this is the GUI library 
from random import choice                       # use this to pick a random element from an array
from PIL import Image, ImageTk                  # use this to set up the and load images into the GUI 
from numpy.random import choice as npchoice     # use this to pick a random element from an array with a probability distribution

# ============= Set up GUI ==============================

window = tk.Tk()                                                #initialize the window 
window.geometry("1300x800")                                     #set the window size
(pulls := tk.Frame(window, height=140)).pack(side=tk.TOP)       #add the pulls list frame to the window                   
(controls := tk.Frame(window)).pack(side=tk.TOP)                #add the controls frame to the window
(collection := tk.Frame(window)).pack(side=tk.BOTTOM)           #add the collection frame to the window 
(singlePull := tk.Button(controls, text="1 Pull", command=lambda:pull(1))).grid(row=0, column=0)   #add the single pull button
(tenPull := tk.Button(controls, text="10 Pull", command=lambda:pull(10))).grid(row=0, column=1)    #add the ten pull button
(clearBut := tk.Button(controls, text="clean", command=lambda:clear())).grid(row=0, column=2)   #add the clear button

# ============= Set up Resources =========================

rarityColors = ["#a97142","#a97142","#a97142","#bec2cb","#ffd700"]  #the card colors for each rarity from 1 to 5 star 
pullChances = [0.28, 0.28, 0.4, 0.03, 0.01]                         #probilities of each rarity being pulled
#Load the charaters data into a list seperated by their rarity
charList = json.loads(open("fgo.json", "r").read())                 
charList = [[char for char in charList if char["rarity"] == rarity] for rarity in range(1, 6)]
#Load the charaters images into dictionary indexed by their ids
tar = tarfile.open("fgoImages.tgz", "r:gz")
images = {int(file.name[:-4]) : ImageTk.PhotoImage(Image.open(tar.extractfile(file)).resize((100, 100))) for file in tar.getmembers()}

# ============ Application State ==========================

charsPerRow = 10        #number of Charaters to display on each row
currentCharaters = []   #Charaters currently displayed as pulled
pulledCharaters = []    #Charaters displayed in your list of previously pulled charaters

# ============= Helper Functions ==========================

#setup a charater's card and add it to a given frame
def addCard(frame, char, row, col):
    backgroundColor = rarityColors[char["rarity"] - 1]  
    card = tk.Frame(frame, bg=backgroundColor)
    tk.Label(card, text=char["name"] + "\n" + ("✯" * char["rarity"]), bg=backgroundColor).grid(row=0) 
    tk.Label(card, image=images[char["id"]]).grid(row=1)
    card.grid(row=col, column=row)

# ============= Application Actions =======================

#clear the current charter and pulled charter frames
def clear():
    global currentCharaters, pulledCharaters
    currentCharaters, pulledCharaters = [], []
    for child in pulls.winfo_children():      #destroy the cards in the pull frame 
        child.destroy()
    for child in collection.winfo_children(): #destroy the cards in the collection frame 
        child.destroy()

#pull a given number of charters and create their cards
def pull(numPulls):
    global currentCharaters, pulledCharaters 
    pulledCharaters += currentCharaters
    currentCharaters = []
    for i in range(numPulls):  #pull the charaters 
        currentCharaters.append(choice(npchoice(charList, None, p=pullChances)))
    for child in pulls.winfo_children():      #destroy the cards in the pull frame 
        child.destroy()
    for child in collection.winfo_children(): #destroy the cards in the collection frame 
        child.destroy()
    for i in range(len(currentCharaters)):    #add the cards in the pull frame 
        addCard(pulls, currentCharaters[i], i % charsPerRow, i // charsPerRow)
    for i in range(len(pulledCharaters)):     #add the cards in the collection frame 
        addCard(collection, pulledCharaters[i], i % charsPerRow, i // charsPerRow)

#start the program
window.mainloop()


import json
import base64
import threading
import tkinter as tk
from random import choice
from PIL import Image, ImageTk
from urllib.request import urlopen, Request
from numpy.random import choice as npchoice

charList = json.loads(open("fgo.json", "r").read())
charList = [[char for char in charList if char["rarity"] == rarity] for rarity in range(1, 6)]

# ============ Application State ==========================

currentCharaters = []   #Charaters currently displayed as pulled
pulledCharaters = []    #Charaters displayed in your list of previously pulled charaters
charImageData = {}
charImages = {}

# ============= Application Actions =======================

def clear():
    global currentCharaters, pulledCharaters
    currentCharaters, pulledCharaters = [], []

def pull(numPulls):
    global currentCharaters, pulledCharaters 
    pulledCharaters += currentCharaters
    currentCharaters = []
    for i in range(numPulls):
        currentCharaters.append(choice(npchoice(charList, None, p=[0.28, 0.28, 0.4, 0.03, 0.01])))
    renderMain()


def fetchFGOimg(char):
    global charImageData
    img = Image.open(urlopen(Request(char["img1"], headers={'User-Agent':'Mozilla'})))
    charImageData[char["id"]] = img.resize((250, 250))

def renderMain():
    global charImages
    for child in pulls.winfo_children():
        child.destroy()
    for child in collection.winfo_children():
        child.destroy()
    needURLs = [char for char in currentCharaters if charImages.get(char["id"]) == None]
    threads = [threading.Thread(target=fetchFGOimg, args=(char,)) for char in needURLs]
    
    charImages = {**charImages, **{char["id"]:ImageTk.PhotoImage(charImageData[char["id"]]) for char in needURLs}}
    for char in currentCharaters:
        card = tk.Frame(pulls)
        tk.Label(card, text=char["name"] + "\n" + ("✯" * char["rarity"])).grid(row=0) 
        tk.Label(card, image=charImages[char["id"]]).grid(row=1)
        card.pack(side=tk.LEFT)

window = tk.Tk()
window.geometry("800x600")
(pulls := tk.Frame(window)).pack(side=tk.TOP)
(controls := tk.Frame(window)).pack(side=tk.TOP)
(collection := tk.Frame(window)).pack(side=tk.BOTTOM)
(singlePull := tk.Button(controls, text="1 Pull", command=lambda:pull(1))).grid(row=0, column=0)
(tenPull := tk.Button(controls, text="10 Pull", command=lambda:pull(10))).grid(row=0, column=1)

window.mainloop()
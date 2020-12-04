

import json
import base64
import tkinter as tk
import multiprocessing
from random import choice
from PIL import Image, ImageTk
from urllib.request import urlopen, Request
from numpy.random import choice as npchoice

charList = json.loads(open("fgo.json", "r").read())
charList = [[char for char in charList if char["rarity"] == rarity] for rarity in range(1, 6)]

# ============ Application State ==========================

currentCharaters = []   #Charaters currently displayed as pulled
pulledCharaters = []    #Charaters displayed in your list of previously pulled charaters
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

def renderMain():
    global charImages
    for child in pulls.winfo_children():
        child.destroy()
    for child in collection.winfo_children():
        child.destroy()
    def fetchFGOimg(url):
        global charImages
        img = Image.open(urlopen(Request(char["img1"], headers={'User-Agent':'Mozilla'}))).resize((250, 250))
        charImages[char["id"]] = ImageTk.PhotoImage(img)
    needURLs = [char["img1"] for char in charImages if charImages.get(char["id"]) == None]
    pool = multiprocessing.Pool(processes=4)
    pool.map(fetchFGOimg, needURLs)
    pool.join()
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
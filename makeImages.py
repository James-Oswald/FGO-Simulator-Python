
#This program downloads all the first URL's image for each charater in fgo.json and puts it inside 
#the zip folder fgoImages.tgz with the charaters ID as its name

import io
import json
import tarfile
from PIL import Image
from urllib.request import urlopen, Request

charList = json.loads(open("fgo.json", "r").read())
tar = tarfile.open("fgoImages.tgz","w:gz")
for char in charList:
    img = Image.open(urlopen(Request(char["img1"], headers={'User-Agent':'Mozilla'}))).resize((250, 250))
    imgFileData = io.BytesIO()
    img.save(imgFileData, format="PNG")
    info = tarfile.TarInfo(name=(str(char["id"]) + ".png"))
    info.size = imgFileData.getbuffer().nbytes
    imgFileData.seek(0)
    tar.addfile(tarinfo=info, fileobj=imgFileData)
    print("pulled %s wrote %s" % (char["img1"], info.name))

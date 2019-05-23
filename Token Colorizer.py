import easygui
import PIL
import random
from PIL import Image
from PIL import ImageOps

done = True
tokenpath = []


##pick the file, then add it to our collection
easygui.msgbox("Please select a black and white token.")

while done == True:
    path = easygui.fileopenbox()
    tokenpath.append(path)
    ## add another or finish?
    exitmessage = "Would you like to choose another token to import?"
    title = "I'm just wondering, bro"
    done = easygui.ynbox(exitmessage, title)


## reset, new check and new list for textures
done = True
texturepath = []

## check multiple textures
easygui.msgbox("Please select a pattern to apply to the token image. The pattern must be at least as large as the token image.")

while done == True:
    newpath = easygui.fileopenbox()
    texturepath.append(newpath)
    ## add another or finish?
    exitmessage = "Would you like to choose another pattern to import?"
    title = "I'm just wondering, bro"
    done = easygui.ynbox(exitmessage, title)



## batch convert to images

tokens = []
textures = []
mwidth = 0
mheight = 0

for pathway in tokenpath:
    img = Image.open(pathway)
    img = img.convert("RGBA")
    tempwidth, tempheight = img.size
    if tempwidth > mwidth:
        mwidth = tempwidth
    if tempheight > mheight:
        mheight = tempheight
    tokens.append(img)

    
for path in texturepath:
    img = Image.open(path)
    img = img.convert("RGBA")
    texwidth, texheight = img.size
    if texwidth > mwidth or texheight >mheight:
        img = img.resize((mwidth, mheight))
    textures.append(img)


## use RGB values to make a transparency and apply the texture as an alpha layer

finished = []
for texture in textures:
    for token in tokens:

        newdata = []
        ## find length of token for tracking purposes
        width, height = token.size
        distance = width * height

        ##check



        ## convert to data
        texdata = list(texture.getdata())
        tokedata = list(token.getdata())


        ## Setup values for readability and tracking
        i = 0
        red = 0
        green = 1
        blue = 2

        ##go line by line using i to track where in the list we are.
        ##If the pixel is not an alpha value and the pixel values are equal
        ##      combine the colors to the average
        ##      put those values into a new list
        ##      append that list of values into a new image
        ##else just put the original pixel into the new one.
        
        for i in range(distance):

            #if tokedata[i][red] <= 50 and tokedata[i][green] <= 50 and tokedata[i][blue] <= 50:
             #   newdata.append(tokedata[i])
            
            if tokedata[i][3] > 0 and tokedata[i][red] == tokedata[i][green] and tokedata[i][red] == tokedata[i][blue]:
                percent = (tokedata[i][red] / 255)
                newred = int(texdata[i][red] * percent)
                newgreen = int(texdata[i][green] * percent)
                newblue = int(texdata[i][blue] * percent)

                newpixel = [newred, newgreen, newblue, 255]
                newdata.append(newpixel)

            else:
                newdata.append(tokedata[i])

        ## build a new image, populate it with the data needed, add it to our finished list of images        
        newimage = Image.new("RGBA", token.size)
        newimage.putdata([tuple(pixel) for pixel in newdata])
        finished.append(newimage)

## Choose an output file

path = ""
while path == "":
    easygui.msgbox("Please select a folder to deposit all of these tokens.")
    path = easygui.diropenbox() + "/"

randname = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
naming = random.choice(randname)
for i in range(4):
    naming += random.choice(randname)

count = 0
for picture in finished:
    thispath = path + naming + str(count) + ".png"
    picture.save(thispath, "PNG")
    count += 1



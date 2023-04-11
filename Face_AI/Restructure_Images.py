import os, random, subprocess

A = os.listdir("C:/Users/cnfer/OneDrive/Desktop/Scripts/NewFaces/lfw")
for x in A:
    randompic = random.choice(os.listdir("C:/Users/cnfer/OneDrive/Desktop/Scripts/NewFaces/lfw/"+x))
    picpath = "C:/Users/cnfer/OneDrive/Desktop/Scripts/NewFaces/lfw" +str(x)+"/"+randompic
    os.popen('cd C:/Users/cnfer/OneDrive/Desktop/Scripts/NewFaces/lfw/'+str(x)+' && move ' +str(randompic)+' C:/Users/cnfer/OneDrive/Desktop/Scripts/NewFaces')
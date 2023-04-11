import os
import random
import subprocess

voicefile = input("Which voice would you like to find a face for?  ")
B = os.listdir('./Faces')
A =[]
ADeny = []
ADenyIndex = []
for x in B:
    A.append(x)
Attempts = []
Successes = []
Percentages = []
zeroone=[0,0]
alen = len(A)
for k in range(alen):
    Attempts.append(0)
    Successes.append(0)
    Percentages.append(0)
print("\nThe directory contains "+str(alen)+" elements.\n")
n = random.choice(A)
print("Here is a random entry from the directory: " + n)
print("It's position is: "+str(A.index(n))+"\n")
m = random.choice(A)
print("Here is another random entry from the directory: " + m)
print("It's position is: "+str(A.index(m)) +"\n")
w = input("Seems everything is working properly, would you like to continue the script?    ")
def runfacescan():
    print("Trying "+ str(int(howmanyiterations)) + f" face combinations with voice: {voicefile}\n")
    for i in range(int(howmanyiterations)):
        n = str(random.choice(A))
        nindex = A.index(n)
        m = str(random.choice(A))
        def checkequality():
            if m == n:
               m = str(random.choice(A))
               checkequality()
        mindex = A.index(m)
        Attempts[nindex]+=1
        Attempts[mindex]+=1
        stream = os.popen(f"python3 ./facevoice-master/facevoice.py v2f -c ./facevoice-master/facevoice-checkpoint-v2f --voice {voicefile} --face0 ./Faces/"+n+" --face1 ./Faces/"+m).read()
        print(stream)
        output = str(stream).replace("predicted matching face: face","").strip("\n")
        if output[0] == "1":
            Successes[mindex]+=1
            zeroone[1]+=1
        elif output[0] == "0":
            Successes[nindex]+=1
            zeroone[0]+=1
        else:
           print("Running face0 and face1 through the algorithm caused an unexpected result")
        print("Combinations successfully tried: "+str(i+1)+" of "+str(int(howmanyiterations))+"\n")

    for j in range(len(A)): 
        print(A[j] +": Attempts ("+str(Attempts[j])+"), Successes ("+str(Successes[j])+")")
        if Attempts[j] != 0:
            Percentages[j] = 100 * Successes[j]/Attempts[j]
    PercentageIndex = []
    for j in range(len(A)):
        PercentageIndex.append([A[j], Percentages[j]])
    def takeSecond(elem):
        return elem[1]
    PercentageIndex.sort(key = takeSecond)
    for j in range(len(A)):
        print(str(PercentageIndex[j][0]) + " percentage of success: " + str(PercentageIndex[j][1])+"% ")
    print("\n\nBias Statistics: \nAmount of zeroes: "+str(zeroone[0])+"    Ones: "+str(zeroone[1])+"\n\nAs a reminder, numbers displaying 0% have not been tested and are thus still stored as int.\nThose that have been tested are stored as float, and thus show up as 0.0%.\n")
    print("The following images have been removed from the algorithm: (no image files means that none have been removed)\n \n")
    for j in range(len(A)):
        if (PercentageIndex[j][1] < 50 and isinstance(PercentageIndex[j][1],float)):
            ADeny.append(PercentageIndex[j][0])
            ADenyIndex.append(A.index(PercentageIndex[j][0]))
            print(str(PercentageIndex[j][0]))
    if len(A) < 4:
        print("Here are the most likely candidates: \n\n")
        print(*A, sep = "\n")
        openthem = input("\nWould you like me to open the image files for you?    ")
        if openthem == "y" or openthem == "Y":
            for x in A:
                os.popen("./Faces/"+x)
    else:
        ADenyIndex.sort()
        listshift = 0
        for h in ADenyIndex:
            indexpart = h - listshift
            Attempts.pop(indexpart)
            Successes.pop(indexpart)
            listshift +=1
        for h in ADeny:
            A.remove(h)
        ADeny.clear()
        ADenyIndex.clear()
        Percentages.clear()
        for e in range(len(A)):
            Percentages.append(int(0))
        print("\nThere are now "+str(len(A))+" images left to be tested.\n(Att = "+str(len(Attempts))+", Succ = "+str(len(Successes))+")\n\n")
        PercentageIndex.clear()
        runfacescan()

if w == "y" or w == "Y":
    #voicefile = input("What voice file (in the proper directory) would you like to test?   ")
    #os.popen("C:/Users/cnfer/OneDrive/Desktop/Scripts/Voices/"+voicefile)
    #shouldcontinue = input("Is this the correct file?   ")
    #if shouldcontinue == "y" or shouldcontinue == "Y":
    howmanyiterations = abs(int(input("How many combinations would you like the program to initially try? (more combinations = more accuracy)   ")))
    runfacescan()
else:
    print("aight nvm")
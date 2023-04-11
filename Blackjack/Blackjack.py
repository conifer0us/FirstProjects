import random
import os
import getpass

cards = ['A','A','A','A',2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,'J','J','J','J','Q','Q','Q','Q','K','K','K','K']
deck = []
moneyleft = [0]
betamount = [0]
decks = input("How many decks in the shoe?   ")
count = 0
dealercards = []
playercards = []
dealerscore = []
playerscore = []
finalplayerscore = []
finaldealerscore = []
originalcards = []
splitcounter = [0]
hitques = ""
issplit = False


def playagain():
    global moneyleft
    global hitques
    global issplit
    if issplit==True and splitcounter[0]==1 or issplit==False:
        play = input("Play again?   ")
        if play == 'Y' or play == 'y':
            os.system('cls')
            print("You now have "+str(moneyleft[0])+" dollars!")
            if input("\nPress enter to continue|  ") != "stop":
                os.system('cls')
                originalcards.clear()
                splitcounter[0]=0
                issplit = False
                card1 = random.choice(deck)
                card2 = random.choice(deck)
                card3 = random.choice(deck)
                card4 = random.choice(deck)
                deck.remove(card3)
                deck.remove(card4)
                deck.remove(card1)
                deck.remove(card2)
                playhand(card1,card2,card3,card4)
        elif issplit==True and splitcounter[0]==0:
            print("\n")
        else:
            print("Thanks for playing! Your final amount was:   "+str(moneyleft[0]))
            exit()
def scoredealer():
    global dealerscore
    possiblescores = [0]
    for i in dealercards:
        if i == 'K' or i == 'J' or i == 'Q':
            for m in range(len(possiblescores)):
                possiblescores[m]+=10
        elif i == 'A':
            for m in range(len(possiblescores)):
                possiblescores.append(possiblescores[m]+11)
                possiblescores[m]+=1
        else:
            for m in range(len(possiblescores)):
                possiblescores[m]+=i
    dealerscore.clear()
    finaldealerscore.clear()
    for j in possiblescores:
        if j not in dealerscore and j <22:
            dealerscore.append(j)
        if j > 21:
            finaldealerscore.append(j)
        
def scoreplayer():
    global playerscore
    possiblescores = [0]
    for i in playercards:
        if i == 'K' or i == 'J' or i == 'Q':
            for m in range(len(possiblescores)):
                possiblescores[m]+=10
        elif i == 'A':
            for m in range(len(possiblescores)):
                possiblescores.append(possiblescores[m]+11)
                possiblescores[m]+=1
        else:
            for m in range(len(possiblescores)):
                possiblescores[m]+=i
    playerscore.clear()
    finalplayerscore.clear()
    for j in possiblescores:
        if j not in playerscore and j <22:
            playerscore.append(j)
        if j > 21:
            finalplayerscore.append(j)
def showgamestate(isdrawing):
    global dealerscore
    global playerscore
    scoreplayer()
    scoredealer()
    if isdrawing:
        print("The dealer has a score of ? with the cards:   ")
        print("?    "+str(dealercards[1])+"\n------------------------------\n")
    else:
        try: print("The dealer has a score of "+str(max(dealerscore))+" with the cards:   ")
        except: print("The dealer has a score of "+str(min(finaldealerscore))+" with the cards:   ")
        print(*dealercards, sep='    ', end = "\n------------------------------\n")
    try: print("You have a score of "+str(max(playerscore))+" with the cards:   ")
    except: print("You have a score of "+str(min(finalplayerscore))+" with the cards:   ")
    print(*playercards, sep='    ', end = "\n------------------------------\n")

def givedealercard():
    global playercards
    global deck
    m = random.choice(deck)
    dealercards.append(m)
    deck.remove(m)

def giveplayercard():
    global dealercards
    global deck
    m = random.choice(deck)
    playercards.append(m)
    deck.remove(m)

def hitorstay():
    global dealerscore
    global playerscore
    global betamount
    global moneyleft
    global hitques
    global issplit
    hitques = input("Hit or stay? (h,s,double,split)   ")
    if hitques == 's' or hitques == 'S':
        print("\n\nDealer will now draw.\n\n")
        showgamestate(False)
    elif hitques == 'h' or hitques == 'H':
        giveplayercard()
        showgamestate(True)
        if playerscore == []:
            print("You went over 21 and lost! You lost "+str(betamount[0])+" dollars!")
            moneyleft[0]-=betamount[0]
        else: 
            hitorstay()
    elif hitques == "double" or hitques == "Double":
        if len(playercards)==2:
            betamount[0] = 2 * betamount[0]
            giveplayercard()
            showgamestate(False)
            if playerscore == []:
                print("You went over 21 and lost! You lost "+str(betamount[0])+" dollars!")
                moneyleft[0]-=betamount[0]
        else:
            print("You can't double in this situation")
            hitorstay()
    elif hitques == 'split' or hitques == "Split":
        if splitcounter[0] < 2 and playercards[0]==playercards[1] and len(playercards)==2 and issplit == False:
            print("*Reminder, you can only split once in this game because the coder was lazy*\n\nHere is your first hand:\n")
            issplit = True
            card1 = random.choice(deck)
            deck.remove(card1)
            playhand(originalcards[0],card1,dealercards[0],dealercards[1])
            print("Here is your second hand:\n")
            card2 = random.choice(deck)
            deck.remove(card2)
            splitcounter[0]+=1
            playhand(originalcards[1],card2,dealercards[0],dealercards[1])
        else:
            print("You cannot split in this situation")
            hitorstay()
    else:
        print("This is not recognized as a proper action. Please enter split, double, h, or s")
        hitorstay()

def continuegamelogic():
    global dealerscore
    global playerscore
    global betamount
    global moneyleft
    hitorstay()
    if playerscore != []:
        while max(dealerscore) < 17 or (len(dealerscore)>1 and max(dealerscore)==17):
            givedealercard()
            showgamestate(False)
            if dealerscore == []: break
        if dealerscore == []:
            print("you win! You have won "+str(betamount[0])+" dollars!")
            moneyleft[0] += betamount[0]
        else:
            print("\nThe dealer must stop drawing.\n")
            if max(playerscore) < max(dealerscore):
                print("you lost :( You have lost "+str(betamount[0])+" dollars!")
                moneyleft[0] -= betamount[0]
            elif max(playerscore) > max(dealerscore):
                print("you win! You have won "+str(betamount[0])+" dollars!")
                moneyleft[0] += betamount[0]
            elif max(playerscore) == max(dealerscore):
                print("You pushed. You will neither gain nor lose money.")
  

def checkblackjack():
    global hitques
    def isblackjack(list):
        if 'A' in list and ('K' in list or 'Q' in list or 'J' in list or 10 in list):
            return True
        else:
            return False
    if isblackjack(playercards) and not isblackjack(dealercards):
        showgamestate(False)
        print("\n\nYou have blackjack and the dealer does not. You have won "+str(1.5 * betamount[0])+" dollars.")
        moneyleft[0] += 1.5*betamount[0]
        if splitcounter[0]!=0 or (hitques!='split' and hitques!="Split"): playagain()
    elif isblackjack(playercards) and isblackjack(dealercards):
        showgamestate(False)
        print("\n\nYou have pushed with the dealer, as you both have blackjack.")
        if splitcounter[0]!=0 or (hitques!='split' and hitques!="Split"): playagain()
    elif isblackjack(dealercards) and not isblackjack(playercards):
        showgamestate(False)
        print("\n\nThe dealer has blackjack and you do not. You have lost "+str(betamount[0])+" dollars.")
        moneyleft[0] -= betamount[0]
        if splitcounter[0]!=0 or (hitques!='split' and hitques!="Split"): playagain()

def playhand(card1,card2, card3, card4):
    global playerscore
    global playercards
    global dealercards
    global dealerscore
    global moneyleft
    global betamount
    global decks
    global deck
    global hitques
    if len(deck) < 20:
        deck.clear()
        for n in range(decks):
            deck+=cards
        print('Too few cards. Reshuffling. \n\n')
    playercards.clear()
    dealercards.clear()
    dealerscore.clear()
    playerscore.clear()
    def checkbetamount():
        betamount[0] = abs(int(input("How much would you like to wager on this hand?   ")))
        if betamount[0] > moneyleft[0]:
            print("This is more money than you have left. Please bet less than "+str(moneyleft[0])+"\n\n")
            checkbetamount()
    if not issplit: checkbetamount()
    dealercards.append(card3)
    dealercards.append(card4)
    playercards.append(card1)
    playercards.append(card2)
    if len(originalcards) == 0:
        originalcards.append(card1)
        originalcards.append(card2)
    checkblackjack()
    showgamestate(True)
    continuegamelogic()
    if splitcounter[0]!=0 or (hitques!='split' and hitques!="Split"): playagain()

def betmoney():
    print("We shall now define an allowance for you to bet with.")
    howmuch = int(input("How much are you willing to wager on this game?   "))
    def checkstaffpassword():
        global count
        if getpass.getpass("Get in touch with Connor to enter staff password. Without this, you will not be able to wager money on the game!   ") == "staffpass":
            moneyleft[0] = howmuch
            card1 = random.choice(deck)
            card2 = random.choice(deck)
            card3 = random.choice(deck)
            card4 = random.choice(deck)
            deck.remove(card1)
            deck.remove(card2)
            deck.remove(card3)
            deck.remove(card4)
            playhand(card1,card2,card3,card4)
        else:
            print("Staff Password was incorrect...")
            count+=1
            if count > 5:
                print("too many failed attempts")
            else:
                checkstaffpassword()
    checkstaffpassword()

try: decks = int(decks)
except:
    print("Shoe will be set to default value of 6. Try putting an actual number in next time.")
    decks = 6
if int(decks) < 6:
    print("Minimum size of shoe in this game is 6 decks...")
    decks = 6
for i in range(decks):
    deck += cards
j = 0
for i in range(len(deck)):
    if deck[i] == 'A':
        j+=1
print("There are "+str(j/4)+" decks in the shoe. \n\n")
betpage = input('Press enter to clear and start the game| ')
if betpage == "":
    os.system('cls')
    betmoney()
else:
    betpageagain = input("Would you like to continue the game or not? (enter y for yes)    ")
    if betpageagain == 'y' or betpageagain == 'Y':
        os.system('cls')
        betmoney()
    else:
        print("\n\nYour loss...")
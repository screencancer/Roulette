import random
import os
import sqlite3


#defining connection and cursors
conn = sqlite3.connect("store_wins.db")

cursor = conn.cursor()
#create wins table


def create_table():
    command1 = """CREATE TABLE IF NOT EXISTS
    data([wins] Integer, [losses] Integer)"""

    cursor.execute(command1)
    print("Table created")


def fetch_WL():
    command2 = """SELECT wins FROM data"""
    cursor.execute(command2)
    win = cursor.fetchone()
    for x in win:
        global wins
        wins = x


bullets = []
punishment = None
wins = 0
losses = 0


def playagain():
    play = input(f"Enter p to play or q to quit {wins} wins so far\n")
    if play == 'p':
        global bullets
        bullets.clear()
        getnumofbullets()
    elif play == 'q':
        quit()
        conn.close()
    else:
        print("Select a valid option")
        playagain()


def getnumofbullets():
    amount = int(input("How many bullets do you want to put in 1-5: \n"))
    if amount > 5:
        print("Too many try again")
        getnumofbullets()
    while amount != 0:
        chamber = random.randint(1,6)
        global bullets
        if chamber not in bullets:
            bullets.append(chamber)
            amount -= 1
    chooserisk()


def chooserisk():
    print("1: No punishment playing for fun\n"
          "2: PC restart")
    choice = int(input("Choose your risk from the list above\n"))

    if choice > 2 or choice < 1:
        print("Please pick between 1-2")
        chooserisk()
    global punishment
    punishment = choice
    shot()


def shot():
    shotnum = random.randint(0,6)
    if shotnum in bullets:
        print("Game over you lost commencing punishment")
        global losses
        losses += 1
        data_entry()
        ExecutePunishment()
    else:
        print("You won!!")
        global wins
        wins += 1
        data_entry()
        playagain()


def data_entry():
    conn.execute("""UPDATE data SET wins = ?""", (wins,))
    conn.execute("""UPDATE data SET losses = ?""", (losses,))
    conn.commit()


def ExecutePunishment():
    if punishment == 1:
        playagain()
    elif punishment == 2:
        os.system("shutdown /r")


create_table()
fetch_WL()
playagain()
chooserisk()
shot()


import sqlite3
import random
info = dict()
id = 0
class Account:
    def __init__(self):
        self.account = ""
        self.password = "".join([str(random.randint(0, 9)) for _ in range(4)])
        self.balance = 0
    def creat(self):
        digitsSum = [4, 0, 0, 0, 0, 0]
        account = "400000".split()
        for i in range(9):
            randNum = random.randint(0, 9)
            digitsSum.append(randNum)
            account.append(str(randNum))
        sumOfDigits = 0
        for i in range(0, len(digitsSum)):
            if i % 2 == 0:
                digitsSum[i] = int(digitsSum[i]) * 2
                if digitsSum[i] > 9:
                    digitsSum[i] -= 9
            sumOfDigits += digitsSum[i]
        checksum = str((sumOfDigits // 10 + 1) * 10 - sumOfDigits)
        if checksum == "10":
            checksum = "0"
        account.append(checksum)
        self.account = "".join(account)
        print(f"\nYour card has been created\nYour card number:\n{self.account}\nYour card PIN:\n{self.password}")
    def printBalance(self):
        print(f"\nBalance: {self.balance}")

def creatNewAccount():
    newAccount = Account()
    newAccount.creat()
    info[newAccount.account] = newAccount
    global id
    operateDB(f"INSERT INTO card (id, number, pin, balance) VALUES ({id}, {newAccount.account}, {newAccount.password}, "
              f"{newAccount.balance})")
    # global id
    id += 1

def loginAccount():
    print("\nEnter your card number:")
    inputAccount = input()
    print("Enter you PIN:")
    inputPin = input()
    if inputAccount not in info or info[inputAccount].password != inputPin:
        print("\nWrong card number or PIN!")
    elif info[inputAccount].password == inputPin:
        print("\nYou have successfully logged in!")
        while True:
            print("\n1. Balance\n2. Add income\n3. Do transfer\n \
            4. Close account\n5. Log out\n0. Exit")
            option = input()
            if option == "1":
                # info[inputAccount].printBalance()
                readBalance(inputAccount)
            elif option == "2":
                income = int(input("Enter income:\n>"))
                modifyBalance(inputAccount, income)
            elif option == "3":
                transferAccount = input("Transfer\nEnter card number\n>")
                if not isValidNumber(transferAccount):
                    continue
                if not checkIfAccount(transferAccount):
                    continue
                moneyTransfer = int(input("Enter how much money you want to transfer:\n>"))
                if moneyTransfer > readBalance(inputAccount):
                    print('Not enough money!')
                    continue
                modifyBalance(inputAccount, -moneyTransfer)
                modifyBalance(transferAccount, moneyTransfer)
                continue
            elif option == "4":
                closeAccount(inputAccount)
            elif option == "5":
                print("\nYou have successfully logged out!")
                break
            elif option == "0":
                print("\nBye!")
                exit()

def menu():
    while True:
        print("\n1. Create an account\n2. Log into account\n0. Exit")
        choice = input()
        if choice == "1":
            creatNewAccount()
        elif choice == "2":
            loginAccount()
        elif choice == "0":
            print("Bye!")
            break


def operateDB(command):
    # command is string
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()

def initialiseDB():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE card \
                (id INTEGER, \
                number TEXT, \
                pin TEXT, \
                balance INTEGER DEFAULT 0);')
    conn.commit()

def readBalance(accountNumber):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute(f'SELECT balance FROM card WHERE number = {accountNumber}')
    balance = int(cur.fetchone()[0])
    print(f'Balance: {balance}')
    return balance

def modifyBalance(accountNumber, money):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    oldBalance = int(cur.execute(f'SELECT balance FROM card WHERE number = {accountNumber}').fetchone()[0])
    newBalance = oldBalance + money
    cur.execute(f'UPDATE card SET balance = {newBalance} WHERE number = {accountNumber}')
    conn.commit()
    if money > 0:
        print("Income was added!")

def isValidNumber(number):
    n = len(number)
    number = list(number)
    if n != 16:
        print("Number must be 16 digits.")
        return False
    for i in range(n - 1):
        number[i] = int(number[i])
        if i % 2 == 0:
            number[i] *= 2
        if number[i] > 9:
            number[i] -= 9
    number[-1] = int(number[-1])
    if sum(number) % 10 != 0:
        print("Probably you made a mistake in the card number. Please try again!")
        return False
    else:
        return True

def checkIfAccount(number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    checkRes = cur.execute(f"SELECT number FROM card WHERE number = {number}").fetchone()
    conn.commit()
    if not checkRes:
        print("Such a card does not exist.")
        return False
    else:
        return True

def closeAccount(accountNumber):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM card WHERE number = {accountNumber}")
    conn.commit()
    print("The account has been closed!")

def initialise():
    try:
        initialiseDB()
    except:
        pass

initialise()
menu()
import random
info = dict()
class Account:
    def __init__(self):
        self.account = "400000" + "".join([str(random.randint(0, 9)) for _ in range(9)]) + "0"
        self.password = "".join([str(random.randint(0, 9)) for _ in range(4)])
        self.balance = 0
    def creat(self):
        print(f"\nYour card has been created\nYour card number:\n{self.account}\nYour card PIN:\n{self.password}")
    def printBalance(self):
        print(f"\nBalance: {self.balance}")

def creatNewAccount():
    newAccount = Account()
    newAccount.creat()
    info[newAccount.account] = newAccount

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
            print("\n1. Balance\n2. Log out\n0. Exit")
            option = input()
            if option == "1": info[inputAccount].printBalance()
            elif option == "2":
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

menu()
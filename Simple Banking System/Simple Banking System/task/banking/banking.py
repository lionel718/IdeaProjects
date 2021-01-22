# Write your code here
import random
def cardAnatomy():
    info = {}
    flag = True
    while True:
        if flag == False: break
        print("\n1. Create an account\n2. Log into account\n0. Exit")
        choice = input()
        if choice == "1":
            accountIdentifier = ""
            for i in range(9):
                accountIdentifier += str(random.randint(0, 9))
            cardNumber = "400000" + accountIdentifier + "5"
            password = ""
            for i in range(4):
                password += str(random.randint(0, 9))
            info[cardNumber] = []
            info[cardNumber].append(password)
            info[cardNumber].append(0)  # balance
            print("\nYour card has been created\nYour card number:\n{}".format(cardNumber))
            print("Your card PIN:\n{}".format(password))
        elif choice == "2":
            print("\nEnter your card number:")
            inputNumber = input()
            print("Enter your PIN:")
            inputPass = input()
            if inputNumber not in info:
                print("\nWrong card number or PIN!")
            elif info[inputNumber][0] != inputPass:
                print("\nWrong card number or PIN!")
            elif info[inputNumber][0] == inputPass:
                print("\nYou have successfully logged in!\n")
                while True:
                    print("1. Balance\n2. Log out\n0. Exit")
                    choiceOfLog = input()
                    if choiceOfLog == "1":
                        print("\nBalance: " + str(info[inputNumber][1]), "\n")
                    elif choiceOfLog == "2":
                        print("You have successfully logged out!")
                        break
                    elif choiceOfLog == "0":
                        flag = False
                        print("Bye!")
                        break
        elif choice == "0":
            print("Bye!")
            break
cardAnatomy()
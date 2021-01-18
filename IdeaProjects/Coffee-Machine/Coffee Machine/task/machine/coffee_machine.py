# Write your code here
def sayHello():
    welcome = "Starting to make a coffee\n" \
        "Grinding coffee beans\n" \
        "Boiling water\n" \
        "Mixing boiled water with crushed coffee beans\n" \
        "Pouring coffee into the cup\n" \
        "Pouring some milk into the cup\n" \
        "Coffee is ready!"
    print(welcome)

def calculateIngredient():
    print("Write how many cups of coffee you will need:")
    numberOfCups = int(input())
    water = numberOfCups * 200
    milk = numberOfCups * 50
    beans = numberOfCups * 15
    print("For {num} cups of coffee you will need:\n" \
          "{water} ml of water\n" \
          "{milk} ml of milk\n" \
          "{beans} g of coffee beans".format(num = numberOfCups, water = water, milk = milk, beans = beans))

def estimateAvaliability():
    water = int(input("Write how many ml of water the coffee machine has:\n")) // 200
    milk = int(input("Write how many ml of milk the coffee machine has:\n")) // 50
    beans = int(input("Write how many grams of coffee beans the coffee machine has:\n")) // 15
    required = int(input("Write how many cups of coffee you will need:\n"))
    cups = min(water, milk, beans)
    if(cups >= required):
        if(cups == required):
            print("Yes, I can make that amount of coffee")
        else:
            print("Yes, I can make that amount of coffee (and even {} more than that)".format(cups - required))
    else:
        print("No, I can make only {} cups of coffee".format(cups))
def buyFillTake():
    def printState(money, water, milk, beans, cups):
        print("\nThe coffee machine has:\n{0} of water\n{1} of milk\n"
              "{2} of coffee beans\n{3} of disposable cups\n"
              "{4} of money\n".format(water, milk, beans, cups, money))
    def buy():
        nonlocal initMoney, initWater, initMilk, initBeans, initCups
        buyWhat = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n")
        if buyWhat == '1':
            initWater -= 250
            initBeans -= 16
            initMoney += 4
        elif buyWhat == '2':
            initWater -= 350
            initMilk -= 75
            initBeans -= 20
            initMoney += 7
        elif buyWhat == '3':
            initWater -= 200
            initMilk -= 100
            initBeans -= 12
            initMoney += 6
        initCups -= 1
    def fill():
        nonlocal initWater, initMilk, initBeans, initCups
        initWater += int(input("Write how many ml of water do you want to add:\n"))
        initMilk += int(input("Write how many ml of milk do you want to add:\n"))
        initBeans += int(input("Write how many grams of coffee beans do you want to add:\n"))
        initCups += int(input("Write how many disposable cups of coffee do you want to add:\n"))

    def take():
        nonlocal initMoney
        print("I gave you $", initMoney)
        initMoney = 0


    initMoney, initWater, initMilk, initBeans, initCups = 550, 400, 540, 120, 9
    printState(initMoney, initWater, initMilk, initBeans, initCups)
    option = input("Write action (buy, fill, take)\n")
    if option == "buy":
        buy()
    elif option == "fill":
        fill()
    elif option == "take":
        take()
    printState(initMoney, initWater, initMilk, initBeans, initCups)
class Coffee:
    def keepTrackOfSupplies(self):
        def printState(money, water, milk, beans, cups):
            print("\nThe coffee machine has:\n{0} of water\n{1} of milk\n"
                  "{2} of coffee beans\n{3} of disposable cups\n"
                  "{4} of money\n".format(water, milk, beans, cups, money))
        def buy():
            nonlocal initMoney, initWater, initMilk, initBeans, initCups
            buyWhat = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n")
            if buyWhat == "back":
                return
            elif buyWhat == '1':
                if(initWater >= 250 and initBeans >= 16):
                    initWater -= 250
                    initBeans -= 16
                    initMoney += 4
                else:
                    if(initWater < 250):
                        print("Sorry, not enough water!\n")
                    elif(initBeans < 16):
                        print("Sorry, not enough coffee beans!\n")
                    return
            elif buyWhat == '2':
                if(initWater >= 350 and initMilk >= 75 and initBeans >= 20):
                    initWater -= 350
                    initMilk -= 75
                    initBeans -= 20
                    initMoney += 7
                else:
                    if(initWater < 350):
                        print("Sorry, not enough water!\n")
                    elif(initMilk < 75):
                        print("Sorry, not enough milk!\n")
                    elif(initBeans < 20):
                        print("Sorry, not enough coffee beans!\n")
                    return
            elif buyWhat == '3':
                if(initWater >= 200 and initMilk >= 100 and initBeans >= 12):
                    initWater -= 200
                    initMilk -= 100
                    initBeans -= 12
                    initMoney += 6
                else:
                    if(initWater < 200):
                        print("Sorry, not enough water!\n")
                    elif(initMilk < 100):
                        print("Sorry, not enough milk!\n")
                    elif(initBeans < 12):
                        print("Sorry, not enough coffee beans!\n")
                    return
            initCups -= 1
            print("I have enough resources, making you a coffee!\n")
        def fill():
            nonlocal initWater, initMilk, initBeans, initCups
            initWater += int(input("Write how many ml of water do you want to add:\n"))
            initMilk += int(input("Write how many ml of milk do you want to add:\n"))
            initBeans += int(input("Write how many grams of coffee beans do you want to add:\n"))
            initCups += int(input("Write how many disposable cups of coffee do you want to add:\n"))

        def take():
            nonlocal initMoney
            print("I gave you $", initMoney, "\n")
            initMoney = 0


        initMoney, initWater, initMilk, initBeans, initCups = 550, 400, 540, 120, 9
        # printState(initMoney, initWater, initMilk, initBeans, initCups)
        while True:
            option = input("Write action (buy, fill, take, remaining, exit)\n")
            if option == "buy":
                buy()
                # printState(initMoney, initWater, initMilk, initBeans, initCups)
            elif option == "fill":
                fill()
                # printState(initMoney, initWater, initMilk, initBeans, initCups)
            elif option == "take":
                take()
                # printState(initMoney, initWater, initMilk, initBeans, initCups)
            elif option == "remaining":
                printState(initMoney, initWater, initMilk, initBeans, initCups)
            elif option == "exit":
                break
coffee = Coffee()
coffee.keepTrackOfSupplies()
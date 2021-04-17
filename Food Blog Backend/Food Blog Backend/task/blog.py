import sys
import sqlite3
import argparse
# >>>>>>>>>>>>>>>>>>>> global <<<<<<<<<<<<<<<<<<<<<<
data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
recipeId = 1
serveId = 1
quantityId = 1
# ===================================================


def buildDB(name):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute("CREATE TABLE meals (meal_id INTEGER PRIMARY KEY, \
    meal_name TEXT NOT NULL UNIQUE);")
    conn.commit()
    cur.execute("CREATE TABLE ingredients (ingredient_id INTEGER PRIMARY KEY, \
    ingredient_name TEXT NOT NULL UNIQUE);")
    conn.commit()
    cur.execute("CREATE TABLE measures (measure_id INTEGER PRIMARY KEY, \
    measure_name TEXT UNIQUE);")
    conn.commit()
    conn.close()


def populateTable(name, flag='initialisation'):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    if flag == 'initialisation':
        for key in data.keys():
            i = 1
            for value in data[key]:
                cur.execute(f"INSERT INTO {key} \
                 VALUES ({i}, \"{value}\");")
                conn.commit()
                i += 1
    elif flag == 'recipes':
        global recipeId
        while True:
            recipeName = input("Recipe name: > ")
            if len(recipeName) == 0:
                conn.close()
                sys.exit(0)
            recipeDescription = input("Recipe description: > ")
            cur.execute(f"INSERT INTO {flag} \
                VALUES ({recipeId}, '{recipeName}', '{recipeDescription}')")
            conn.commit()
            populateServe(name, cur, conn)
            populateQuantity(name, cur, conn)
            recipeId += 1
    conn.close()


def populateServe(name, cur, conn):
    global serveId
    meals = cur.execute("SELECT * FROM meals").fetchall()
    conn.commit()
    for mealId, meal in meals:
        print(f"{mealId}) {meal}  ", end='')
    print("")
    mealId = input("Enter proposed meals separated by a space: > ")
    for i in range(len(mealId.split())):
        cur.execute(f"INSERT INTO serve VALUES \
                ({serveId}, {recipeId}, {int(mealId.split()[i])})")
        conn.commit()
        serveId += 1


def populateQuantity(name, cur, conn):
    global quantityId
    allMeasure = cur.execute("SELECT * FROM measures").fetchall()
    allMeasuresName = list()
    for i in range(len(allMeasure)):
        allMeasuresName.append(allMeasure[i][1])
    allIngredient = cur.execute("SELECT * FROM ingredients").fetchall()
    allIngredientName = list()
    for i in range(len(allIngredient)):
        allIngredientName.append(allIngredient[i][1])
    while True:
        temp = input("Input quantity of ingredient <press enter to stop>:")
        if temp == "":
            break
        temp = temp.split(" ")
        if len(temp) == 2:
            temp.insert(1, "")
        # if temp[1] in allMeasuresName:
        allMeasuresNameTime = 0
        allSimilarMeasures = list()
        if temp[1] != "":
            for i in range(len(allMeasuresName)):
                if temp[1] in allMeasuresName[i]:
                    allSimilarMeasures.append(allMeasuresName[i])
                    allMeasuresNameTime += 1
                if allMeasuresNameTime > 1:
                    break
            if allMeasuresNameTime > 1:
                print("The measure is not conclusive!")
                continue
            elif allMeasuresNameTime == 1:
                temp[1] = allSimilarMeasures[0]
        allIngredientNameTime = 0
        allSimilarIngredient = list()
        for i in range(len(allIngredientName)):
            if temp[2] in allIngredientName[i]:
                allIngredientNameTime += 1
                allSimilarIngredient.append(allIngredientName[i])
            if allIngredientNameTime > 1:
                break
        if allIngredientNameTime > 1:
            print("The ingredient is not conclusive!")
            continue
        elif allIngredientNameTime == 1:
            temp[2] = allSimilarIngredient[0]
        cur.execute(f"INSERT INTO quantity VALUES \
                    ({quantityId}, {int(temp[0])}, {recipeId}, \
                    {allMeasure[allMeasuresName.index(temp[1])][0]}, \
                    {allIngredient[allIngredientName.index(temp[2])][0]})")
        quantityId += 1
        conn.commit()



def createTable(name, tableName):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    if tableName == 'recipes':
        cur.execute("CREATE TABLE recipes (recipe_id INTEGER PRIMARY KEY, \
        recipe_name TEXT NOT NULL, recipe_description TEXT)")
        conn.commit()
    elif tableName == 'serve':
        cur.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
        cur.execute("CREATE TABLE serve (serve_id INTEGER PRIMARY KEY, \
        recipe_id INTEGER NOT NULL, meal_id INTEGER NOT NULL, \
        FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id), \
        FOREIGN KEY(meal_id) REFERENCES meals(meal_id))")
        conn.commit()
    elif tableName == 'quantity':
        cur.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
        cur.execute("CREATE TABLE quantity (quantity_id INTEGER PRIMARY KEY, \
        quantity INTEGER NOT NULL, \
        recipe_id INTEGER NOT NULL, \
        measure_id INTEGER NOT NULL, \
        ingredient_id INTEGER NOT NULL, \
        FOREIGN KEY(measure_id) REFERENCES measures(recipe_id) \
        FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id) \
        FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id))")
        conn.commit()
    conn.close()


def commandLine():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--ingredients")
    parser.add_argument("--meals")
    args = parser.parse_args()
    dbName = args.name
    ingredientsInput = args.ingredients
    mealsInput = args.meals
    if not ingredientsInput or not mealsInput:
        return False, dbName, None, None
    else:
        ingredientsInput = ingredientsInput.split(',')
        mealsInput = mealsInput.split(',')
        return True, dbName, ingredientsInput, mealsInput

def searchCommand(dbName, ingredients, meals):
    mealID = set()
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    for i in range(len(meals)):
        temp = cur.execute(f"SELECT meal_id FROM meals WHERE meal_name='{meals[i]}'").fetchall()
        conn.commit()
        mealID.add(temp[0][0])
    recipeID = set()
    for meal in mealID:
        temp = cur.execute(f"SELECT recipe_id FROM serve WHERE meal_id={meal}").fetchall()
        conn.commit()
        for temp1 in temp:
            recipeID.add(temp1[0])
    allIngredients = []
    intermidateIngre = cur.execute("SELECT ingredient_name FROM ingredients").fetchall()
    for temp in intermidateIngre:
        allIngredients.append(temp[0])
    for temp in ingredients:
        if temp not in allIngredients:
            print("There are no such recipes in the database.")
            return
    ingredientsID = set()
    for ingre in ingredients:
        temp = cur.execute(f"SELECT ingredient_id  FROM ingredients WHERE ingredient_name='{ingre}'").fetchall()
        conn.commit()
        for temp1 in temp:
            ingredientsID.add(temp1[0])
    recipeIDPrime = list()
    for ingreID in ingredientsID:
        tempSet = set()
        temp = cur.execute(f"SELECT DISTINCT recipe_id FROM quantity WHERE ingredient_id={ingreID}").fetchall()
        for temp1 in temp:
            tempSet.add(temp1[0])
        recipeIDPrime.append(tempSet)
    recipeIDPrime = set.intersection(*recipeIDPrime)
    res = recipeID  & recipeIDPrime
    returnValues = []
    for ans in res:
        temp = cur.execute(f"SELECT recipe_name FROM recipes WHERE recipe_id={ans}").fetchall()
        returnValues.append(temp[0][0])
    if not returnValues:
        print("There are no such recipes in the database.")
    else:
        print("Recipes selected for you: ", end="")
        i = 0
        for v in returnValues:
            print(v, end="")
            if i != len(returnValues) - 1:
                print(", ", end="")
            i += 1

# dbName = sys.argv[1]
ifArgs, dbName, ingredientsInput, mealsInput = commandLine()
if not ifArgs:
    buildDB(dbName)
    populateTable(dbName, flag='initialisation')
    createTable(dbName, 'recipes')
    createTable(dbName, 'serve')
    createTable(dbName, 'quantity')
    populateTable(dbName, flag='recipes')
elif ifArgs:
    searchCommand(dbName, ingredientsInput, mealsInput)

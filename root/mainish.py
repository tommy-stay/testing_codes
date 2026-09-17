choices = ["eat", "leave", "1", "2", "3", "4"]

customer_cost = 0

def display_menu():
    print("Here is the menu:")
    print("1. Chocolate croissant for $5")
    print("2. BLT Sandwich for $3.50")
    print("3. Pasta for $8.25")
    print("4. Chocolate chip cookies for $2.50")

def food_cost():
    print("Calculating total cost...")

def greetings():
    print("Welcome to The Bakery!")

def chocolate_croissant():
    print("The cost of this is $5")
customer_cost += 5

def blt_sandwich():
    print("The cost of this is $3.50")

def pasta():
    print("The cost of this is $8.25")


def chocolate_chip():
    print("The cost of this is $2.50")


def order_food():
    user_answer = input("What would you like to eat? Type '1', '2', '3', or '4': ")

    if user_answer == "1":
        customer_cost += 5
        food_cost()
        chocolate_croissant()
        pay_or_add()
    elif user_answer == "2":
        customer_cost += 3.50
        food_cost()
        blt_sandwich()
        pay_or_add()

    elif user_answer == "3":
        customer_cost += 8.25
        food_cost()
        pasta()
        pay_or_add()

    elif user_answer == "4":
        customer_cost += 2.50
        food_cost()
        chocolate_chip()
        pay_or_add()

    else:
        print("That is not a valid menu item.")

def final_orderone():
    print("You chose the chocolate croissant.")
    chocolate_croissant()

def final_ordertwo():
    print("You chose the BLT sandwich.")
    blt_sandwich()

def final_orderthree():
    print("You chose the pasta.")
    pasta()

def final_orderfour():
    print("You chose the chocolate chip.")
    chocolate_chip()

def pay_or_add():
    user_pay = input("Would you like to buy something else or pay?")
    if user_pay.lower() == "buy":
       print("Choose another food (not programmed to make something yet)")
    elif user_pay.lower() == "pay":
        print("Alright!")
        food_cost()
    print("Your final cost is", customer_cost)



greetings()

while True:
    user_answer = input("\nWhat would you like to do? (eat or leave): ").lower()

    if user_answer == "eat":
        print("You've come to the right place!\n")
        display_menu()
        order_food()
    elif user_answer == "leave":
        print("Goodbye! Come back soon!")
        break
    else:
        print("Sorry, you are not allowed to do that!")


import time

shopping_list = []
saved_list = []

print("Current state: Story Time")
time.sleep(2)
print("It's a long read, bear with me... I had a great idea.")
time.sleep(2.5)

story = """

(Don't worry, I'll give you 15 seconds to read, it's longer than it seems. 
Do not fret, I don't look upon your reading skills with disdain.)

It was a beautiful Saturday afternoon and you were relaxing on your couch in your apartment.
A sudden rumble disturbed in the quiet peace.
....
It was your stomach. Whoops. At least, no one else heard it.
You stand up and walk to your fridge...
WHOOSH!
....
That was the sound of air rushing through your fridge.
Or rather, an empty one.
There was only a half filled water bottle, disappointment,
and your dissapating hopes and dreams of getting something to eat.

"""
print(story)
time.sleep(15)

story2 = """
Now, you would have ordered some pizza to fulfill your hunger needs...
But you have a roommate...
Mr. Forsyth.
And it would be VERY unkind of you to not buy groceries and 
prevent the potentially starving Mr. Forsyth in the future. 
Right?
Anyways, let's go make a list so you know what to buy.
"""
print(story2)

print("TIME TO MAKE A LIST!")

while True:
    print()
    print("1. Add an Item")
    print("2. Remove an Item")
    print("3. Display the List")
    print("4. Undo the Previous Change")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        saved_list = shopping_list.copy()
        item = input("Enter the item to add: ")
        shopping_list.append(item)
        print(item, "was added to the list.")

    elif choice == "2":
        if shopping_list == []:
            print("The list is empty.")
            time.sleep(3)
            print("You should probably go add something..")
            time.sleep(3)
            print("So that you can... you know... remove it.")

        else:
            saved_list = shopping_list.copy()

            print("Current items:")
            index = 0
            for item in shopping_list:
                print(index, "-", item)
                index = index + 1

            remove_index = int(input("Enter the index of the item to remove: "))

            if remove_index >= 0 and remove_index < 4:
                removed_item = shopping_list.pop(remove_index)
                print(removed_item, "was removed from the list.")
            else:
                print("That index does not exist.")

    elif choice == "3":
        if shopping_list == []:
            print("The list is empty.")
            time.sleep(2)
            print("You should probably go add something..")
            time.sleep(4)
            print("Probably..")
            time.sleep(3)
        else:
            print("Current shopping list:")
            index = 0
            for item in shopping_list:
                print(index, "-", item)
                index = index + 1

    elif choice == "4":
        if saved_list == []:
            print("There is no previous change to undo.")
            time.sleep(2.75)
            print("You should probably go add something..")
            time.sleep(2.75)
            print("So you can... undo it.")
            time.sleep(2.75)
            print("Actually... Better suggestion.. Why are you choosing this"
                  " when you know there's nothing...")
            time.sleep(2)
            print("Now I look upon your choosing skills with disdain. Tsk tsk..")
            time.sleep(4)
            print("You can go now.")
            time.sleep(3)
        else:
            shopping_list = saved_list.copy()
            saved_list = []
            print("The previous change was undone.")

    elif choice == "5":
        if saved_list == []:
            print("Goodbye!")
            time.sleep(3)
            print("What an... empty list...")
            time.sleep(4)
            print("Leaving poor Mr. Forsyth hungry...")
            time.sleep(4)
            print("How unkind...")
            time.sleep(3)
            break
        else:
            print("Wow! You actually filled the list.")
            time.sleep(2)
            print("I won't hold you for too long.")
            print("You should probably go buy those now.")
            print("Goodbye!")
            break

    else:
        print("That's not one of the options. Please enter 1, 2, 3, 4, or 5.")
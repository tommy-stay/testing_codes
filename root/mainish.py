import time

state = "In the street"

# states: go left, go right, go straight, alley, safehouse, in the street, bakery, ice cream store, continue walking, death
path = ["the bakery", "ice cream store", "continue walking", "go left", "go right", "go straight"]
choices = ["eat", "leave", "1", "2", "3", "4"]
user_answers = ["1", "2", "3", "4"]

customer_cost = 0

# Tracking variables.
has_video_tape = False

bakery_locked = False

turned_left = False

turned_right = False

truth_loop = False

trying_to_annoy = False

has_bakery_key = False

bakery_key_code = False

special_easter_egg = False

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


def blt_sandwich():
    print("The cost of this is $3.50")


def pasta():
    print("The cost of this is $8.25")


def chocolate_chip():
    print("The cost of this is $2.50")


def order_food():
    user_answer = input(
        "What would you like to eat? Type '1', '2', '3', or '4': \n"
    ).strip()
    global customer_cost
    if user_answer == "1":
        customer_cost += 5
        food_cost()
        chocolate_croissant()
        pay_or_treat()
    elif user_answer == "2":
        customer_cost += 3.50
        food_cost()
        blt_sandwich()
        pay_or_treat()
    elif user_answer == "3":
        customer_cost += 8.25
        time.sleep(2)
        print("Don't.\n")
        time.sleep(2)
        print("The pasta isn't food...\n")
        time.sleep(1.5)
        print("It's a bakery, why would there be-\n")
        time.sleep(1.5)
        print("Cashier: 'Sorry about that.😊'")
        food_cost()
        pasta()
        pay_or_treat()
    elif user_answer == "4":
        customer_cost += 2.50
        food_cost()
        chocolate_chip()
        pay_or_treat()
    else:
        print("That is not a valid menu item.")


def yes_or_no():
    print("It's a bit of a hassle to make more...\n")
    customer_answer = input("Do you mind just paying? (yes or no)\n").strip().lower()
    if customer_answer == "yes":
        if special_easter_egg == True:
            print("\nThe cashier hands your stuff and her eyes land on the Forsyth resting on your shoulder.\n")
            print("Cashier: What a nice friend you got there.\n")

        print("Cashier: Thank you so much! Here!\n")
        leave_bakery()
    elif customer_answer == "no":
        time.sleep(2)
        print("The cashier's smile fades.\n")
        time.sleep(1.5)
        print("Cashier: Oh.\n")
        time.sleep(1)
        print("Cashier: That's a bit rude, no?")
        time.sleep(1)
        death()


def leave_bakery():
    global bakery_locked, state
    bakery_locked = True
    print("You take the food from the cashier and hand her the required cash.")
    print("You exit the bakery satisfied with your new snack.")
    state = "In the street"


def death():
    print("\nThe lights shut off.")
    time.sleep(3)
    print(
        "\nAs you look around, an ear-deafening screech is heard and"
        " immense pain fills your body."
    )
    time.sleep(1)
    print("YOU FAILED!\n")
    time.sleep(1.5)
    print("THE MONSTER GOT TO YOU.")
    time.sleep(1)
    print("\nTRY AGAIN.")
    exit()


def death_in_street():
    print("\nYou just stand there.\n")
    time.sleep(2)
    print("... Yep.\n")
    time.sleep(2)
    print("Now, you just stand there. Not doing...\n")
    time.sleep(3)
    print("Anything.")
    exit()


def pay_or_treat():
    user_pay = input(
        "\nWould you like to buy something else or pay? (buy or treat)\n"
    ).strip().lower()
    if user_pay == "buy":
        print("\nCashier: Sorry, we're about to close.")
        yes_or_no()
    elif user_pay == "treat":
        print("You smile at the cashier after paying and exit the store with your new treat.")
        print("You look across from you and see a pastel pink themed ice cream shop.\n")
        print("Your stomach grumbles and you give in and go inside.")
        travel()


def travel():
    global state
    print("Travelling to...")
    print("The ice cream store!🍦")
    state = "ice cream store"


while True:
    if state == "In the street":
        print(f"Current state: {state}")

        print(
            "You are currently walking in the street. You stop to look around"
            " at the stores nearby...\n"
        )
        print(
            "Would you like to enter the bakery (left), ice cream store"
            " (right), or continue walking (forward)?\n"
        )
        path = input("Type (left), (right), or (forward).\n").strip().lower()

        if path == "left":
            if bakery_locked:
                print("\nThe bakery doors are shut.")
                print("You try to push it open but it doesnt bugde.")
                print("A handwritten note reads: 'PERMANENTLY CLOSED FOR MAINTENANCE'.")
                print("You can no longer enter the bakery!\n")
                state = "In the street"
                continue
            else:
                state = "Bakery"
        elif path == "right":
            state = "ice cream store"
        elif path == "forward":
            state = "continue walking"
        else:
            print("Sorry, you are not allowed to do that!")
            state = "In the street"

    if state == "Bakery":
        greetings()
        user_answer = input(
            "\nWhat would you like to do? (eat or leave): "
        ).strip().lower()

        if user_answer == "eat":
            print("You've come to the right place!\n")
            display_menu()
            order_food()
        elif user_answer == "leave":
            time.sleep(3)
            print("That's not a choice for you...\n")
            time.sleep(2)
            print("You have to stay..\n")
            time.sleep(2)
            print("There's... something out there...😐\n")
            time.sleep(3)
            user_answer = input("\nWhat would you like to do? (eat): ").strip().lower()

            if user_answer == "eat":
                time.sleep(2)
                print("\nThat's better...\n")
                time.sleep(1.5)
                print("Next time. Don't make this so difficult..\n")
                time.sleep(2)
                display_menu()
                order_food()
            else:
                print("Sorry, you are not allowed to do that!😊\n")
                continue

    elif state == "ice cream store":
        story = """
       You enter the ice cream shop to your left and you take notice of the cozy, warm feeling the decorations make.

       As the bell above the door rings, the cashier welcomes you in with a bright smile. 
       You take notice that the ice cream store is empty except for one lone customer sitting by himself at one of the booths.

       Cashier: 'Hello and welcome, how can I help you?'

       Do you...

       A: Greet the cashier back with a smile and start ordering ice cream.
       OR
       B: Smile at the cashier but walk over to the customer sitting by himself.
       ?
       """
        print(story)
        user_choice = input().strip().lower()

        if user_choice == "b":
            print("\nYou smile at the cashier and take a seat near the man in the booth.")
            print("\nThe man stares at you.\n")
            print("You look back at the man and smile with a small nod.")
            print("Man: 'This here isn't a regular town, you know?'")
            print("You: '..Sorry?'")
            print("Man: 'You should leave before this gets bad.'")
            print(
                "The cashier calls you back to the front and you hesitate before standing up and walking to the front desk.\n")

        if user_choice in ["a", "b"]:
            story = """
           You walk over to the front desk with a kind smile.

           You: 'Hello. Can I order...'

           A: Strawberry ice cream
           OR
           B: Vanilla ice cream

           """
            print(story)
            user_choice = input().strip().lower()

            if user_choice == "b":
                story = """
                You: 'Can I have vanilla ice cream please?'

                The cashier smirks slightly and enters it into POS terminal.

                Cashier: 'Excellent choice, that's our best selling flavor. Let me get that ready for you'

                The cashier walks inside the back to make your ice cream.
                Leaving you alone with the man in the corner booth of the shop who is now staring at you.

                Do you?

                A: Ignore the stranger and sit by yourself in a chair and wait for your ice cream
                OR 
                B: Try to make small talk with the stranger

                """
                print(story)
                user_choice = input().strip().lower()

                if user_choice == "b":
                    print("\nYou approach the strange man.")
                    print("For a moment, he just stares at you..")
                    print("\nYou: 'Hello..?")
                    print("Man: 'This town isn't what it seems like..'\n")
                    print("You: 'Sorry?'")
                    trust_choice = input("Man: 'Do you trust me?'\n (Yes or no)\n").strip().lower()

                    if trust_choice == "yes":
                        print("\nYou: 'Yeah.'")
                        print("Man: 'Good choice.'")
                        print("The man grabs you by your arm and guides you out the side door back toward the bakery kitchen...\n")
                    elif trust_choice == "no":
                        print("\nYou: 'I don't even know you! Of course not!'")
                        print("Man: 'Huh. Suit yourself.. I tried to help you..")
                        time.sleep(2)
                        death()
                        truth_loop = True
                    else:
                        print("\nThe man stares at you slowly, confusion covering his previous expression.")
                        time.sleep(2)
                        print("\nMan: 'That's not what I asked. I said yes or no.'")
                        time.sleep(2)
                        print("\nMan: 'The normal response to that question would be either yes or no!'")
                        time.sleep(2)
                        print("\nMan: 'I don't even know why I'm even bothering to help you a stranger..'")
                        time.sleep(1)
                        print("\nThe man walks off in disappointment.")
                        death_in_street()

                    while truth_loop:
                        print("\nYou and the strange man slip through the alley and into the storage door behind the bakery.\n")
                        print("There's two choices you can make.\n")
                        print("A: Sneak past the cashier into the storage room to search for clues.\n")
                        print("B: Walk into the front room and try talking to the bakery cashier.")
                        choice = input("\nDo you choose A or B? ").strip().lower()

                        if choice == "a":
                            print("\nYou walk quietly into the dark storage room while the strange man keeps watch.")
                            time.sleep(2)
                            print("\nYou find no food for making any of the pastries in a bakery.\n")
                            print("Strange...")
                            print("\nAll you find is wires, cashier aprons, and robot parts.")

                            if not has_video_tape:
                                print("\nSomething catches your eye from underneath a dirty apron..")
                                print("You crawl closer and see it's an old VHS tape.")
                                print("Labelled: 'The Truth'")
                                print("You place the video tape in your back pocket so you can show it to the man.")
                                has_video_tape = True
                            else:
                                print(
                                    "\nYou search the shelves again, but you have ALREADY collected 'The Truth' video tape!")
                                print("There are no other clues left to find here.")

                            print("\nStrange Man: 'We got what we came for! Look out! The cashier is coming!'")
                            print("Do you:\n")
                            print("A: Leave immediately with the strange man out the back door.")
                            print("B: Stay and confront the cashier.")

                            escape_choice = input("\nType A or B: ").strip().lower()
                            if escape_choice == "a":
                                print(
                                    "\nYou and the strange man slip out into the alley just as heavy, metallic footsteps echo inside.\n")
                                print("The strange man locks the back doors tight behind you.\n")
                                bakery_locked = True
                                print("\nStrange Man: 'We can never go back in there. It knows we were there.'")
                                if has_video_tape:
                                    print("\nYou: 'I found this videotape in there. This could be useful, right?'")
                                    print("The man ")
                                    print(
                                        "Strange Man: 'Let's take this tape to the safe house and see what Amaryllis Town really is!'")
                                    state = "go straight"
                                    truth_loop = False
                                else:
                                    state = "In the street"
                                    truth_loop = False
                            else:
                                death()

                        elif choice == "b":
                            print("\nYou walk up to the bakery cashier.")
                            print("Cashier: 'Welcome to the Bakery! What would you like to do?'")
                            print("You try asking her what is wrong with the town, but she responds word-for-word:")
                            print("Cashier: 'Welcome to the Bakery! What would you like to do?'")
                            print(
                                "\nSuddenly, her voice changes into high-pitched static. Sparks fly from her neck!")
                            print("C-C-COULD... I... G-G-GET... YOU... A... C-CROISSANT...?")
                            print("Her eyes flicker red as gear-grinding noises roar from inside her chest!")

                            print("\nStrange Man: 'SHE IS MALFUNCTIONING! WE HAVE TO RUN NOW!'")
                            print("Do you:")
                            print("A: Leave immediately with the strange man.")
                            print("B: Stay and try to help her.")

                            malfunction_choice = input("\nQuickly! Choose A or B: ").strip().lower()
                            if malfunction_choice == "a":
                                print("\nYou run out the exit door into the alley with the strange man.")
                                print("The heavy door slams behind you, locking permanently.")
                                bakery_locked = True
                                print("\nStrange Man: 'That bakery is locked off to us forever now.'")
                                state = "In the street"
                                truth_loop = False
                            else:
                                print(
                                    "\nYou take a step forward to help, but her arm shoots out with unnatural force...")
                                death()

                else:
                    print("You sit waiting by yourself...")
                    death()

            elif user_choice == "a":
                story = """
                You: 'Can I have strawberry ice cream please?'

                The cashier looks at you and her smile drops ever so slightly but bounces back immediately.

                Cashier: 'Sorry, unfortunately we ran out of strawberry ice cream, would you like to order vanilla-'

                A deep voice interuppts the cashier.

                It's the man who was sitting by himself in the booth.

                Man: 'Don't listen to her. You shouldn't be here.'

                Man: 'You need to get out. Fast.'

                What do you do?

                A: Ignore the strange man and order the vanilla ice cream.
                OR 
                B: Listen to the man and escape the ice cream store.
                """
                print(story)
                user_choice = input().strip().lower()

                if user_choice == "b":
                    print("\nYou listen to the man and hurry out the door with him.")
                    print("Man: 'Follow me into the back of the bakery... we need to find proof.'")

                    truth_loop = True
                    while truth_loop:
                        print("\nYou slip through the alley into the storage area behind the bakery.")
                        print("A: Sneak behind the cashier into the storage room to look for clues.")
                        print("B: Walk up and try talking to the cashier.")

                        choice = input("\nChoose A or B: ").strip().lower()

                        if choice == "a":
                            print("\nYou sneak into the back storage room.")
                            print(
                                "Inside, you discover robot parts, dirty aprons, and gears scattered across tables!")
                            print("No materials needed to make food served at this bakery...")
                            print("Strange...")

                            if not has_video_tape:
                                print("\nYou find a videotape labeled: 'The Truth of Amaryllis Town'")
                                print("You slip the videotape into your bag.")
                                has_video_tape = True
                            else:
                                print(
                                    "\nYou search again, but you ALREADY picked up 'The Truth of Amaryllis Town' video tape!")

                            print("\nDo you:")
                            print("A: Leave with the strange man.")
                            print("B: Stay here.")

                            esc = input("\nChoose A or B: ").strip().lower()
                            if esc == "a":
                                bakery_locked = True
                                print(
                                    "\nYou escape out the back alley. The doors bang shut and padlock behind you.")
                                print("You can no longer enter the bakery ever again!")
                                if has_video_tape:
                                    state = "go straight"
                                    truth_loop = False
                                else:
                                    state = "In the street"
                                    truth_loop = False
                            else:
                                death()

                        elif choice == "b":
                            print("\nYou try talking to the cashier.")
                            print("Cashier: 'Hello and welcome! What would you like to order today?'")
                            print("You try to ask questions, but she repeats with robotic precision:")
                            print("Cashier: 'Hello and welcome! What would you like to order today?'")
                            print(
                                "\nSparks burst from her joints! Her jaw unhinges as she begins severely malfunctioning!")
                            print("\nStrange Man: 'RUN! SHE IS GOING TO BLOW!'")
                            print("A: Leave with the strange man.")
                            print("B: Stay.")

                            esc = input("\nChoose A or B: ").strip().lower()
                            if esc == "a":
                                bakery_locked = True
                                print("\nYou dash into the street as the bakery locks up behind you permanently.")
                                state = "In the street"
                                truth_loop = False
                            else:
                                death()
                else:
                    death()

    elif state == "continue walking":
        story = """
    You decide to ignore the temptation of getting a sweet treat and continue walking down the street.

    Time passes by and you reach a familiar road, it's the way home. 
    Yet, you pause.

    It's still bright outside, you don't have to head home yet.

    Do you...

    A: Take one last lap before heading inside to burn off some energy.
    OR
    B: Give in and go inside to get extra rest? 
    """
        print(story)
        user_choice = input().strip().lower()

        if user_choice == "a":
            story = """
            You: 'What's the harm in getting a little more steps in tonight?'

            You turn to your left and head down the street.

            As time goes on, you come across a three-way split in the road: turn left, turn right, or go forward."""

            print(story)

            if trying_to_annoy:
                print("Don't try it again..")
                time.sleep(2)
                print("I'm seriously warning you.")
                time.sleep(4)
                print("Choose wisely...\n")

            direction_choice = input("Which direction do you take? (left, right, forward): \n").strip().lower()

            if direction_choice == "left":
                state = "go left"
            elif direction_choice == "right":
                state = "go right"
            elif direction_choice == "forward":
                state = "go straight"
            else:
                if trying_to_annoy:
                    death_in_street()
                else:
                    print("\nNot an option.\n")
                    time.sleep(5)
                    print("You're just going to stand there?\n")
                    time.sleep(2)
                    print("Are you serious?")
                    time.sleep(3)
                    print("\nHow useless..")
                    time.sleep(3)
                    trying_to_annoy = True
                    state = "continue walking"

        elif user_choice == "b":
            print("\nYou walk inside your apartment.\n")
            time.sleep(2)
            print("The door was left unlocked, that's odd.")
            time.sleep(2)
            print("\nYou could have swore you locked it when you left.\n")
            print("You shrug it off and walk inside. As soon as you do the door locks behind you.\n")
            time.sleep(1)
            death()

    elif state == "go left":
        print("\nYou turn to go left...")
        time.sleep(0.5)
        print(
            "\nAs you keep walking, you pass by tall, clean houses. But no one playing outside or sitting on the porch.")
        time.sleep(2)
        print("\nThe lights aren't on in any of the houses either...\n")
        time.sleep(2)
        print(
            "You shake your head and just keep going. You don't have the right to question anyone's light choices.\n")
        time.sleep(3)
        print(
            "You've been walking for a couple minutes and something feels odd. So you stop and look around.\n")
        time.sleep(2)
        print("You're back at the three-way split!")
        time.sleep(1)
        print("That's odd... but whatever.")
        turned_left = True

        direction_choice = input("Which direction do you take? (left, right, forward): ").strip().lower()

# no matter what user chooses they end up back at the split
# if you go right, you'll get a different code that will give you a secret ending
# if you go forward, you'll find an easter egg of something
        if direction_choice == "right":
            turned_right = True
            print("ill make a story that either leads you to trap or gives you evidence but you'll end back at the three way split.")
            state = "go right"
        elif direction_choice == "forward":
            print(
                "specific pre-story with an easter egg will happen"
                " but you'll end up back at the three way split.")
            state = "go straight"
        else:
            death_in_street()

    elif state == "go right":
        print("\nYou turn to go right...")
        time.sleep(2)
        print("\nYou walk through the quieter side of the neighborhood. But you notice something strange.\n")
        time.sleep(2)
        print("This neighborhood is usually quiet but now it's a bit too quiet..\n")
        print("You pass the down the somewhat familiar street and spot the abandoned neighborhood park that no one ever used...")
        time.sleep(2)
        print("For whatever reason.\n")
        print("You look around and almost walk into the dark, tall lampost.")
        time.sleep(2)
        print("You step back a little, feeling a bit embarrassed until you notice something on the lampost.\n")
        time.sleep(2)
        print("You spot '1984' scratched into a lamppost on the corner.\n")
        print("You take note of it but shrug it off, must have been some kid vandalizing the park for fun.\n")
        time.sleep(3)
        print("You've been walking for a couple minutes and something feels odd. So you stop and look around.\n")
        time.sleep(2)
        print("You're back at the three-way split!")
        time.sleep(1)
        print("That's odd... but whatever.\n")
        state = "continue walking"

    elif state == "go straight":
        print("\nYou walk straight ahead and reach an abandoned safe house with a digital keypad on the door.")

        while True:
            code = input("\nEnter the 4-digit passcode to unlock the door (or type 'back' to return to the street): \n").strip()


            if code == "1984":
                print("\n*CLICK* The heavy door unlocks! You step inside.")
                state = "safe house"
                break
            if code == "4460":
                if bakery_key_code == True:
                    print("You enter 4460 in the digital keypad.\n")
                    time.sleep(2)
                    print("*CLICK* A camera comes out of the top of the door and scans you down.")
                    print("\nYou look directly at it and wait as the cyan light scans over you.")
                    time.sleep(3)
                    print("\nCamera: 'OBJECT NOT IDENTIFIED! INTRUDER DETECTED!'")
                    time.sleep(1)
                    print("\nThe camera's light changes to a vibrant red.\n")
                    time.sleep(1)
                    print("The door activates a loud ear-piercing siren and you quickly cover your ears.\n")
                    time.sleep(2)
                    print("You step back out of the camera's light and the camera light changes back to the cyan.")
                    print("The sound dies down abruptly and the camera shrinks back into the wall.\n")
                    time.sleep(1)
                    print("You run away from the digital keypad and back into the street, not bothering to try again right now.\n")
                    state = "go straight"

                if bakery_key_code == False:
                    print("\n*WHIR*")
                    time.sleep(2)
                    print("The door makes a small whirring sound, then a small door underneath the door handle opens.")
                    time.sleep(1)
                    print("A small compartment opens and you get a rusty bronze key.")
                    print("You don't know what it unlocks but you pocket it anyway and stand up.")
                    has_bakery_key = True
                    bakery_code = True
                    state = "continue walking"
            if code == "2723":
                print("the door opens a little bit and a small toy gets pushed out.\n")
                print("when you pick it up, you realize it's a small Mr. Forsyth in his iconic green sweater with gold sword.\n")
                print("Door: 'Special item unlocked. Enjoy, he's your new companion now.\n")
                time.sleep(2)
                print("You smile and place the little Forsyth on your shoulder.\n")
                print("Now it's not so lonely in this odd town.\n")
                special_easter_egg = True

            elif code.lower() == "back":
                state = "In the street"
                break
            else:
                print("Wrong passcode. Please try again.\n")

    elif state == "alley":
        print("\nYou are standing in the dark back alley behind the bakery.")
        choice = input("Where do you want to go? (street): ").strip().lower()
        state = "In the street"

    elif state == "safe house":
        print("\nYou enter the safe house away from the robot.")
        if has_video_tape:
            print("\nYou figured out the truth!!")
            print("You play the video tape with the strange man and discover Amaryllis Town isn't a regular town..\n")
            time.sleep(2)
            print("It's actually run by robots!\n")
            print("Congratulations! You won!")
        else:
            print("You escaped safely into the bunker, but you didn't manage to bring the evidence videotape...")
            print("\nYou survived but you still don't know the truth about the town...\n")
            print("Try again if you want to figure out what it is. Don't get caught though!")
        exit()
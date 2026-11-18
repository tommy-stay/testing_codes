import time

students = {
    "Daniel": 85,
    "Tomi": 82,
    "Shivangni": 90,
    "Bart": 62,
    "Daniella": 88,
    "Helene": 83
}

tasks = [
    "Look up a student's grade",
    "Change a student's grade",
    "Add a new student",
    "Remove a student",
    "Show the current amount of students",
    "Display the students and their grades"
]

completed_tasks = []

story = """
(You have 10 seconds to read through it.)

Wow! Congratulations! You passed the job interview, you're a teacher now!
    How great is that! Well, now it's time to actually get started.
    You're subbing for a Computer Science 15 and 25 class in STEM.
    Mr. Forsyth, the original teacher, had to take a leave due to food poisoning...
    It's rumored his roommate didn't buy any food for the fridge
    so he ended up eating a left-out donut in the staff room.
    What a bad roommate... Anyways! Enough of that. Let's get to work.
"""
print(story)
time.sleep(10)

story2 = """
(You'll have 5 seconds to read this one.)

The students just finished working on a List Making Assignment, and your job is to grade them!
    Mr. Forsyth left you a dictionary with each student's current average.

    He also left you a list of tasks to complete.
    You can view the tasks and check them off as you finish them.

    Good luck!
"""
print(story2)
time.sleep(5)


while True:
    print()
    print("TIME TO GRADE THE STUDENTS!")
    print()
    print("1. Look Up a Student's Grade")
    print("2. Change a Student's Grade")
    print("3. Add a Student")
    print("4. Remove a Student")
    print("5. Show Current Amount of Students")
    print("6. Display the Students and Their Grades")
    print("7. View Mr. Forsyth's Tasks")
    print("8. Check Off a Task")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        student = input("Enter the student's name: ")

        if student in students:
            print(student, "'s current grade is", students[student], ".")
        else:
            print("That student is not in the class.")

    elif choice == "2":
        print()
        print("Current students:")

        for student in students:
            print(student)

        student = input("Enter the name of the student whose grade you want to change: ")

        if student in students:
            new_grade = int(input("Enter " + student + "'s new grade: "))
            students[student] = new_grade
            print(student, "'s grade was changed to", students[student], ".")
        else:
            print("That student is not in the class.")

    elif choice == "3":
        new_student = input("Enter the name of the new student: ")
        new_student_grade = int(input("Enter " + new_student + "'s grade: "))
        students[new_student] = new_student_grade
        print(new_student, "was added to the class with a grade of", students[new_student], ".")

    elif choice == "4":
        print()
        print("Current students:")

        for student in students:
            print(student)

        student = input("Enter the name of the student you want to remove: ")

        if student in students:
            students.pop(student)
            print(student, "was removed from the class.")
        else:
            print("That student is not in the class.")

    elif choice == "5":
        print("There are currently", len(students), "students in the class.")

    elif choice == "6":
        print()
        print("Current class grades:")

        for student, grade in students.items():
            print(student, "-", grade)

    elif choice == "7":
        print()
        print("Mr. Forsyth's Tasks:")

        for task in tasks:
            if task in completed_tasks:
                print("[X]", task)
            else:
                print("[ ]", task)

    elif choice == "8":
        print()
        print("Tasks:")

        index = 0
        for task in tasks:
            if task in completed_tasks:
                print(index, "- [X]", task)
            else:
                print(index, "- [ ]", task)
            index = index + 1

        task_number = int(input("Enter the number of the task you want to check off: "))

        if task_number >= 0 and task_number < len(tasks):
            task = tasks[task_number]

            if task in completed_tasks:
                print("That task has already been checked off.")
            else:
                completed_tasks.append(task)
                print("You checked off:", task)
        else:
            print("That task number does not exist.")

    elif choice == "9":
        if len(completed_tasks) == len(tasks):
            print()
            print("Wow! You did it! I'm so proud!")
            time.sleep(2)
            print("Or rather Mr. Forsyth is proud of you... Same thing.\n")
            time.sleep(2)
            print("Your day of work is now over! You can go home. Bye bye!\n")
        elif len(completed_tasks) > 0:
            print()
            time.sleep(3)
            print("\nWell...")
            time.sleep(2)
            print("\nYou DID do something.. So I can't really get mad at you..")
            time.sleep(2)
            print("\nGood job for trying... I guess..")
            time.sleep(1)
            print("\nBye...?")
        else:
            print()
            print("...")
            time.sleep(2)
            print("\nNow, you're just downright lazy.\n")
            time.sleep(2)
            print("Why would you go to the interview for a teacher")
            print("if you aren't going to do what a teacher would do?\n")
            time.sleep(2)
            print("Poor Mr. Forsyth is going to have to come in while sick ")
            print("to do the work you weren't able to do!\n")
            time.sleep(2)
            print("So rude... Just so rude...")

        break

    else:
        print("That's not one of the options. Please enter 1, 2, 3, 4, 5, 6, 7, 8, or 9.")
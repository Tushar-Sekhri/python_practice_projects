# in this program the computer will genertae a random number between 0 to 100 and we will try to guess it ,
# based on our answer there can be there options :
# 1. number is too high 
# 2. number is too low 
# 3. yup this is your number

# Number Guessing Game
# The computer generates a random number between 0 and 100.
# Guess the number based on the hints.
# Difficulty Levels:
# Easy   -> Unlimited lives
# Medium -> 5 lives
# Hard   -> 3 lives

import random

secret_number = random.randint(0, 100)
attempts = 0

level = input("Choose difficulty (Easy-e, Medium-m, Hard-h): ").strip().lower()

if level == "e":
    lives = None
elif level == "m":
    lives = 5
elif level == "h":
    lives = 3
else:
    print("Invalid choice. Defaulting to Easy mode.")
    lives = None

print("\n Game Started!")
print("Guess a number between 0 and 100.\n")

while True:

    if lives == 0:
        print("\n You lost!")
        print(f"The secret number was {secret_number}.")
        break

    if lives is None:
        print("Lives: Unlimited")
    else:
        print(f"Lives Remaining: {lives}")

    try:
        guess = int(input("Enter your guess: "))

        if guess < 0 or guess > 100:
            print("Please enter a number between 0 and 100.\n")
            continue

        attempts += 1

        if guess > secret_number:
            print("Too High!")

            difference = guess - secret_number
            if difference <= 5:
                print("Very Close!")
            elif difference <= 10:
                print("Close.")
            else:
                print("Far Away.")

            if lives is not None:
                lives -= 1

        elif guess < secret_number:
            print("Too Low!")

            difference = secret_number - guess
            if difference <= 5:
                print("Very Close!")
            elif difference <= 10:
                print("Close.")
            else:
                print("Far Away.")

            if lives is not None:
                lives -= 1

        else:
            print("\nCongratulations!")
            print(f"You guessed the number {secret_number} correctly!")
            print(f"It took you {attempts} attempts.")
            break

        print()

    except ValueError:
        print("Please enter a valid integer.\n")
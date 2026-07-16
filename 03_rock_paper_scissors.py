import random

options=['r','p','s']

names = {
    "r": "Rock",
    "p": "Paper",
    "s": "Scissors"
}
def get_user_choice():
    choice=input("Enter your choice (r/p/s) :").strip().lower()
    if choice  in options:
        return choice
    else:
        print("Invalid choice ,choose r,p or s")
    
def play_game():
    computer_choice=random.choice(options)
    your_choice = get_user_choice()

    print(f"Computer chose: {names[computer_choice]}")

    if your_choice == computer_choice:
        print("its a draw")
        return "draw"

    elif (
    (your_choice == "r" and computer_choice == "s") or
    (your_choice == "p" and computer_choice == "r") or
    (your_choice == "s" and computer_choice == "p")
    ):
        print("you win")
        return "player"
        
    else:
        print("you loose")
        return "computer"
        

def play_again():

      while True:
        choice = input("Play again? (y/n): ").strip().lower()
        if choice in ("y", "n"):
            return choice == "y"
        print("Please enter only y or n.")
    
your_score = 0
computer_score = 0
draws = 0

while True:

    result = play_game()

    if result == "player":
        your_score += 1
    elif result == "computer":
        computer_score += 1
    else:
        draws += 1

    print("\nScoreboard")
    print(f"You      : {your_score}")
    print(f"Computer : {computer_score}")
    print(f"Draws    : {draws}\n")

    if not play_again():
        print("Thanks for playing!")
        break

    
   
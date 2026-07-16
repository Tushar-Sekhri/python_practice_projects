import random

options=['r','p','s']

names = {
    "r": "Rock",
    "p": "Paper",
    "s": "Scissors"
}

your_score=0
computer_score=0
draw=0
game_running=True
while game_running:
    computer_choice=random.choice(options)
    your_choice=input("Enter your choice (r/p/s) :").strip().lower()
    print(f"Computer chose: {names[computer_choice]}")
    

    if your_choice not in options:
        print("Invalid choice ,choose r,p or s")
        continue

    elif your_choice == computer_choice:
        print("It's a draw!")
        draw+=1

    elif (
    (your_choice == "r" and computer_choice == "s") or
    (your_choice == "p" and computer_choice == "r") or
    (your_choice == "s" and computer_choice == "p")
    ):
        print("You win!")
        your_score+=1
    else:
        print("You lose!")
        computer_score+=1
    
    print("\nScoreboard")
    print(f"You      : {your_score}")
    print(f"Computer : {computer_score}")
    print(f"Draws    : {draw}\n")

    
    while True:
        play_again=input("Do you want to play again(y/n) :").strip().lower()
        if play_again == "y":
            break

        elif play_again == "n":
            print("Thanks for playing!!")
            game_running=False 
            break     

        else:
            print("Please enter only 'y' or 'n'.")
#  task is to create a dice rolling game which will ask user:
# Roll the dice? (y/n): 
# type anything else it shows invalid choice 
# if n (no) then exit if y(yes) then it will give output two numbers eg. (1,5) 
import random 
while True:
    choice=input("Roll the dice? (y/n): ").strip().lower()
    if choice=='y':
        dice_roll1=random.randint(1,6)
        dice_roll2=random.randint(1,6)
        print(f"({dice_roll1},{dice_roll2})")

    elif choice =='n':
         print("thanks for playing")
         break
    else :
         print ("invalid choice , enter y or n ")

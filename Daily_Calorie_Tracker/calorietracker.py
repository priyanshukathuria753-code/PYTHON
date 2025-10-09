#Calorie Tracker

print("***Daily Calorie Tracker***")

meals=[]
calories_intake=[]

z=int(input("Enter total number of meals you had today:"))

for i in range(z):
    meal=input(f"Enter the name of the meal{i+1}:")
    cal_str=input(f"Enter the colories intake for the meal {meal}:")
    print()
    cal_str=float(cal_str)
    meals.append(meal)
    calories_intake.append(cal_str)

print("\n***** Daily Calorie Report *****")
for i in range(len(meals)):
    print(f"Meal: {meals[i]}, Calories: {calories_intake[i]} kcal")

Total_calories=sum(calories_intake)
print("\nTotal calories intake for the day:",Total_calories)

Calories_left=1800-Total_calories
print("\nCalories left for the day:",Calories_left)

Average_calories=Total_calories/z
print("Average calories intake for the day:",Average_calories)

if Total_calories>1800:
        print("Warning: You have exceeded your daily calorie limit!")
else :
        print("Good Job! you are within your daily calorie limit")
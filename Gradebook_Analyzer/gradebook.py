# ------------------------------------------------------------
# Priyanshu Kathuria
# November 2025
# Gradebook Analyzer
# ------------------------------------------------------------

#welcome message
print("======================================")
print("   Welcome to the Gradebook Analyzer   ")
print("======================================\n")

#functions and calculations
def calculate_average(marks_dict):
    if not marks_dict:
        return 0
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    scores = sorted(marks_dict.values())
    n = len(scores)
    if n == 0:
        return 0
    mid = n // 2
    return (scores[mid - 1] + scores[mid]) / 2 if n % 2 == 0 else scores[mid]

def find_max_score(marks_dict):
    if not marks_dict:
        return 0
    return max(marks_dict.values())

def find_min_score(marks_dict):
    if not marks_dict:
        return 0
    return min(marks_dict.values())

#assign graded using if-else
def assign_grades(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
    return grades

def count_grade_distribution(grades_dict):
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for grade in grades_dict.values():
        distribution[grade] += 1
    return distribution

#check for pass and fail
def pass_fail(marks_dict):
    return (
        [n for n, s in marks_dict.items() if s >= 40],
        [n for n, s in marks_dict.items() if s < 40]  )

#table
def results_table(marks_dict, grades_dict):
    print("\nName\t\tMarks\tGrade")
    print("-------------------------------------")
    for name in marks_dict:
        print(f"{name:<10}\t{marks_dict[name]:<6}\t{grades_dict[name]}")
    print("-------------------------------------")

#input marks and assign grade using loop
while True:
    print("\nMenu:")
    print("1. Enter Student Data Manually")
    print("2. Exit")

    choice = input("\nEnter your choice (1 or 2): ")

    if choice == "1":
        marks = {}
        num_students = int(input("\nEnter number of students: "))

        for i in range(num_students):
            name = input(f"Enter name of student {i+1}: ")
            mark = float(input(f"Enter marks for {name}: "))
            marks[name] = mark


        avg = calculate_average(marks)
        median = calculate_median(marks)
        high = find_max_score(marks)
        low = find_min_score(marks)

        print("\n--- Summary ---")
        print(f"Average Marks: {avg:.2f}")
        print(f"Median Marks: {median:.2f}")
        print(f"Highest Marks: {high}")
        print(f"Lowest Marks: {low}")


        grades = assign_grades(marks)
        distribution = count_grade_distribution(grades)

        print("\n--- Grade Distribution ---")
        for grade, count in distribution.items():
            print(f"{grade}: {count}")


        passed, failed = pass_fail(marks)

        print("\n--- Pass/Fail Summary ---")
        print(f"Passed: {', '.join(passed) if passed else 'None'}")
        print(f"Failed: {', '.join(failed) if failed else 'None'}")



        print("\n--- Final Results ---")
        results_table(marks, grades)

    elif choice == "2":
        print("\nExiting the Gradebook Analyzer. Goodbye!")
        break

    else:
        print("\nInvalid choice. Please try again.")
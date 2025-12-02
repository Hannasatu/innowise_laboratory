
student  = []
def main():
    while True:
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report (all students)")
        print("4. Find top performer")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                    add_new_student(student)
            elif choice == 2:
                    add_grades_for_student(student)
            elif choice == 3:
                    show_report(student)
            elif choice == 4:
                    find_top_performer(student)
            elif choice == 5:
                    print("Exiting program. Goodbye!")
                    break
            else:
                    print("Invalid choice. Please try again.")
        except ValueError:
                print("Invalid input. Please enter a number from 1 to 5.")
                continue


def add_new_student(student_list):
    name = input("Enter your name: ").strip()
    if not name:
        print("Name is empty. Please enter a name.")
        return

    for student_dict in student_list:
        if student_dict["name"].lower() == name.lower():
            print(f"Student '{name}' already exists.")
            return


    student_list.append({"name": name, "grades": []})
    print(f"Student '{name}' added successfully.")

def add_grades_for_student(student_list):
    if not student_list:
        print("No students have been added yet.")
        return

    name = input("Enter the name of the student to add grades for: ").strip()
    student_found = False

    for student_dict in student_list:
        if student_dict["name"].lower() == name.lower():
            student_found = True
            print(f"Adding grades for {student_dict['name']}. Enter 'done' when finished.")
            while True:
                grade_input = input("Enter grade (0-100) or 'done': ").strip().lower()
                if grade_input == 'done':
                    break

                try:
                    grade = int(grade_input)
                    if 0 <= grade <= 100:
                        student_dict["grades"].append(grade)
                        print(f"Grade {grade} added for {student_dict['name']}.")
                    else:
                        print("Grade must be between 0 and 100.")
                except ValueError:

                    print("Invalid input. Please enter a number for the grade or 'done'.")
                except ZeroDivisionError:
                    print("An unexpected ZeroDivisionError occurred during grade input validation.")
            break

    if not student_found:
        print(f"Student '{name}' not found.")
def show_report(student_list):
    if not student_list:
        print("No students have been added yet.")
        return

    print("\n--- Student Grades Report ---")
    all_grades_overall = []
    students_with_grades_count = 0

    for student_dict in student_list:
        name = student_dict["name"]
        grades = student_dict["grades"]

        if grades:
            try:
                average_grade = sum(grades) / len(grades)
                print(f"{name}'s average grade is {average_grade:.2f}.")
                all_grades_overall.extend(grades)
                students_with_grades_count += 1
            except ZeroDivisionError:

                print(f"{name} has no grades, his average should be N/A (ZeroDivisionError avoided).")
        else:
            print(f"{name} has no grades, his average should be N/A.")

    print("\n--- Overall Summary ---")
    if student_list:
        print(f"Total number of students registered: {len(student_list)}")

    if all_grades_overall:
        overall_average = sum(all_grades_overall) / len(all_grades_overall)
        min_overall_grade = min(all_grades_overall)
        max_overall_grade = max(all_grades_overall)

        print(f"Total students with grades: {students_with_grades_count}")
        print(f"Overall average grade across all students: {overall_average:.2f}")
        print(f"Minimum grade observed: {min_overall_grade}")
        print(f"Maximum grade observed: {max_overall_grade}")
    else:
        print("No grades present at all among registered students.")

def find_top_performer(student_list):
    if not student_list:
        print("No students have been added yet.")
        return

    students_with_grades = [s for s in student_list if s["grades"]]

    if not students_with_grades:
        print("No top student: No students have grades yet.")
        return

    top_student = max(students_with_grades, key=lambda s: sum(s["grades"]) / len(s["grades"]))

    top_avg = sum(top_student["grades"]) / len(top_student["grades"])
    print(f"The top performer is {top_student['name']} with an average grade of {top_avg:.2f}.")


if __name__ == "__main__":
    main()

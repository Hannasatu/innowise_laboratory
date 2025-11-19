import json


def generate_profile(age):
    if 0<= age <= 12:
        return "Child"
    elif 13<=age<=19:
        return "Teenager"
    else:
        return "Abult"
user_name = input("Enter your full name: ")
birthday = input("Enter your birthday year: ")
birthday_year = int(birthday)
age = 2025-birthday_year
hobbies = []

while True:
    hobby  = input("Enter a favourite hobby ot type 'stop' to finish: ").lower()
    if hobby == "stop":
        break
    hobbies.append(hobby)

life_stage = generate_profile(age)

user_profile = {
    "user_name": user_name,
    "birthday": birthday,
    "life_stage": life_stage,
    "hobbies": hobbies
}

print("\n---Profile Details---")
print(f"Name: {user_profile['user_name']}")
print(f"Age: {user_profile['birthday']}")
print(f"Life stage: {user_profile['life_stage']}")

if not user_profile["hobbies"]:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite hobbies( {len(user_profile['hobbies'])} ):")
    for hobby in user_profile["hobbies"]:
        print(f"-\t{hobby.capitalize()}")
print("---")
# Ask the user for their name
name = input("What is your name? ")

# Ask for their current age and convert the input text into a number
age = int(input("How old are you? "))

# Ask for their favorite color
favorite_color = input("What is your favorite color? ")

# Calculate age for next year
next_year_age = age + 1

# Print a friendly summary message
print()  # Adds an empty line for neat formatting
print(
    f"Nice to meet you, {name}! Your favorite color is {favorite_color}, "
    f"and you will be {next_year_age} years old next year!"
)
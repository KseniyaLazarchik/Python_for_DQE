# Importing the random module to generate random numbers
import random

# Create a list of 100 random numbers ranging from 0 to 1000
random_numbers = [random.randint(0, 1000) for _ in range(100)]
print(f"Original list: {random_numbers}")

# Implement selection sort algorithm
for i in range(len(random_numbers)):
     min_index = i
     for j in range(i + 1, len(random_numbers)):
         # Select minimum element in every iteration
         if random_numbers[j] < random_numbers[min_index]:
             min_index = j
     # Swap the elements
     (random_numbers[i], random_numbers[min_index]) = (random_numbers[min_index], random_numbers[i])

# Print sorted list of elements
print(f"Sorted list: {random_numbers}")

# Separate even numbers from the sorted list
even_numbers = [num for num in random_numbers if num % 2 == 0]

# Separate odd numbers from the sorted list
odd_numbers = [num for num in random_numbers if num % 2 != 0]

# Calculate the average of even numbers
try:
    avg_even = sum(even_numbers) / len(even_numbers)
except ZeroDivisionError:
    avg_even = 0  # If there are no even numbers, set the average to 0

# Calculate the average of odd numbers
try:
    avg_odd = sum(odd_numbers) / len(odd_numbers)
except ZeroDivisionError:
    avg_odd = 0  # If there are no odd numbers, set the average to 0

# Print the average of even numbers
print(f"The average of even numbers is: {avg_even}")

# Print the average of odd numbers
print(f"The average of odd numbers is: {avg_odd}")


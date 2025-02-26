import random
import string
from collections import defaultdict

# Generate a random number of dictionaries (between 2 and 10)
num_dicts = random.randint(2, 10)

# Create empty list
dicts_list = []

# Generate list for random number of dictionaries
for i in range(num_dicts):
    # Generate a random number of keys (between 1 and 10)
    num_keys = random.randint(1, 10)
    # Randomly select letters for keys
    keys = random.sample(string.ascii_lowercase, num_keys)
    # Create a dictionary with random values (0-100)
    new_dict = {key: random.randint(0, 100) for key in keys}
    # Append the dictionary to the list
    dicts_list.append(new_dict)

print(dicts_list)

# Create a default dict to store the max values and corresponding dictionary index
merged_dict = defaultdict(lambda: (0, 0))

# Count of dictionary iterations
for i, d in enumerate(dicts_list, start=1):
    # Go through dictionary items
    for key, value in d.items():
        # If key already exists, compare values
        if value > merged_dict[key][0]:
            merged_dict[key] = (value, i)
        elif key not in merged_dict:
            merged_dict[key] = (value, i)

# Create the final dictionary with keys renamed according to the rules
final_dict = {}
for key, (value, idx) in merged_dict.items():
    new_key = f"{key}_{idx}" if len([d for d in dicts_list if key in d]) > 1 else key
    final_dict[new_key] = value

# Printing the final dictionary
print(final_dict)

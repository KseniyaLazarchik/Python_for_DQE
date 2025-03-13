text = """
 tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces.
"""
#Calculate number of whitespace characters
whitespace_count = sum(1 for char in text if char.isspace())
print(f"Number of whitespace character is {whitespace_count}.")

# Remove all unnecessary spaces
text_new = text.replace('\n', ' ').replace('“', ' “')
# Lowercase everything
text_new = ' '.join(text_new.split()).lower()

# Create list for new words
last_words = []

# Split by sentences (by .)
sentences_split = text_new.split('. ')

# Find last words in sentences
for sentence in sentences_split:
    words = sentence.split()
    if words:
        last_words.append(words[-1])

sentence_new = ' '.join(last_words).capitalize()
print(f"New sentence is: {sentence_new}")

sentences = [sentence.strip().capitalize() for sentence in sentences_split]
text_new = '. '.join(sentences)

# Show resalt with a new entence
result = text_new + " " + sentence_new

# Fix “iz” with correct “is”
# Only fix “iz” surrounded by whitespace
#result = result.replace( ' iz ', ' is ')
# OR
# Fix “iz” surrounded by spaces and special characters
replacements = [
    ("iz", "is"),
    ("'iz'", "'is'"),
    ('"iz"', '"is"')
]

for old, new in replacements:
    result = result.replace(old, new)

print(result)

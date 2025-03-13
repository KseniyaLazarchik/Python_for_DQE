import re

text = """
 tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces.
"""
#Calculate number of whitespace characters
whitespace_count = sum(1 for char in text if char.isspace())
print(f"Number of whitespace character is {whitespace_count}.")

# Replace newline characters with spaces and adjust spacing around quotes
text_new = text.replace('\n', ' ').replace('“', ' “')
# Remove extra whitespace and lowercase everything
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

# Show result with a new sentence
result = text_new + ' ' + sentence_new

# Fix “is” surrounded by spaces or placed in start or end of sentence
result = re.sub(r'(?<=\s)iz(?=\s)', 'is', result)

print(result)

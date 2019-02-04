
'''

A user enters a sentence.

Print the sentence in reverse order in words.

Only the 1st letter is in upper case as shown below.

Use one “For” statement.

The input is a complete sentence with a “.”.

The reversed output is also a complete sentence with a “.”.

You cannot use more than one ‘for’ statement.
You cannot use ‘while’ statement.

we haven't covered the reverse statement so i don't really have a clue how to start this

'''

sentence = "Talis is the best bot known to man."

sentence_l = sentence.replace(".", "").lower().split(" ")
words = len(sentence_l)

reverse = []
for i in range(words):
    reverse.append(sentence_l[(words-1)-i].lower())

print(" ".join(reverse).capitalize() + ".")

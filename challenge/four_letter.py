
haystack = None

with open("four_letter.py", 'r') as fh:
    haystack = fh.readline().strip("\r\n")

fh.close()

print(haystack)

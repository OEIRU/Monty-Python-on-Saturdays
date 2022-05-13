word = input()
word = word.split()
word = ''.join(word)
print(word)
if str(word) == str(word)[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")
# Checking for a palindrome

word = str(input())
if str(word) == str(word)[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")